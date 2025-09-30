"""
All Critical Bug Examples for Tabbed Package

Simple code to demonstrate all critical bugs found during code review.
Run each section to see the specific bug.
"""

import tempfile
import os
from tabbed.reading import Reader

# =============================================================================
# Bug #1: StopIteration Exception
# =============================================================================

content = "metadata_line\nheader,data\nvalue1,value2\n"
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
    f.write(content)
    temp_file = f.name

with open(temp_file, 'r') as infile:
    reader = Reader(infile)
    # Triggers: RuntimeError: generator raised StopIteration
    data = list(reader.read(None, None))

os.unlink(temp_file)

# =============================================================================
# Bug #2: Invalid Delimiter 
# =============================================================================

content = "A\nB\nC\nD"  # Single column data
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
    f.write(content)
    temp_file = f.name

with open(temp_file, 'r') as infile:
    reader = Reader(infile)
    # Triggers: ValueError: bad delimiter value
    data = list(reader.read(None, None))

os.unlink(temp_file)

# =============================================================================
# Bug #3: Empty File Handling
# =============================================================================

content = ""  # Empty file
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
    f.write(content)
    temp_file = f.name

with open(temp_file, 'r') as infile:
    # Triggers: RuntimeError: Types could not be determined...
    reader = Reader(infile)

os.unlink(temp_file)

# =============================================================================
# Bug #4: Metadata Boundary Detection
# =============================================================================

content = "meta1\nmeta2\nheader,col2\ndata1,val1\n"
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
    f.write(content)
    temp_file = f.name

with open(temp_file, 'r') as infile:
    reader = Reader(infile)
    # Triggers: RuntimeError: generator raised StopIteration (boundary error)
    data = list(reader.read(None, None))

os.unlink(temp_file)