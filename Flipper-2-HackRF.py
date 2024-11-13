import argparse
import os
import struct
import numpy as np

def parse_args():
    """Parse command-line arguments with default values if arguments are omitted."""
    parser = argparse.ArgumentParser(description="Convert between .sub and .C16/.TXT formats automatically.")
    parser.add_argument("--input", required=True, help="Input file path (.sub or .C16)")
    parser.add_argument("--txt", help="Optional .TXT file for .C16 to .sub conversion")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--intermediate_freq", type=int, help="Intermediate frequency for .sub to .C16 conversion", default=5000)
    parser.add_argument("--sampling_rate", type=int, help="Sampling rate (default: 500000)", default=500000)
    parser.add_argument("--amplitude", type=int, help="Amplitude (default: 100)", default=100)
    return parser.parse_args()

def parse_sub(file_path):
    """Parse .sub file and extract metadata and RAW_Data."""
    metadata = {}
    chunks = []
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                if ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key == "raw_data":
                        chunks = [[int(x) for x in value.split()]]
                    else:
                        metadata[key] = value
        if not chunks:
            print("No RAW_Data found. Using default duration sequence.")
            chunks = [[100, 200, 300, 400, 500]]
    except FileNotFoundError:
        raise Exception("Cannot read .sub file.")
    metadata["chunks"] = chunks
    return metadata

def durations_to_bin_sequence(durations, sampling_rate, intermediate_freq, amplitude):
    sequence = []
    for duration in durations:
        level = duration > 0
        duration = abs(duration)
        sequence.extend(us_to_sin(level, duration, sampling_rate, intermediate_freq, amplitude))
    return sequence

def us_to_sin(level, duration, sampling_rate, intermediate_freq, amplitude):
    iterations = int(sampling_rate * duration / 1_000_000)
    data_step = 2 * np.pi / (sampling_rate / intermediate_freq)
    amplitude_scale = (256**2 - 1) * (amplitude / 100)
    if level:
        return [[int(np.cos(i * data_step) * (amplitude_scale / 2)), int(np.sin(i * data_step) * (amplitude_scale / 2))] for i in range(iterations)]
    else:
        return [[0, 0] for _ in range(iterations)]

def sequence_to_16le_buffer(sequence):
    buffer = bytearray()
    for i, q in sequence:
        buffer.extend(struct.pack('<h', i))
        buffer.extend(struct.pack('<h', q))
    return buffer

def write_hrf_file(output_path, buffer, frequency, sampling_rate):
    output_c16 = f"{output_path}.C16"
    output_txt = f"{output_path}.TXT"
    with open(output_c16, 'wb') as file:
        file.write(buffer)
    with open(output_txt, 'w') as file:
        file.write(f"sample_rate={sampling_rate}\n")
        file.write(f"center_frequency={frequency}")
    return [output_c16, output_txt]

def read_txt_metadata(txt_file_path):
    """Read frequency and sample rate from .TXT file."""
    metadata = {}
    with open(txt_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            metadata[key] = int(value)
    return metadata

def decode_c16_to_durations(c16_file_path):
    """Decode .C16 file to a list of timing durations."""
    durations = []
    with open(c16_file_path, 'rb') as file:
        while True:
            iq_pair = file.read(4)
            if not iq_pair:
                break
            i, q = struct.unpack('<hh', iq_pair)
            amplitude = int(np.sqrt(i**2 + q**2))
            durations.append(amplitude)
    return durations

def convert_to_sub(c16_file_path, txt_file_path, output_path):
    """Convert .C16 and .TXT files to .sub format."""
    metadata = read_txt_metadata(txt_file_path)
    frequency = metadata.get('center_frequency', 0)
    sampling_rate = metadata.get('sample_rate', 500000)
    durations = decode_c16_to_durations(c16_file_path)
    with open(output_path, 'w') as file:
        file.write(f"Filetype: Flipper SubGhz RAW File\n")
        file.write(f"Version: 1\n")
        file.write(f"Frequency: {frequency}\n")
        file.write(f"Preset: FuriHalSubGhzPresetOok650Async\n")
        file.write(f"Protocol: RAW\n")
        file.write("RAW_Data: ")
        file.write(" ".join(map(str, durations)))
    print(f"Converted to .sub format: {output_path}")

def main():
    args = parse_args()

    input_ext = os.path.splitext(args.input)[1].lower()
    sampling_rate = args.sampling_rate
    amplitude = args.amplitude

    if input_ext == ".sub":
        print("Converting .sub to .C16 and .TXT format...")
        parsed_metadata = parse_sub(args.input)
        sequence = parsed_metadata["chunks"][0] if parsed_metadata["chunks"] else []
        buffer = sequence_to_16le_buffer(
            durations_to_bin_sequence(
                sequence,
                sampling_rate,
                args.intermediate_freq,
                amplitude
            )
        )
        output_path = args.output or os.path.splitext(args.input)[0]
        write_hrf_file(output_path, buffer, parsed_metadata.get("frequency", "0"), sampling_rate)
    elif input_ext == ".c16" and args.txt:
        print("Converting .C16 and .TXT to .sub format...")
        output_path = args.output or os.path.splitext(args.input)[0]
        convert_to_sub(args.input, args.txt, output_path)
    else:
        print("Invalid input. Please provide either a .sub file or both .C16 and .TXT files for conversion.")

if __name__ == "__main__":
    main()