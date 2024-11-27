import pandas as pd  # Importing pandas for data manipulation
import os  # Importing os for interacting with the operating system
import configparser  # Importing configparser for reading configuration files
import logging  # Importing logging for logging errors and information
from concurrent.futures import ThreadPoolExecutor  # Importing ThreadPoolExecutor for parallel processing
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Set up logging configuration
log_filename = os.path.join(logs_dir, f"{datetime.now().strftime('%Y-%m-%d')}-{datetime.now().strftime('%H-%M-%S')}.log")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename)




def read_file(file_path):
    """Read a file and return a DataFrame.
    
    Args:
        file_path (str): The path to the input file.

    Returns:
        DataFrame: A pandas DataFrame containing the data from the file.

    Raises:
        ValueError: If the file type is unsupported (not .csv or .xlsx).
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)  # Read CSV file into a DataFrame
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)  # Read Excel file into a DataFrame
    else:
        raise ValueError("Unsupported file type: {}".format(file_path))  # Raise error for unsupported file types

def save_to_csv(df, output_dir, base_filename, part_number):
    """Save DataFrame to CSV format.
    
    Args:
        df (DataFrame): The DataFrame to save.
        output_dir (str): The directory to save the CSV file.
        base_filename (str): The base name for the output file.
        part_number (int): The part number for naming the output file.
    """
    output_path = os.path.join(output_dir, f"{base_filename}_part_{part_number}.csv")  # Construct the output file path
    df.to_csv(output_path, index=False)  # Save DataFrame as CSV without the index
    logging.info(f"Saved {output_path} as CSV.")  # Log the save action

def save_to_excel(df, output_dir, base_filename, part_number):
    """Save DataFrame to Excel format.
    
    Args:
        df (DataFrame): The DataFrame to save.
        output_dir (str): The directory to save the Excel file.
        base_filename (str): The base name for the output file.
        part_number (int): The part number for naming the output file.
    """
    output_path = os.path.join(output_dir, f"{base_filename}_part_{part_number}.xlsx")  # Construct the output file path
    df.to_excel(output_path, index=False)  # Save DataFrame as Excel without the index
    logging.info(f"Saved {output_path} as Excel.")  # Log the save action

def split_file(file_path, row_limit, csv_output, excel_output, output_dir):
    """Split the input file into smaller files based on the specified row limit.
    
    Args:
        file_path (str): The path to the input file.
        row_limit (int): The maximum number of rows per split file.
        csv_output (bool): Flag to determine if CSV output is required.
        excel_output (bool): Flag to determine if Excel output is required.
        output_dir (str): The directory to save the output files.
    """
    try:
        # Check if the file is a CSV and read in chunks to handle large files
        if file_path.endswith('.csv'):
            chunks = pd.read_csv(file_path, chunksize=row_limit)  # Read the CSV file in chunks
            base_filename = os.path.splitext(os.path.basename(file_path))[0]  # Get the base filename without extension
            part_number = 1  # Initialize part number

            # Process each chunk and save as required
            for chunk in chunks:
                if csv_output:
                    save_to_csv(chunk, output_dir, base_filename, part_number)  # Save chunk as CSV if required
                if excel_output:
                    save_to_excel(chunk, output_dir, base_filename, part_number)  # Save chunk as Excel if required
                part_number += 1  # Increment part number for the next chunk

        # Check if the file is an Excel file
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)  # Read the entire Excel file into a DataFrame
            base_filename = os.path.splitext(os.path.basename(file_path))[0]  # Get the base filename without extension
            total_rows = len(df)  # Get the total number of rows in the DataFrame
            part_number = 1  # Initialize part number

            # Split the DataFrame into smaller parts based on the row limit
            for start in range(0, total_rows, row_limit):
                end = min(start + row_limit, total_rows)  # Calculate the end index for slicing
                part_df = df.iloc[start:end]  # Get the part of the DataFrame

                # Save output in CSV format if flag is set
                if csv_output:
                    save_to_csv(part_df, output_dir, base_filename, part_number)  # Save the part as CSV if required

                # Save output in Excel format if flag is set
                if excel_output:
                    save_to_excel(part_df, output_dir, base_filename, part_number)  # Save the part as Excel if required

                part_number += 1  # Increment part number for the next part

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")  # Log any errors encountered during processing

def process_file(file_path, row_limit, csv_output, excel_output, output_dir):
    """Wrapper function to process individual files with error handling.
    
    Args:
        file_path (str): The path to the input file.
        row_limit (int): The maximum number of rows per split file.
        csv_output (bool): Flag to determine if CSV output is required.
        excel_output (bool): Flag to determine if Excel output is required.
        output_dir (str): The directory to save the output files.
    """
    try:
        split_file(file_path, row_limit, csv_output, excel_output, output_dir)  # Call the split_file function
    except Exception as e:
        logging.error(f"Failed to process {file_path}: {e}")  # Log any errors encountered during file processing

def main():
    """Main function to load configuration and process files in the input directory."""
    # Load configuration
    # config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')  # Updated path
    config = configparser.ConfigParser()  # Create a ConfigParser object
    config.read(config_file_path)  # Read the configuration file
    # print(f"Config file path: {config_file_path}")
    # Extract settings from the configuration file
    input_dir = config['settings']['input_directory']  # Get the input directory
    input_dir = (os.path.join(os.path.dirname(__file__), '..', f'{input_dir}'))
    output_dir = config['settings']['output_directory']  # Get the output directory
    output_dir = (os.path.join(os.path.dirname(__file__), '..', f'{output_dir}'))
    row_limit = int(config['settings']['max_rows'])  # Get the maximum number of rows per split file
    csv_output = config.getboolean('settings', 'CSV_output')  # Get the CSV output flag
    excel_output = config.getboolean('settings', 'EXCEL_output')  # Get the Excel output flag

    # Process each file in the input directory using ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = []  # Initialize a list to keep track of future results
        for filename in os.listdir(input_dir):  # Iterate through files in the input directory
            if filename.endswith('.csv') or filename.endswith('.xlsx'):  # Check if the file is a CSV or Excel file
                file_path = os.path.join(input_dir, filename)  # Construct the full file path
                futures.append(executor.submit(process_file, file_path, row_limit, csv_output, excel_output, output_dir))  # Submit file processing to the executor
        
        # Wait for all futures to complete
        for future in futures:
            future.result()  # This will raise exceptions if any occurred in the threads

if __name__ == "__main__":
    main()  # Execute the main function when the script is run
