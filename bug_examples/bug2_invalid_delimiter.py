"""
Bug #2: Invalid Delimiter Handling

CleverCSV returns invalid delimiters that Python's csv module cannot handle.
"""

import tempfile
import os
from tabbed.reading import Reader

# Test cases that trigger the invalid delimiter bug
test_cases = [
    "single line",
    "A\nB\nC\nD", 
    "data without delimiters\nanother line\nthird line"
]

for content in test_cases:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
        temp_file = f.name
    
    try:
        with open(temp_file, 'r') as infile:
            reader = Reader(infile)
            # This will trigger the "bad delimiter value" bug
            data = list(reader.read(None, None))
    finally:
        os.unlink(temp_file)