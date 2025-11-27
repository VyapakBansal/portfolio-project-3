# design_project.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# Group 4
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.
import user_csv


def get_max_endagered_species(region = False, subregion = False):
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
    data = user_csv.read_csv("./data_files/Threatened_Species.csv", include_headers=False)
    for country_profile in data:
        total_species = sum(country_profile[1:])
        if total_species >= max_species:
            max_species = total_species
            countries.append(country_profile[0])
    return f"The maximum endangered species: {max_species}.\nThe countries are {", ".join([country for country in countries])}"
    

def get_population_density(country, year = '2020'):
    """Finds the population density in a given country and year 
    Parameters:
        country(str): A valid country 
        year(str): The year that to take the population data from, defaults to 2020
    Returns:
        population_density(flt): the ratio of population per square kilometer"""

def plot_pop_and_endSpec(country):
    """Plots a feature with 2 subplots, one that shows a countrys population over time and one 
        breaks down the number of endagered species in that country
    Parameters:
        country(str): A valid country
    Returns: 
        2 graphs on the same figure showing population and endagered species"""