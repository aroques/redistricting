'''

Name: Alec Roques
Date: 02/03/2018
Course: 4500 - Intro to the Software Profession (T/TH @ 12:30p)
Version: 1
Purpose/Description:  25 voters (15 green and 10 purple party) are ramdomly spread across 5 districts 
    with 5 voters in each district. Which party wins each district? Which party wins each redistricting?
    This program provides simulates 1,000,000 redistrictings and prints the statistics.
External files: HW3output.txt (the text-file that the results of the 1,000,000 redistrictings are written to)
Sources: python3 documentation

'''

from random import shuffle
from itertools import product
import time

start_time = time.time()

NUM_RUNS = 1

def main():

    voter_parties = get_voter_parties()
    district_scheme = get_district_scheme()
    district_coordinates = get_district_coordinates()

    # test
    start_coord = (0,0)
    neighbors = []
    neighbors.append(start_coord)
    if has_five_neighbours(neighbors, district_scheme, start_coord):
        print("this district is contiguous")
        stats = {}
        for i, district in enumerate(district_scheme):
            for j, voter_district in enumerate(district):
                if voter_district not in stats:
                    stats[voter_district] = District()
                    stats[voter_district].add_party(voter_parties[i][j])
                else:
                    stats[voter_district].add_party(voter_parties[i][j])
        
        for k, v in stats.items():
            if v.green_count > v.purple_count:
                winner = 'green'
            else:
                winner = 'purple'
            print("District {}: Winner {} - {} green, {} purple".format(k, winner, v.green_count, v.purple_count))
                

    
    num_contiguous = 1

    for i in range(NUM_RUNS):
        shuffle(district_coordinates)
        populate_district_scheme(district_scheme, district_coordinates)
        start_coords = get_start_coords(district_scheme)
        redistricting_is_contiguous = True
        
        for start_coord in start_coords:
            neighbors = []
            neighbors.append(start_coord)
            if not has_five_neighbours(neighbors, district_scheme, start_coord):
                redistricting_is_contiguous = False
                break
        
        if redistricting_is_contiguous:
            print("this district is contiguous")
            for i, district in enumerate(district_scheme):
                for j, voter_district in enumerate(district):
                    print("voter district: {}, voter party: {}".format(voter_district, voter_parties[i][j]))

            num_contiguous += 1
    
    print("num_contiguous is {}".format(num_contiguous))

class District:
    def __init__(self):
        self.green_count = 0
        self.purple_count = 0 
    
    def add_party(self, p):
        if p == 'G':
            self.green_count += 1
        elif p == 'P':
            self.purple_count += 1

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

def get_district_coordinates():
    """ Returns a list of district coordinates (tuples) """
    return list(product(range(5), repeat=2))

def populate_district_scheme(district_scheme, coordinates):
    """ Populates district_scheme with districts using coordinates """
    district = -1
    for i, coord in enumerate(coordinates):
        if (i % 5) == 0:
            district += 1
    
        district_scheme[coord[0]][coord[1]] = district

def has_five_neighbours(neighbors, grid, coord):
    """ Returns true if start coord is in a partition (of values equal to itself) of size 5 """
    if len(neighbors) == 5:
        return True

    shifts = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    x = coord[0]
    y = coord[1]

    this_val = grid[x][y]

    found_neighbor = False
    
    # Loop through adjacent coordinates
    for shift in shifts:
        n_row = x + shift[0]
        n_col = y + shift[1]

        if (n_row < len(grid[0]) and n_row >= 0) and (n_col < len(grid) and n_col >= 0): # Bounds Check
            adjacent_val = grid[n_row][n_col]
            
            neighbor = (n_row, n_col)
            
            if (this_val == adjacent_val) and (neighbor not in neighbors):
                # We found a neighbor!
                neighbors.append(neighbor)
                found_neighbor = True
                return has_five_neighbours(neighbors, grid, neighbor)
    
    if not found_neighbor:
        return False

def get_start_coords(district_scheme):
    """ Returns a list that contains a coordinate from each district """ 
    start_coords = []
    for i in range(5):
        start_coord = get_start_coord(district_scheme, i)
        start_coords.append(start_coord)
    return start_coords

def get_start_coord(district_scheme, district_num):
    """ Returns the first coordinate from district_scheme that has a value of district_num """
    for i, district in enumerate(district_scheme):
        for j, voter in enumerate(district):
            if voter == district_num:
                return (i, j)

if __name__ == '__main__':
    main()