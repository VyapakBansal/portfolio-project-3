import user_csv
import matplotlib.pyplot as plt
import numpy as np

def get_avg_population(region, country_data, population_data, subregion=False, year=2020):
    """Finds the average population of a region, with an optional subregion
    Parameters:
        region(str): A valid region 
        subregion(str): An optional specification for a valid sub-region 
        year(int): The year to take the population data from, defaults to 2020
    Returns:
        avg_population(float): the average population in a region"""
    # Initiate an empty list
    countries = []
    # Either make a list of all countries in a region or subregion
    if not subregion:
        for row in country_data:
            if row[1] == region:
                countries.append(row[0])
    else:
        for row in country_data:
            if row[2] == subregion:
                countries.append(row[0])
    
    # Handle case where no countries found
    if len(countries) == 0:
        return 0
    
    # Turn the year input into a useable index
    year_index = 2021 - int(year)
    # Count the total population
    list_population = []
    for row in population_data:
        if row[0] in countries:
            list_population.append(row[year_index])
    
    # Return the average population
    print(list_population)
    list_population = np.array(list_population, dtype = object)
    avg_population = list_population.mean()
    return avg_population

def get_max_endagered_species(region, country_data, species_data, subregion=''):
    """Finds the country with the highest endangered species in a region, with an optional subregion
    Parameters:
        region(str): A valid region 
        subregion(str): An optional specification for a valid sub-region 
    Returns:
        tuple: (max_countries(list), max_species(int)) - list of countries and their max species count""" 
    
    max_species = 0
    countries = []
    max_countries = []
    
    # Build list of countries in the region/subregion
    for region_profile in country_data:
        if region == region_profile[1]:
            if subregion and subregion != region_profile[2]:
                continue
            countries.append(region_profile[0])
    
    # Go through species data and find the max
    for country_profile in species_data:
        if country_profile[0] in countries:
            total_species = sum(country_profile[1:])
            
            if total_species > max_species:
                max_species = total_species
                max_countries = [country_profile[0]]
            elif total_species == max_species:
                max_countries.append(country_profile[0])
    
    return max_countries, max_species


def get_population_density(country, population_data, country_data, year=2020):
    """Finds the population density in a given country and year 
    Parameters:
        country(str): A valid country 
        year(int): The year to take the population data from, defaults to 2020
    Returns:
        population_density(float): the ratio of population per square kilometer"""
    
    population = 0
    area = 0
    
    # Get the population for this year
    for pop_profile in population_data:
        if country == pop_profile[0]:
            population = pop_profile[2021-year]
            break
    
    # Get the area of the country
    for country_profile in country_data:
        if country == country_profile[0]:
            area = country_profile[3]
            break
    
    # Avoid dividing by zero if area is missing
    if area == 0:
        return 0
    
    population_density = population/area
    return population_density


def annual_population_growth(country, population_data, start_year=2000, end_year=2020):
    """Calculates the annual population growth rate of a given country over a specified time range.
    Parameters:
        country(str): A valid country.
        start_year(int): The starting year for comparison, defaults to 2000
        end_year(int): The ending year for comparison, defaults to 2020
    Returns:
        growth_rate(float): The annual percentage growth rate in population"""
    
    # Initiate a count
    growth_percent = 0
    
    # Find the growth percent
    for pop_profile in population_data:
        if country == pop_profile[0]:
            start_pop = pop_profile[2021-start_year]
            end_pop = pop_profile[2021-end_year]
            years_diff = end_year - start_year
            
            if start_pop > 0 and years_diff > 0:
                growth = (end_pop - start_pop) / (years_diff * start_pop)
                growth_percent = round(growth * 100, 2)
            break
    
    return growth_percent


def most_least_population(region, country_data, population_data, subregion=''):
    """
    Calculates the minimum and maximum population values for a given region
    (and optional subregion), and identifies the countries associated with them.
    Parameters:
        region(str): The region to search within (e.g., "Asia", "Europe").
        subregion(str): An optional subregion filter. If empty, all
                        subregions within the region are included.
    Returns:
        tuple: (min_country_data, max_country_data) where each is [country_name, population]
    """
    
    countries = []
    profiles = []
    
    # Get all countries in the region or subregion
    for region_profile in country_data:
        if region == region_profile[1]:
            if subregion and subregion != region_profile[2]:
                continue
            countries.append(region_profile[0])
    
    # Grab the 2020 population data for each country
    for pop_profile in population_data:
        if pop_profile[0] in countries:
            profiles.append([pop_profile[0], pop_profile[1]])
    
    # Sort by population to find min and max
    profiles = np.array(profiles, dtype=object)
    populations = profiles[:, 1].astype(float)

    min_idx = np.argmin(populations)
    max_idx = np.argmax(populations)
    
    return profiles[min_idx], profiles[max_idx]


# Graph plotting functions
def plot_avg_population_graph(region, country_data, population_data, subregion=False):
    """
    Plots the average population of a region/subregion over the years 2000-2020
    Parameters:
        region(str): A valid region
        subregion(str or bool): An optional subregion specification
    """
    
    years = np.arange(2000, 2021)
    avg_populations = []
    
    # Calculate average pop for each year
    for year in years:
        avg_pop = get_avg_population(region, country_data, population_data, subregion, year)
        avg_populations.append(avg_pop)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_populations, marker='o', linewidth=2, markersize=4)
    
    if subregion:
        plt.title(f'Average Population in {subregion} (2000-2020)', fontsize=14, fontweight='bold')
    else:
        plt.title(f'Average Population in {region} (2000-2020)', fontsize=14, fontweight='bold')
    
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("final_plots/avg_population.png")
    plt.show()


