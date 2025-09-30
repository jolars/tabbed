# Bug Report for Tabbed Package

Based on my analysis of the tabbed package source code, I've identified several critical bugs that could cause failures or unexpected behavior when parsing data files with leading metadata sections. Below is a comprehensive list of the bugs found:

## Critical Bugs

### 1. **StopIteration Exception in File Reading (Critical)**

**Location:** `src/tabbed/reading.py`, line 442
**Bug:** Unhandled StopIteration when trying to advance file pointer beyond file length

```python
# Problematic code in _prime() method:
[next(self.infile) for _ in range(astart)]
```

**Root Cause:** The autostart calculation in `_prime()` method can compute a line number that exceeds the actual file length. This happens when:
- Metadata detection fails and incorrectly identifies the entire file as metadata
- Header detection returns `None` and metadata detection returns an end line number equal to or greater than the file length

**Example failure case:**
```
File content: "metadata\nheader,col2\ndata,val2\n" (3 lines)
Computed autostart: 4 (beyond file length)
Result: StopIteration when trying to skip 4 lines
```

**Impact:** Complete failure to read files where metadata detection incorrectly includes data sections.

### 2. **Invalid Delimiter Handling (Critical)**

**Location:** `src/tabbed/sniffing.py`, lines 306-311
**Bug:** CleverCSV sometimes returns invalid delimiters that Python's csv module cannot handle

```python
# Problematic code in dialect setter:
delimiter = '\r' if value.delimiter == '' else value.delimiter
```

**Root Cause:** When CleverCSV fails to detect a proper delimiter for single-column data or files without clear delimiters, it may return `\r` as a delimiter. Python's csv module considers `\r` an invalid delimiter value.

**Example failure cases:**
- Single line files: "single line"
- Single column data: "A\nB\nC\nD"
- Files without clear delimiters

**Impact:** RuntimeError when trying to create csv.DictReader with invalid dialect.

### 3. **Empty File Handling (Critical)**

**Location:** `src/tabbed/sniffing.py`, lines 443-449
**Bug:** Type detection fails for empty files or files containing only excluded values

```python
if not rows:
    raise RuntimeError(msg)
```

**Root Cause:** When all rows in a file contain only values in the exclude list (empty strings, spaces, 'nan', etc.), the type detection fails instead of gracefully handling the edge case.

**Example failure cases:**
- Completely empty files
- Files with only whitespace or newlines
- Files containing only "excluded" values

**Impact:** RuntimeError during Reader initialization for edge case files.

### 4. **Metadata Boundary Detection Error (Medium)**

**Location:** `src/tabbed/reading.py`, lines 392-395
**Bug:** Incorrect autostart calculation when metadata detection fails

```python
metalines = self._sniffer.metadata(None, self.poll, self.exclude).lines
autostart = metalines[1] + 1 if metalines[1] else metalines[0]
```

**Root Cause:** When metadata detection returns `metalines[1]` as `None`, the code falls back to `metalines[0]` which is typically 0, but this doesn't account for cases where the file should start reading from a different position.

**Impact:** Data may be read from wrong starting position, potentially including metadata in the data results.

## Medium Priority Bugs

### 5. **Header Name Collision Handling (Medium)**

**Location:** `src/tabbed/sniffing.py`, lines 61-70
**Bug:** Header name disambiguation may create invalid or confusing column names

```python
mapping = {
    name: (
        [name] if cnt < 2 else [name + '_' + str(v) for v in range(cnt)]
    )
    for name, cnt in counted.items()
}
```

**Issue:** When duplicate header names exist, the renaming strategy creates names like "col_0", "col_1", etc., which may conflict with existing names or be unintuitive.

### 6. **Type Consistency Detection Logic (Medium)**

**Location:** `src/tabbed/sniffing.py`, lines 458-462
**Bug:** Type consistency check has overly restrictive logic

```python
if len(s) > 1 and not s.issubset({float, int, complex}):
    consistent = False
    break
```

**Issue:** The logic considers columns inconsistent if they contain mixed types, even when some mixing (like int/float) should be acceptable in more cases.

## Low Priority Issues

### 7. **Inefficient Large File Handling**

**Location:** Multiple locations in parsing and reading modules
**Issue:** No chunked processing for very large files during metadata/header detection phase, which could cause memory issues.

### 8. **Limited Error Context**

**Location:** Throughout the codebase
**Issue:** Error messages often lack sufficient context about file position, line numbers, or specific content that caused the failure.

### 9. **Unicode and Encoding Edge Cases**

**Issue:** No explicit handling of files with different encodings or BOM (Byte Order Mark).

## Recommended Fixes

### For Critical Bug #1 (StopIteration):
```python
# In _prime() method, add bounds checking:
file_lines = sum(1 for _ in self.infile)
self.infile.seek(0)
astart = min(astart, file_lines)  # Ensure we don't exceed file length

# Or use safer iteration:
try:
    for _ in range(astart):
        next(self.infile)
except StopIteration:
    # Handle case where file is shorter than expected
    pass
```

### For Critical Bug #2 (Invalid Delimiter):
```python
# In dialect setter, validate delimiter:
if value:
    delimiter = value.delimiter
    if delimiter == '' or delimiter == '\r':
        # Fall back to comma for invalid delimiters
        delimiter = ','
    value.delimiter = delimiter
```

### For Critical Bug #3 (Empty Files):
```python
# In types() method, handle empty rows gracefully:
if not rows:
    # Return default types for single string column
    return [str], True
```

## Testing Recommendations

1. Add tests for empty files and files with only whitespace
2. Add tests for files with invalid or unclear delimiters
3. Add tests for files where metadata detection might fail
4. Add tests for extremely small files (1-2 lines)
5. Add tests for files with Unicode content and different encodings
6. Add stress tests with very large files or very long lines

These bugs represent real-world edge cases that could cause the software to fail when processing certain types of data files, particularly those with unusual structure or content.
