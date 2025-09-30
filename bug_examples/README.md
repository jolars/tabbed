# Tabbed Package - Critical Bug Examples

This directory contains minimal code examples that demonstrate critical bugs found in the tabbed package during JOSS review.

## Files

- `bug1_stopiteration.py` - StopIteration exception when file pointer exceeds file length
- `bug2_invalid_delimiter.py` - "bad delimiter value" error from invalid delimiters  
- `bug3_empty_file.py` - Type detection failure for empty files
- `bug4_metadata_boundary.py` - Metadata boundary detection errors
- `all_bugs.py` - All bugs in one file for easy testing

## Usage

Run any file interactively in Python:

```python
exec(open('bug1_stopiteration.py').read())
```

Or copy/paste the code sections into a Python REPL.

## Expected Errors

1. **Bug #1**: `RuntimeError: generator raised StopIteration`
2. **Bug #2**: `ValueError: bad delimiter value`  
3. **Bug #3**: `RuntimeError: Types could not be determined as last 20 polling rows...`
4. **Bug #4**: `RuntimeError: generator raised StopIteration` (boundary error)

These represent critical failures that should be addressed before publication.