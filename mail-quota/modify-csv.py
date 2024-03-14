import csv
import re
import sys

# Function to remove 'context*' and update first column with context id
def modify_csv(input_file, output_file):
    # Open input file for reading and output file for writing
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        # Create CSV reader and writer objects
        reader = csv.reader(infile, delimiter=',')
        writer = csv.writer(outfile, delimiter=',')

        # Loop through each row in input file
        for row in reader:
            # Initialize new row to store modified values
            new_row = []
            for col in row:
                # Check if the column matches pattern 'context*'
                if re.match(r'^context\d+$', col):
                    # If column matches pattern, skip it
                    continue
                elif col.isdigit():
                    # If column contains only numercial digits, move it to first column
                    new_row.insert(0, col)
                else:
                    # Otherwise, keep the column in its original position
                    new_row.append(col)

            # Write modified row to output file
            writer.writerow(new_row)

if __name__ == "__main__":
    # Check if correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 modify-csv.py input_file output_file")
        sys.exit(1)

    # Get input and output filenames from command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    modify_csv(input_file, output_file)

    print(f"CSV modification complete. Output written to {output_file}")
