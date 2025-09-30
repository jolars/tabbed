"""
Bug #4: Metadata Boundary Detection Error

Metadata detection incorrectly computes the data start position,
leading to reading from wrong positions or beyond file length.
"""

import tempfile
import os
from tabbed.reading import Reader

# Test cases that trigger metadata boundary detection issues
test_cases = [
    "metadata1\nmetadata2\nheader,col2\ndata1,val1\ndata2,val2\n",
    "key:value\nother:data\ncol1,col2\nval1,val2\n", 
    "single_metadata_line\ncol1,col2\nval1,val2\n",
]

for content in test_cases:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
        temp_file = f.name
    
    try:
        with open(temp_file, 'r') as infile:
            reader = Reader(infile)
            # This will trigger the boundary bug (StopIteration or wrong data)
            data = list(reader.read(None, None))
    finally:
        os.unlink(temp_file)