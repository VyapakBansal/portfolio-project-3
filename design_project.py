# design_project.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# GROUP NAME
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

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

    countrys = []
    if not subregion:
        for row in country_data:
            if row[1] == region:
                countrys.append(row[0])
        
    else:
        for row in country_data:
            if row[2] == subregion:
                countrys.append(row[0])

    country_count = len(countrys)
    year_index = 2021 - int(year)
    total_population = 0
    for row in population_data:
        if row[0] in countrys:
            total_population += row[year_index]
    
    ave_population = total_population / countrys
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

def plot_pop_and_endSpec(country):
     """Plots a feature with 2 subplots, one that shows a countrys population over time and one 
        breaks down the number of endagered species in that country
    Parameters:
    country(str): A valid country
        
    Returns: 
    2 graphs on the same figure showing population and endagered species"""