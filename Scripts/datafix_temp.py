"""
Fixing the data format in the wave file for the training of allosaurus model 
"""
import os

def process_line(line):
    parts = line.strip().split(' ')
    if len(parts) == 2:
        parts[0] = parts[0].replace('.wav', '')  # Remove .wav from the first part
    return ' '.join(parts)

def process_file(input_filename, output_filename):
    # Check if input file exists
    if not os.path.isfile(input_filename):
        print(f"Error: The file '{input_filename}' does not exist in the directory '{os.getcwd()}'.")
        return

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            processed_line = process_line(line)
            outfile.write(processed_line + '\n')

# Example usage
input_filename = 'wave'  
output_filename = 'wave_test_2k'

# Print the current working directory to ensure the script is running in the correct directory
print(f"Current working directory: {os.getcwd()}")

# Run the process
process_file(input_filename, output_filename)
