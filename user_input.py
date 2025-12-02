import numpy as np


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
