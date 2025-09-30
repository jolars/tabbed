"""
Bug #3: Empty File Handling

Type detection fails for empty files or files containing only excluded values.
"""

import tempfile
import os
from tabbed.reading import Reader

# Test cases that trigger the empty file bug
test_cases = [
    "",  # Completely empty
    "\n",  # Single newline
    "\n\n\n",  # Multiple newlines
    " \n \n \n",  # Spaces and newlines (excluded values)
    "-\nnan\nNaN",  # Only excluded values
]

for content in test_cases:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
        temp_file = f.name
    
    try:
        with open(temp_file, 'r') as infile:
            # This will trigger the type detection failure during Reader initialization
            reader = Reader(infile)
    finally:
        os.unlink(temp_file)