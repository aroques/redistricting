from itertools import product

def get_voter_parties():
    """ Returns map of voter parties """
    return [['P', 'G', 'G', 'G', 'G'],
            ['G', 'P', 'P', 'P', 'G'],  
            ['G', 'P', 'G', 'G', 'G'], 
            ['G', 'G', 'G', 'P', 'P'],
            ['P', 'G', 'P', 'G', 'P']]

def get_district_scheme():
    """ Returns contiguous district scheme """
    return [[1, 5, 5, 5, 2],
            [1, 5, 5, 2, 2],  
            [3, 1, 1, 2, 4], 
            [3, 3, 1, 2, 4],
            [3, 3, 4, 4, 4]]

def get_another_district_scheme():
    """ Returns another contiguous district scheme """
    return [[4, 1, 1, 3, 3],
            [5, 4, 1, 1, 3],  
            [5, 4, 4, 1, 3], 
            [5, 4, 2, 3, 2],
            [5, 5, 2, 2, 2]]

def get_start_coords(coordinates):
    """ Returns a list that contains a coordinate from each district """ 
    return [
        coordinates[0],
        coordinates[5],
        coordinates[10],
        coordinates[15],
        coordinates[20]
    ]

def get_district_coordinates():
    """ Returns a list of district coordinates (tuples) """
    return list(product(range(5), repeat=2))