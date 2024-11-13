# Flipper-2-HackRF

This Python script provides a utility to convert between Flipper Zero SubGHz `.sub` files and `.C16`/`.TXT` formats. The script detects the type of input file and performs the appropriate conversion, either:
- `.sub` to `.C16` and `.TXT` 
- `.C16`/`.TXT` to `.sub`.

## Features
- **Automatic Conversion**: The script detects the type of file provided (`.sub` or `.C16`/`.TXT`) and processes it accordingly.
- **Default Parameters**: If `sampling_rate` and `amplitude` are not specified, the script uses `500000` and `100` as defaults.
- **Command-Line Interface**: Provides flexibility to specify input/output files, optional parameters, and conversion details.

## Requirements
- Python 3.x
- `numpy` library

Install `numpy` via pip if it’s not already installed:
```bash
pip install numpy
