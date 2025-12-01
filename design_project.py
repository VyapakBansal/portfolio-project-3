# design_project.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# Group 4
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.
import user_csv
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV files and save as numpy arrays
COUNTRY_DATA = user_csv.read_csv("./data_files/Country_Data.csv", include_headers=False)
SPECIES_DATA = user_csv.read_csv("./data_files/Threatened_Species.csv", include_headers=False)
POPULATION_DATA = user_csv.read_csv("./data_files/Population_Data.csv", include_headers=False)

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
    total_population = 0
    for row in population_data:
        if row[0] in countries:
            total_population += row[year_index]

    
    # Return the average population
    total_population = np.array(total_population, dtype = object)
    avg_population = total_population.mean()
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
    order = profiles[:, 1].argsort()
    sorted_profiles = profiles[order]
    
    minimum_populated_country = sorted_profiles[0]
    maximum_populated_country = sorted_profiles[-1]
    
    return minimum_populated_country, maximum_populated_country


# Graph plotting functions
def plot_avg_population_graph(region, subregion=False):
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
        avg_pop = get_avg_population(region, subregion, year)
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
    plt.show()


def plot_population_density_graph(country):
    """
    Plots the population density trend for a country over years 2000-2020
    Parameters:
        country(str): A valid country name
    """
    
    years = np.arange(2000, 2021)
    densities = []
    
    # Calculate density for each year
    for year in years:
        density = get_population_density(country, year)
        densities.append(density)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, densities, marker='s', linewidth=2, markersize=4, color='#E74C3C')
    plt.title(f'Population Density Trend in {country} (2000-2020)', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population Density (people/km²)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
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
    population_data = []
    for pop_profile in population_data:
        if pop_profile[0] == country:
            start_index = 2021 - start_year
            end_index = 2021 - end_year
            population_data = pop_profile[end_index:start_index+1][::-1]
            break
    
    years = np.arange(start_year, end_year + 1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, population_data, marker='o', linewidth=2, markersize=5, color='#27AE60')
    plt.title(f'Population Growth in {country} ({start_year}-{end_year})', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
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
            if area == '':
                continue
            pop_density = pop_2020 / area

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

    # Create headers


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


def get_sub_regions(region, country_data):
    """Gets all unique subregions within a region
    Parameters:
        region(str): A valid region name
    Returns:
        subregions(numpy.ndarray): Array of unique subregion names"""
    # Initiate empty list
    subregions = []
    # Find unique subregions
    for country_profile in country_data:
        if country_profile[1] == region:
            subregions.append(country_profile[2])
    subregions = np.unique(subregions)
    return subregions


def get_user_region(regions):
    """Prompts user for a valid region name
    Parameters:
        regions(numpy.ndarray): Array of valid region names
    Returns:
        region(str): A valid region selected by the user"""
    
    # Print all the available regions and get input
    while True:
        print('\nAvailable regions:', ', '.join(regions))
        region = input('Please enter the region: ').strip().title()

        # Check if valid region
        if region in regions:
            return region
        else:
            print('Invalid region. Please try again.')


def get_user_subregions(subregions):
    """Prompts user for a valid subregion name
    Parameters:
        subregions(numpy.ndarray): Array of valid subregion names
    Returns:
        subregion(str): A valid subregion selected by the user"""
    # Gets subregion input
    while True:
        subregion = input('Please enter the subregion: ').strip().title()

        # Verify it is valid
        if subregion in subregions:
            return subregion
        else:
            print('Invalid subregion. Please try again.')


def get_user_country(all_countries):
    """Prompts user for a valid country name
    Parameters:
        all_countries(numpy.ndarray): Array of all valid country names
    Returns:
        country(str): A valid country selected by the user"""
    
    # Get input for country selection and verify its valid
    while True:
        print('\nAvailable countries:', ', '.join(all_countries[:10]), '... (and more)')
        country = input('Please enter the country name: ').strip().title()

        if country in all_countries:
            return country
        else:
            print('Invalid country. Please try again.')


# Main function
def main(country_data, population_data, species_data):
    """Main function that provides a menu-driven interface for data analysis"""
    
    # Get all unique regions from the data
    regions = np.unique(country_data[:, 1])
    
    while True:
        # Show the menu
        print('\n' + '='*60)
        print('Welcome to our data analysis tool!')
        print('='*60)
        print('What data would you like to access?:')
        print('1) Average Population')
        print('2) Highest Threatened Species')
        print('3) Population Density')
        print('4) Population Growth')
        print('5) Maximum and Minimum Populations')
        print('0) End Program')
        print('='*60)
        
        menu_option = input('>> ')
        
        # Average population option
        if menu_option == '1':
            region = get_user_region(regions)
            
            # Get all subregions in this region
            subregions = get_sub_regions(region, country_data)
            # See if they want to narrow it down to a subregion
            print(f'\nAvailable subregions in {region}:', ', '.join(subregions))
            use_subregion = input('Would you like to filter by subregion? (yes/no): ').strip().lower()
            
            if use_subregion == 'yes':
                subregion = get_user_subregions(subregions)
                
                year = input('Enter year (2000-2020, default 2020): ').strip() or '2020'
                avg_pop = get_avg_population(region, country_data, population_data, subregion, int(year))
                print(f'\nAverage population in {subregion} ({year}): {avg_pop:,.2f}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_avg_population_graph(region, subregion)
            else:
                year = input('Enter year (2000-2020, default 2020): ').strip() or '2020'
                avg_pop = get_avg_population(region, country_data, population_data, False, int(year))
                print(f'\nAverage population in {region} ({year}): {avg_pop:,.2f}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_avg_population_graph(region)
        
        # Threatened species option
        elif menu_option == '2':
            region = get_user_region(regions)
            
            # Get all subregions in this region
            subregions = get_sub_regions(region, country_data)
            
            # Checking if they want to narrow it down to a subregion
            print(f'\nAvailable subregions in {region}:', ', '.join(subregions))
            use_subregion = input('Would you like to filter by subregion? (yes/no): ').strip().lower()
            
            if use_subregion == 'yes':
                # Keep asking until we get a valid subregion
                subregion = get_user_subregions(subregions)
                max_countries, max_species = get_max_endagered_species(region, country_data, subregion)
                print(f'\nMaximum endangered species count: {max_species}')
                print(f'Country(ies) with highest count: {", ".join(max_countries)}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_endangered_species_graph(region, species_data, subregion)
            else:
                max_countries, max_species = get_max_endagered_species(region, country_data, species_data)
                print(f'\nMaximum endangered species count: {max_species}')
                print(f'Country(ies) with highest count: {", ".join(max_countries)}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_endangered_species_graph(region, species_data)
        
        # Population density option
        elif menu_option == '3':
            all_countries = country_data[:, 0]
            
            # Keep asking until we get a valid country
            country = get_user_country(all_countries)
            year = input('Enter year (2000-2020, default 2020): ').strip() or '2020'
            density = get_population_density(country, population_data, country_data, int(year))
            print(f'\nPopulation density in {country} ({year}): {density:,.2f} people per km²')
            
            show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
            if show_graph == 'yes':
                plot_population_density_graph(country)
        
        # Population growth option
        elif menu_option == '4':
            all_countries = country_data[:, 0]
            
            # Keep asking until we get a valid country
            country = get_user_country(all_countries)
            
            start_year = input('Enter start year (2000-2020, default 2000): ').strip() or '2000'
            end_year = input('Enter end year (2000-2020, default 2020): ').strip() or '2020'
            
            growth = annual_population_growth(country, population_data, int(start_year), int(end_year))
            print(f'\nAnnual population growth rate in {country} ({start_year}-{end_year}): {growth}%')
            
            show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
            if show_graph == 'yes':
                plot_population_growth_graph(country, population_data, int(start_year), int(end_year))
        
        # Min/Max population option
        elif menu_option == '5':
            region = get_user_region(regions)
            
            # Get all subregions in this region
            subregions = get_sub_regions(region)
            # See if they want to narrow it down to a subregion
            print(f'\nAvailable subregions in {region}:', ', '.join(subregions))
            use_subregion = input('Would you like to filter by subregion? (yes/no): ').strip().lower()
            
            if use_subregion == 'yes':
                # Keep asking until we get a valid subregion
                subregion = get_user_subregions(subregions)
                
                min_pop, max_pop = most_least_population(region, country_data, population_data, subregion)
                print(f'\nMinimum population: {min_pop[0]} with {float(min_pop[1]):,.0f} people')
                print(f'Maximum population: {max_pop[0]} with {float(max_pop[1]):,.0f} people')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_min_max_population_graph(region, subregion)
            else:
                min_pop, max_pop = most_least_population(region, country_data, population_data, '')
                print(f'\nMinimum population: {min_pop[0]} with {float(min_pop[1]):,.0f} people')
                print(f'Maximum population: {max_pop[0]} with {float(max_pop[1]):,.0f} people')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_min_max_population_graph(region, '')
        
        # Exit option
        elif menu_option == '0':
            print('\nThank you for using our data analysis tool. Goodbye!')
            break
        
        # Invalid input
        else:
            print('\nInput not recognized. Please try again.')

new_csv(COUNTRY_DATA, SPECIES_DATA, POPULATION_DATA)
# Run the program
if __name__ == "__main__":
    main_graph(POPULATION_DATA, SPECIES_DATA)
    main(COUNTRY_DATA, POPULATION_DATA, SPECIES_DATA)