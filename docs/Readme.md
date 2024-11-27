# Splitting File Tool

The **Splitting File Tool** is a Python script designed to split large CSV and Excel files into smaller, manageable parts based on a specified row limit. This tool is particularly useful for processing large datasets efficiently.

## Features

- Supports both CSV and Excel file formats.
- Configurable maximum number of rows per output file.
- Generates output in both CSV and Excel formats.
- Utilizes parallel processing for faster execution.
- Robust error handling for unsupported formats and corrupted files.

## Requirements

To run this tool, ensure you have the following installed:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- Required Python libraries:
  - `pandas`
  - `configparser`
  - `openpyxl`

You can install the required libraries using pip:

```bash
pip install pandas openpyxl
```
## Directory Structure

Before you start, ensure your project folder looks like this:
splitting_file_tool/ 
```bash
│
├── input_files/           # Place your input files here
│   ├── sample_data.csv    # Example CSV file
│   └── sample_data.xlsx   # Example Excel file
│
├── output_files/          # The output files will be saved  here
│
├── LOGS/                  # Log files will be saved here
│
├── config/                # Configuration folder
│   └── config.ini         # Configuration file for settings
│
└── src/                   # Source code folder
    └── splitter_multiple_files.py
```

## Step 1: Prepare Your Input Files
Supported File Types
Place your input files in the ```input_files directory```. The tool supports:
* CSV files (e.g., ```sample_data.csv```)

### File Names
You can use any valid file names, but it's helpful to keep them descriptive.

## Step 2: Configure the config.ini File
Open the ```config.ini``` file located in the ```config``` directory. Here’s how to set the maximum row limit for splitting your files:
``` bash
[settings]
input_directory = input_files         # Directory where input files are stored
output_directory = output_files       # Directory where output files will be saved
max_rows = 100                        # Set the maximum number of rows per output file
CSV_output = True                     # Set to True if you want CSV outputs
EXCEL_output = True                   # Set to True if you want Excel outputs
```
### Explanation of Configurations
* input_directory: This is where your input files are located. You don’t need to change this unless you move your files.
* output_directory: This is where the split output files will be saved.
* max_rows: Set this value to define the maximum number of rows you want in each split file. For example, setting it to 100 means each output file will contain up to ```100``` rows.
* CSV_output: Set to ```True``` if you want the tool to create CSV files as output.
* EXCEL_output: Set to ```True``` if you want the tool to create Excel files as output.

## Step 3: Running the Tool
Once your input files are in place and the ```config.ini``` file is configured, you can run the script:

1. Open a terminal or command prompt 
2. Navigate to the ```src``` directory.
3. Execute the following command:
``` bash
python splitter_multiple_files.py
```
After running the script, you will find the split files in the output_files directory based on your configurations.
## Example
For demonstration, I have placed sample files named  ```sample_data.csv``` in the ```input_files``` directory. After running the script, you will find the split output files in the ```output_files``` directory.

In this example, the tool generates a total of 20 output files based on the specified row limit: 10 files in CSV format and 10 files in Excel format. Each of these output files will contain the designated number of rows as specified in the configuration file.
Note : the number of files might change based on row_limit/max_row provided

## Logging
The tool generates logs that can help you track the processing of files. The log files will be saved in the ```LOGS``` directory with the format ```YYYY-MM-DD-HH-MM-SS.logs```.

## Error Handling
The tool includes error handling mechanisms to manage potential issues, such as unsupported file formats and corrupted files. Any errors encountered during processing will be logged to the console for user review.

## Contributing
Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to create an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any inquiries or support, please reach out to ```akhilharold97@gmail.com```.


