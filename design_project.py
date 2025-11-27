# design_project.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# Group 4
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.
import user_csv
import matplotlib as plt
import numpy as np


COUNTRY_DATA = user_csv.read_csv("./data_files/Country_Data.csv", include_headers=False)
SPECIES_DATA = user_csv.read_csv("./data_files/Threatened_Species.csv", include_headers=False)
POPULATION_DATA = user_csv.read_csv("./data_files/Population_Data.csv", include_headers=False)
def get_avg_population(region, subregion = False, year = 2020):
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
    countries = []
    # Either make a list of all countries in a region or subregion
    if not subregion:
        for row in COUNTRY_DATA:
            if row[1] == region:
                countries.append(row[0])
    else:
        for row in COUNTRY_DATA:
            if row[2] == subregion:
                countries.append(row[0])
    # Turn the year input into a useable index
    year_index = 2021 - int(year)
    # Count the total population
    total_population = 0
    for row in POPULATION_DATA:
        if row[0] in countries:
            total_population += row[year_index]
    
    # Return the average population
    avg_population = total_population / len(countries)
    return avg_population


def get_max_endagered_species(region, subregion = ''):
    """Finds the country with the highest endagered species of a region, with an optional subregion
    Parameters:
        region(str): A valid region 
        subregion(str): An optional specification for a valid sub-region 
    Returns:
        max_endagered_species(lst): a list containg the countries and it's number of endagered species""" 
    # @Matt, can you fix the docstring here to reflect this? I am not able to get the exact things to say.

    total_species = 0
    max_species = 0
    countries = []
    max_countries = []
    for region_profile in COUNTRY_DATA:
        if region == region_profile[1]:
            if subregion == region_profile[2]:
                countries.append(region_profile[0])
                continue
            countries.append(region_profile[0])
    for country_profile in SPECIES_DATA:
        if country_profile[0] in countries:
            total_species = sum(country_profile[1:])
            if total_species >= max_species:
                max_species = total_species
                max_countries.append(country_profile[0])
    # return f"The maximum endangered species: {max_species}.\nThe countries are {", ".join([country for country in countries])}"
    return max_countries, max_species


def get_population_density(country, year = 2020):
    """Finds the population density in a given country and year 
    Parameters:
        country(str): A valid country 
        year(float): The year that to take the population data from, defaults to 2020
    Returns:
        population_density(flt): the ratio of population per square kilometer"""
    population = 0
    area = 0
    for pop_profile in POPULATION_DATA:
        if country == pop_profile[0]:
            population = pop_profile[2021-year]
    for country_profile in COUNTRY_DATA:
        if country == country_profile[0]:
            area = country_profile[3]
    
    population_density = population/area
    return population_density

def annual_population_growth(country, start_year = 2000, end_year = 2020):
    """Calculates the population growth of a given country over a specified time range.
    Parameters:
        country (str): A valid country.
        start_year (float): The starting year for comparison, defaults to 2000
        end_year (float): The ending year for comparison, default to 2019
    Returns:
        growth_rate (float): The percentage change in population from start_year to end_year.
    """
    for pop_profile in POPULATION_DATA:
        if country == pop_profile[0]:
            growth = (pop_profile[2021-end_year] - pop_profile[2021-start_year])/((end_year-start_year)*pop_profile[2021-start_year])
            growth_percent = round(growth*100, 2)
    return growth_percent

def most_least_population(region, subregion=''):
    """
    Calculates the minimum and maximum population values for a given region
    (and optional subregion), and identifies the countries associated with them.
    Parameters:
        region (str): The region to search within (e.g., "Asia", "Europe").
        subregion (str): An optional subregion filter. If empty, all
                         subregions within the region are included.
    Returns:
        tuple: A tuple containing:
            min_population (float), min_country (str): The smallest population and its country.
            max_population (float), max_country (str): The largest population and its country.
    """
    countries = []
    profiles = []
    for region_profile in COUNTRY_DATA:
        if region == region_profile[1]:
            if subregion == region_profile[2]:
                countries.append(region_profile[0])
                continue
            countries.append(region_profile[0])
    for pop_profile in POPULATION_DATA:
        if pop_profile[0] in countries:
            profiles.append([pop_profile[0], pop_profile[1]])
    profiles = np.array(profiles, dtype=object)
    order = profiles[:, 1].argsort()
    sorted_profiles = profiles[order]
    maximum_populated_country = sorted_profiles[0]
    minimum_populated_country = sorted_profiles[-1]
    return maximum_populated_country, minimum_populated_country

def plot_pop_and_endSpec(country):
    """Plots a feature with 2 subplots, one that shows a countrys population over time and one 
    breaks down the number of endagered species in that country
    Parameters:
    country(str): A valid country
    population_data(array): A numpy array containing information on endagered species 
    threatened_species(array): a numpy array containing data on endagered species
    Returns: 
    2 graphs on the same figure showing population and endagered species"""
    x = np.linspace(2000,2020,21)
    for row in POPULATION_DATA:
        if row[0] == country:
            y1 = row[21:0,-1]

    plt.figure(figsize = (10,5))
    plt.subplot(1,2,1)
    plt.plot(x,y1) 
    plt.title(f"Population from 2000 to 2020 in {country}")
    plt.xlable('Year')
    plt.ylable('Population')

    for row in SPECIES_DATA:
        if row[0] == country:
            y2 = row[1:5]

    plt.bar(1,2,2)
    plt.plot(['Mammals', 'Birds', 'Fish', 'Plants'],y2) 
    plt.title(f"Number of Endagered Animals is {country}")
    plt.xlable('Species Class')
    plt.ylable('Number of Species')



"""
For note, we need to add .lower and .upper for all the case scenaraios in the 
main function when we will be returning our values, and we need to present all
the data in the form of integers.
"""

"""
Things to add.
1. Population Growth Rate ==> Done
2. Average Threatened Species Count by Region
3. Most/Least Populated Country in Each Region ==> Done 
"""