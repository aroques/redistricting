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

NUM_RUNS = 50000000

def main():

    redistricting_stats = {}
    voter_parties = get_voter_parties()
    district_scheme = get_district_scheme()
    district_coordinates = get_district_coordinates()

    # Test run
    start_coord = (0,0)
    neighbors = []
    neighbors.append(start_coord)
    if has_five_neighbours(neighbors, district_scheme, start_coord):
        print("Found a contiguous district!")
        district_stats = get_district_stats(district_scheme, voter_parties)
        update_redistricting_stats(redistricting_stats, district_stats)
        num_contiguous = 1
    
    # Now loop
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
            print("Found a contiguous district!")
            district_stats = get_district_stats(district_scheme, voter_parties)
            num_contiguous += 1
            update_redistricting_stats(redistricting_stats, district_stats)
        
        if i % 10000000 == 0 and i != 0:
            print("10,000,000 runs")
            
    print_redistricting_stats(redistricting_stats, num_contiguous)

def get_district_stats(district_scheme, voter_parties):
    """ Returns statistics of how many of each party each district contains """
    d_stats = {key: {'G': 0, 'P': 0} for key in range(1, 6)}
    for i, district in enumerate(district_scheme):
        for j, district_num in enumerate(district):
            party = voter_parties[i][j]
            d_stats[district_num][party] += 1
    return d_stats

def update_redistricting_stats(redistricting_stats, district_stats):
    """ Uses districts_stats to update redistricting_stats """
    g_cnt = p_cnt = 0

    for k, v in district_stats.items():
        if v['G'] > v['P']:
            g_cnt += 1
        else:
            p_cnt += 1

    key = (g_cnt, p_cnt)

    if key not in redistricting_stats:
        redistricting_stats[key] = 1
    else:
        redistricting_stats[key] += 1

def print_redistricting_stats(redistricting_stats, num_contiguous):
    out = '\nTotal time ran: {:.2} minutes\n'.format((time.time() - start_time) / 60)
    out += 'Number of runs: {}\n\n'.format(NUM_RUNS)
    out += '{:>50}'.format('----- Redistrict Win Ratio Stats -----\n')
    out += '{:<15} {:<15} {:<15} {:<15}\n'.format('Winner', 'Green wins', 'Purple wins', 'Pct times occured')
    for k, v in redistricting_stats.items():
        if k[0] > k[1]:
            winner = 'Green'
        else:
            winner = 'Purple'
        out += '{:<15} {:<15} {:<15} {:<15.2%}\n'.format(winner, k[0], k[1], v/num_contiguous)
    print(out)
    with open('HW3output.txt', 'w') as f:
        f.write(out)

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