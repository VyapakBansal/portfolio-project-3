# user_csv.py
# ENDG 233 F24
# STUDENT NAME(S)
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
    with open(file_name, "r") as country_data:
        for index, line in enumerate(country_data):
            if index == 0:
                continue
            row = line.strip().split(",")
            for index, element in enumerate(row):
                if index == 3:
                    if element == '':
                        continue
                    row[3] = float(element)
            array = np.array(row , dtype=object)
            print(array)


read_csv("./data_files/Country_Data.csv")
def write_csv(filename, data, overwrite):
    """Takes a 2D list and writes it in to a CSV file

    Parameters:
    filename(str): name of the file you want to write the CSV into
    data(list): the 2D list to write into the CSV
    overwrite(bool): whether to overwrite the existing data or appending the new data"""
