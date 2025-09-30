"""
Bug #1: StopIteration Exception in File Reading

Creates a file where metadata detection fails and computes an autostart
position beyond the file length, causing StopIteration.
"""

import tempfile
import os
from tabbed.reading import Reader

# Create test file content that triggers the bug
test_content = "metadata_line\nheader,data\nvalue1,value2\n"

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
    f.write(test_content)
    temp_file = f.name

try:
    with open(temp_file, 'r') as infile:
        reader = Reader(infile)
        # This will trigger the StopIteration bug
        data = list(reader.read())
finally:
    os.unlink(temp_file)