def plot_endangered_species_graph(region, species_data, subregion=''):
    """
    Plots a bar chart of endangered species by category for countries with max species
    Parameters:
        region(str): A valid region
        subregion(str): An optional subregion specification
    """
    
    max_countries, max_species = get_max_endagered_species(region, subregion)
    
    # Just use the first country if there's multiple with the same count
    country = max_countries[0]
    
    # Pull out the species data for this country
    species_counts = []
    for row in species_data:
        if row[0] == country:
            species_counts = row[1:5]
            break
    
    categories = ['Mammals', 'Birds', 'Fish', 'Plants']
    plt.figure(figsize=(10, 6))
    plt.bar(categories, species_counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    
    if subregion:
        plt.title(f'Endangered Species in {country} ({subregion})', fontsize=14, fontweight='bold')
    else:
        plt.title(f'Endangered Species in {country} ({region})', fontsize=14, fontweight='bold')
    
    plt.xlabel('Species Category', fontsize=12)
    plt.ylabel('Number of Endangered Species', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig("final_plots/endangered_species.png")
    plt.show()


def plot_population_density_graph(country, population_data, country_data):
    """
    Plots the population density trend for a country over years 2000-2020
    Parameters:
        country(str): A valid country name
    """
    
    years = np.arange(2000, 2021)
    densities = []
    
    # Calculate density for each year
    for year in years:
        density = get_population_density(country, population_data, country_data, year)
        densities.append(density)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, densities, marker='s', linewidth=2, markersize=4, color='#E74C3C')
    plt.title(f'Population Density Trend in {country} (2000-2020)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population Density (people/km²)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("final_plots/population_density.png")
    plt.show()


def plot_population_growth_graph(country, population_data, start_year=2000, end_year=2020):
    """
    Plots the actual population values over time for a country
    Parameters:
        country(str): A valid country name
        start_year(int): Starting year for the plot
        end_year(int): Ending year for the plot
    """
    
    # Grab population data for the country
    pop_data = []
    for pop_profile in population_data:
        if pop_profile[0] == country:
            start_index = 2021 - start_year
            end_index = 2021 - end_year
            pop_data = pop_profile[end_index:start_index+1][::-1]
            break
    
    years = np.arange(start_year, end_year + 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, pop_data, marker='o', linewidth=2, markersize=5, color='#27AE60')
    plt.title(f'Population Growth in {country} ({start_year}-{end_year})', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("final_plots/population_growth.png")
    plt.show()


def plot_min_max_population_graph(region, subregion=''):
    """
    Plots a bar chart comparing minimum and maximum population countries
    Parameters:
        region(str): A valid region
        subregion(str): An optional subregion specification
    """
    
    min_pop, max_pop = most_least_population(region, subregion)
    
    countries = [min_pop[0], max_pop[0]]
    populations = [float(min_pop[1]), float(max_pop[1])]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(countries, populations, color=['#3498DB', '#E74C3C'])
    
    if subregion:
        plt.title(f'Population Comparison in {subregion}', fontsize=14, fontweight='bold')
    else:
        plt.title(f'Population Comparison in {region}', fontsize=14, fontweight='bold')
    
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Population (2020)', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig("final_plots/min_max.png")
    plt.show()


def new_csv(country_data, species_data, population_data):
    """Creates a new combined CSV file with selected data from all three datasets"""
    # Combine data from all three arrays
    new_data = []
    headers = ['Country', 'UN Region', 'UN Sub-Region', 'Total Threatened Species', 
               'Current Population', 'Population Density']
    new_data.append(headers)
    for country_profile in country_data:
        country_name = country_profile[0]

        # Find matching species data
        species_row = None
        for species_profile in species_data:
            if species_profile[0] == country_name:
                species_row = species_profile
                break

        # Find matching population data
        pop_row = None
        for p_row in population_data:
            if p_row[0] == country_name:
                pop_row = p_row
                break

        # If we have all the data, create the combined row
        if species_row is not None and pop_row is not None:
            # Calculate total threatened species
            total_species = sum(species_row[1:5])
            # Get 2020 population
            pop_2020 = pop_row[1]
            # Calculate population density
            area = country_profile[3]
            if area == '' or area == 0 or area == None:
                continue
            pop_density = round(pop_2020/area, 2)

            # Create new row
            new_row = [
                country_name,
                country_profile[1],  # UN Region
                country_profile[2],  # UN Sub-Region
                total_species,
                pop_2020,
                pop_density
            ]
            new_data.append(new_row)
    # Convert to numpy array and add headers
    new_csv_array = np.array(new_data, dtype=object)

    # Write to CSV
    user_csv.write_csv('Combined_Data.csv', new_csv_array, True)
    print("Combined CSV file created successfully!")

def main_graph(population_data, species_data):
    """Makes a grph of total population over time and total counts for threatened species in different classes"""
    # Make a vector of all the total population in each year
    populations_slice = population_data[:, 1:]
    populations = np.sum(populations_slice, axis=0)
    x = np.arange(2020,1999,-1)
    # Make a vector of total species
    species = np.sum(species_data[:,1:], axis=0)
    x2 = ['Mammals','Birds','Fish','Plants']

    # Plot the population
    plt.subplot(1,2,1)
    plt.plot(x,populations)
    plt.title('Total Population Over Time')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Plot the threatened species
    plt.subplot(1,2,2)
    plt.bar(x2,species, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    plt.title('Total Threatened Species')
    plt.xlabel('Species Class', fontsize = 12)
    plt.ylabel('Number of Species', fontsize = 12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
   
    # Save and print the graph
    plt.savefig("final_plots/main_graph.png")
    plt.show()
