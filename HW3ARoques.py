'''

Name: Alec Roques
Date: 02/09/2018
Course: 4500 - Intro to the Software Profession (T/TH @ 12:30p)
Version: 1
Purpose/Description:  25 voters (15 green and 10 purple party) are ramdomly spread across 5 districts 
    with 5 voters in each district. Which party wins each district? Which party wins each redistricting?
    This program provides randomly generates redistrictings, checks if the random redistricting is contiguous 
    and if it is will log statistics of the contiguous redistricting. Final statistics will be printed when the 
    program is done running (i.e, which party won in what ratio). Ex. Green Won - 3, 2 and what percent of the 
    total did each party win. Ex. Green Won 95% of the time.

    30 contiguous districts took around 16 hours (1 billion runs).
External files: HW3output.txt (the text-file that the results of the program are written to)
Sources: python3 documentation, https://py.checkio.org/mission/count-neighbours/, 
    http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/ray.html,
    https://github.com/a1ip/checkio-1/blob/master/the%20Moore%20neighborhood.py


'''

from random import shuffle
from visualize_results import paint_results
import time
from copy import deepcopy
from getters import *

start_time = time.time()
TITLE_WIDTH = 70

def main():
    district_scheme_visualization = '{}'.format(' District Schemes '.center(TITLE_WIDTH, '-'))
    district_scheme_visualization += '\n'
    num_runs = 0
    redistricting_stats = {}
    voter_parties = get_voter_parties()
    contiguous_grids = []

    district_scheme = get_district_scheme()
    contiguous_grids.append(deepcopy(district_scheme))
    district_coordinates = get_district_coordinates()

    # Test run
    start_coord = (0, 1)

    neighbors = []
    neighbors.append(start_coord)
    if has_five_neighbours(neighbors, district_scheme, start_coord):
        print("Found a contiguous district!")
        district_scheme_visualization += get_district_scheme_visualization(district_scheme, voter_parties)
        district_stats = get_district_stats(district_scheme, voter_parties)
        update_redistricting_stats(redistricting_stats, district_stats)
        num_contiguous = 1

    contiguous_grids.append(get_another_district_scheme())

    #Now loop
    #while num_contiguous < 2:
    for _ in range(2): 
        num_runs += 1
        shuffle(district_coordinates)
        populate_district_scheme(district_scheme, district_coordinates)
        start_coords = get_start_coords(district_coordinates)
        redistricting_is_contiguous = True
        
        for j, start_coord in enumerate(start_coords):

            if j == 4:
                for row in district_scheme:
                    print(row)

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
            district_scheme_visualization += get_district_scheme_visualization(district_scheme, voter_parties)
            contiguous_grids.append(deepcopy(district_scheme))

        if num_runs % 10000000 == 0 and num_runs != 0:
            print_update(num_runs, num_contiguous)

    write_redistricting_stats(district_scheme_visualization, redistricting_stats, num_contiguous, num_runs)
    ratio_stats = get_ratio_stats(redistricting_stats, num_contiguous)
    paint_results(contiguous_grids, ratio_stats)

def print_update(num_runs, num_contiguous):
    print("Number of contiguous districts found: {}\n".format(num_contiguous))
    hours = (time.time() - start_time) / 60 / 60
    print('Time ran: {:.2} hours\n'.format(hours))
    print("Number of runs: {:,}\n".format(num_runs))

def populate_district_scheme(district_scheme, coordinates):
    """ Populates district_scheme with districts using coordinates """
    district = 1
    for i, coord in enumerate(coordinates):
        if (i != 0) and (i % 5) == 0:
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

def get_ratio_stats(redistricting_stats, num_contiguous):
    ratio = {}

    for k, v in redistricting_stats.items():
        key = (k[0], k[1])
        ratio[key] = v/num_contiguous
    
    return ratio

def write_redistricting_stats(district_scheme_visualization, redistricting_stats, num_contiguous, num_runs):
    """ Writes redistricting stats to a file """ 
    out = '\n\n'
    out += '{}'.format(' General Stats '.center(TITLE_WIDTH, '-'))
    out += '\n\n'
    out += 'Total time ran: {:.2} hours\n'.format((time.time() - start_time) / 60 / 60)
    out += 'Number of runs: {:,}\n'.format(num_runs)
    out += 'Number of contiguous redistrictings found: {}\n'.format(num_contiguous)
    out += '\n\n'
    out += '{}'.format(' Redistrict Win Ratio Stats '.center(TITLE_WIDTH, '-'))
    out += '\n\n'
    out += '{:<15} {:<15} {:<15} {:<15}\n'.format('Winner', 'Green wins', 'Purple wins', 'Pct times occured')
    for k, v in redistricting_stats.items():
        if k[0] > k[1]:
            winner = 'Green'
        else:
            winner = 'Purple'
        out += '{:<15} {:<15} {:<15} {:<15.2%}\n'.format(winner, k[0], k[1], v/num_contiguous)
    outfile = 'HW3output.txt'
    out += '\n\n'
    out += district_scheme_visualization
    with open(outfile, 'w') as f:
        f.write(out)

def get_district_scheme_visualization(grid, voters):
    """ Returns a textual visualization of the district scheme (grid) """ 
    out = ''

    WIDTH = 27

    for i in range(WIDTH):
        out += '='
    out += '\n'
    for i, row in enumerate(grid):
        out += '|'
        for j, col in enumerate(row):
            out += ' {}.{} '.format(col, voters[i][j])
        out += '|\n'

    for i in range(WIDTH):
        out += '='
    out += '\n'

    return out

if __name__ == '__main__':
    main()