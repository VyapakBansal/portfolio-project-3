# design_project.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# GROUP NAME
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

import matplotlib as plt
import numpy as np

def get_ave_population(region, country_data, population_data, subregion = False, year = '2020'):
    """Finds the the average population of a region, with an optional subregion
    Parameters:
    region(str): A valid region 
    subregion(str): An optional specification for a valid sub-region 
    year(str): The year that to take the population data from, defaults to 2020
    country_data(array): A numpy array containing all the country data
    population_data(array): A numpy array containing information on endagered species 
    Returns:
    ave_population(flt): the average population in a region"""
    # Initiate an empty list
    countrys = []
    # Either make a list of all countrys in a region or subregion
    if not subregion:
        for row in country_data:
            if row[1] == region:
                countrys.append(row[0])
        
    else:
        for row in country_data:
            if row[2] == subregion:
                countrys.append(row[0])

    # Turn the year input into a useable index
    year_index = 2021 - int(year)
    # Count the total population
    total_population = 0
    for row in population_data:
        if row[0] in countrys:
            total_population += row[year_index]
    
    # Return the average population
    ave_population = total_population / len(countrys)
    return(ave_population)


def get_max_endagered_species(region, subregion = False):
    """Finds the country with the highest endagered species of a region, with an optional subregion
    Parameters:
    region(str): A valid region 
    subregion(str): An optional specification for a valid sub-region 
    Returns:
    max_endagered_species(lst): a list containg the country and it's number of endagered species"""

def get_population_density(country, year = '2020'):
        """Finds the population density in a given country and year 
    Parameters:
    country(str): A valid country 
    year(str): The year that to take the population data from, defaults to 2020
    Returns:
    population_density(flt): the ratio of population per square kilometer"""

def plot_pop_and_endSpec(country, population_data, threatened_species):
    """Plots a feature with 2 subplots, one that shows a countrys population over time and one 
    breaks down the number of endagered species in that country
    Parameters:
    country(str): A valid country
    population_data(array): A numpy array containing information on endagered species 
    threatened_species(array): a numpy array containing data on endagered species
    Returns: 
    2 graphs on the same figure showing population and endagered species"""
    x = np.linspace(2000,2020,21)
    for row in population_data:
        if row[0] == country:
            y1 = row[21:0,-1]

    plt.figure(figsize = (10,5))
    plt.subplot(1,2,1)
    plt.plot(x,y1) 
    plt.title(f"Population from 2000 to 2020 in {country}")
    plt.xlable('Year')
    plt.ylable('Population')

    for row in threatened_species:
        if row[0] == country:
            y2 = row[1:5]

    plt.bar(1,2,2)
    plt.plot(['Mammals', 'Birds', 'Fish', 'Plants'],y2) 
    plt.title(f"Number of Endagered Animals is {country}")
    plt.xlable('Species Class')
    plt.ylable('Number of Species')