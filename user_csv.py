# user_csv.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# GROUP NAME
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

import numpy as np

def read_csv(file_name, include_headers = True):
    """Reads the contents of a CSV file and returns a 2D list
    
    Parameters:
    filename(str): The name of the CSV to be read
    include_headers(bool): whether or not to return the headers as part of the output, defaults to True
    Returns:
    data_list(lst): A 2D list of the CSV file, with or without headers"""
    rows = []
    with open(file_name, "r") as file:
        for index, line in enumerate(file):
            if not include_headers:
                if index == 0:
                    continue
            row = line.strip().split(",")
            for index, element in enumerate(row):
                if element.replace('-', '', 1).replace('.', '', 1).isdigit():
                    row[index] = float(element)                  
            rows.append(row)
        array = np.array(rows , dtype=object)
    return array

def write_csv(filename, data, overwrite):
    """
    Takes a 2D list and writes it into a CSV file
    Parameters:
        filename(str): name of the file you want to write the CSV into
        data(list): the 2D list to write into the CSV
        overwrite(bool): whether to overwrite the existing data or append the new data
    """

    # Check to see if we are writing or appending
    if overwrite:
        mode = "w"
    else:
        mode = "a"

    # Use context manager to ensure file is properly closed
    with open(filename, mode, newline='') as f:
        # Write each row into a csv
        for row in data:   
            # Convert each value to string and join with commas
            # Handle values that might contain commas by wrapping in quotes
            escaped_row = []
            for value in row:
                str_value = str(value)
                # If value contains comma, quote, or newline, wrap in quotes and escape quotes
                if ',' in str_value or '"' in str_value or '\n' in str_value:
                    str_value = '"' + str_value.replace('"', '""') + '"'
                escaped_row.append(str_value)
            
            f.write(','.join(escaped_row))
            f.write('\n')