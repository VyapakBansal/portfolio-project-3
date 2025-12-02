# design_project.py
# ENDG 233 F24
# Matthew Guillaume, Vyapak Bansal
# Group 4
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.
import user_csv
import numpy as np
from analysis import *
from user_input import *
# Read the CSV files and save as numpy arrays
COUNTRY_DATA = user_csv.read_csv("./data_files/Country_Data.csv", include_headers=False)
SPECIES_DATA = user_csv.read_csv("./data_files/Threatened_Species.csv", include_headers=False)
POPULATION_DATA = user_csv.read_csv("./data_files/Population_Data.csv", include_headers=False)

# Main function
def main(country_data, population_data, species_data):
    """Main function that provides a menu-driven interface for data analysis
    Parameters:
        country_data(ndarray): An array of country data
        population_data(ndarray): An array of population data
        species_data(ndarray): An array of threatened species data"""
    
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
                    plot_avg_population_graph(region, country_data, population_data, subregion)
            else:
                year = input('Enter year (2000-2020, default 2020): ').strip() or '2020'
                avg_pop = get_avg_population(region, country_data, population_data, False, int(year))
                print(f'\nAverage population in {region} ({year}): {avg_pop:,.2f}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_avg_population_graph(region, country_data, population_data)
        
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
                max_countries, max_species = get_max_endangered_species(region, country_data, species_data, subregion)
                print(f'\nMaximum endangered species count: {max_species}')
                print(f'Country(ies) with highest count: {", ".join(max_countries)}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_endangered_species_graph(region, country_data, species_data, subregion)
            else:
                max_countries, max_species = get_max_endangered_species(region, country_data, species_data)
                print(f'\nMaximum endangered species count: {max_species}')
                print(f'Country(ies) with highest count: {", ".join(max_countries)}')
                
                show_graph = input('\nWould you like to see a graph? (yes/no): ').strip().lower()
                if show_graph == 'yes':
                    plot_endangered_species_graph(region, country_data, species_data)
        
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
                plot_population_density_graph(country, population_data, country_data)
        
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
            subregions = get_sub_regions(region, country_data)
            # See if they want to narrow it down to a subregion
            print(f'\nAvailable subregions in {region}:', ', '.join(subregions))
            use_subregion = input('Would you like to filter by subregion? (yes/no): ').strip().lower()
            if most_least_population(region, country_data, population_data, subregion) == None:
                print("No data found for the same.")
            
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
                min_pop, max_pop = most_least_population(region, country_data, population_data)
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


# Run the program
if __name__ == "__main__":
    main(COUNTRY_DATA, POPULATION_DATA, SPECIES_DATA)
    new_csv(COUNTRY_DATA, SPECIES_DATA, POPULATION_DATA)
    main_graph(POPULATION_DATA, SPECIES_DATA)