# user_csv.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# GROUP NAME
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

def read_csv(filename, include_headers = True):
    """Reads the contents of a CSV file and returns a 2D list
    
    Parameters:
    filename(str): The name of the CSV to be read
    include_headers(bool): whether or not to return the headers as part of the output, defaults to True
    
    Returns:
    data_list(lst): A 2D list of the CSV file, with or without headers"""


def write_csv(filename, data, overwrite):
    """Takes a 2D list and writes it in to a CSV file

    Parameters:
    filename(str): name of the file you want to write the CSV into
    data(list): the 2D list to write into the CSV
    overwrite(bool): whether to overwrite the existing data or appending the new data"""

    
    # Check to see if we are writing or appending
    if overwrite:
        f = open(filename, "w")
    else:
        f = open(filename, "a")
    # Write each row into a csv
    for row in data:   
        f.write(','.join(str(value) for value in row))
        f.write('\n')

