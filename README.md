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
```

## Usage

```bash
python file_converter.py --input <file> [--txt <txt_file>] [--output <output_file>] [--intermediate_freq <freq>] [--sampling_rate <rate>] [--amplitude <amplitude>]
```

### Parameters

- `--input` (required): Path to the input file. Either `.sub` for SubGHz conversion or `.C16` for binary conversion.
- `--txt`: Path to the `.TXT` file when converting `.C16` to `.sub`. Required for `.C16` to `.sub` conversions.
- `--output`: Path for the output file. If not provided, the script names the output based on the input file name.
- `--intermediate_freq`: Intermediate frequency for `.sub` to `.C16` conversion. Defaults to `5000` if not specified.
- `--sampling_rate`: Sampling rate for `.sub` to `.C16` conversion. Defaults to `500000`.
- `--amplitude`: Amplitude level for `.sub` to `.C16` conversion. Defaults to `100`.

### Examples

1. **Convert `.sub` to `.C16` and `.TXT`**
```bash
   python file_converter.py --input example.sub --output converted_example
```

2. **Convert `.C16` and `.TXT` to `.sub`**
```bash
   python file_converter.py --input example.C16 --txt example.TXT --output converted_example.sub
```

## Script Details

### Functions
- `parse_sub`: Parses a `.sub` file, extracting metadata and `RAW_Data`.
- `durations_to_bin_sequence`: Converts duration data into a binary sequence.
- `us_to_sin`: Generates I/Q values based on signal level, frequency, and amplitude.
- `sequence_to_16le_buffer`: Converts I/Q values to a 16-bit little-endian buffer.
- `write_hrf_file`: Writes `.C16` and `.TXT` files from buffer data.
- `read_txt_metadata`: Reads metadata from a `.TXT` file.
- `decode_c16_to_durations`: Decodes `.C16` I/Q data to duration-based values.
- `convert_to_sub`: Combines `.C16` and `.TXT` files into a `.sub` file.

## Notes
- The script uses default values for `sampling_rate` and `amplitude` when not provided.
- The script checks if `RAW_Data` exists in `.sub` files and uses a default sequence if it is missing.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any changes or enhancements.
