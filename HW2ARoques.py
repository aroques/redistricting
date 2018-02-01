'''

Name: Alec Roques
Date: 01/27/2018
Course: 4500 - Intro to the Software Profession (T/TH @ 12:30p)
Version: 1
Purpose/Description:  25 voters (15 green and 10 purple party) are ramdomly spread across 5 districts 
    with 5 voters in each district. Which party wins each district? Which party wins each redistricting?
    This program provides simulates 1,000,000 redistrictings and prints the statistics.
External files: HW2output.txt (the text-file that the results of the 1,000,000 redistrictings are written to)
Sources: python3 documentation

'''

import random, time

start_time = time.time()

NUM_VOTERS = 25
NUM_REDISTRICTINGS = 1000000

def main():
   
    vs = VoterStatistician()

    for i in range(0, NUM_REDISTRICTINGS):
        voters = Voters()
        
        for j in range(0, NUM_VOTERS):
            voter = Voter()
            voters.add_voter(voter)
        
        vs.log_statistics(voters)

    vs.print_statistics()

class MaxError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Party:
    def __init__(self, color, max_count):
        self.color = color
        self.max_count = max_count
        self.count = 0

    def __repr__(self):
        return self.color

class Parties:
    def __init__(self):
        self.party_color = ['green', 'purple']
        self.max_count  = [15, 10]
        self.parties = []

        for i in range(len(self.party_color)):
            self.parties.append(Party(self.party_color[i], self.max_count[i]))
    
    def get_random_party(self):
        """ Returns a random party - purple or green """
        if(all(party.count == party.max_count for party in self.parties)):
            raise MaxError("Each party has the maximum number of voters", self.parties)

        while(True):

            party = random.choice(self.parties)
    
            if party.count < party.max_count:
                party.count += 1
                return party
            else:
                self.parties.remove(party)


class Districts:
    def __init__(self):
        self.MAX_VOTER_PER_DISTRICT = 5
        self.NUM_DISTRICTS = 5
        self.count = dict.fromkeys(range(1,6), 0)
        self.choices = list(range(1, self.NUM_DISTRICTS+1))

    def get_random_district(self):
        """ Returns a random district - 1, 2, 3, 4, 5 """
        while (True):
            
            if(all(district_cnt == self.MAX_VOTER_PER_DISTRICT for district_cnt in self.count.values())):
                raise MaxError("Each district has the maximum number of voters")
            
            district = random.choice(self.choices)

            if self.count[district] < self.MAX_VOTER_PER_DISTRICT:
                self.count[district] += 1
                return district
            else:
                self.choices.remove(district)

class Voters:
    def __init__(self):
        self.parties = Parties()
        self.districts = Districts()
        self.voters = []
        self.voter_count = 0
    
    def add_voter(self, v):
        """ Adds a voter to voters list """
        v.party = self.parties.get_random_party()
        v.district = self.districts.get_random_district()
        self.voters.append(v)

class Voter:
    def __repr__(self):
        return "Voter | District: {} | Party: {}".format(self.district, self.party)

class VoterStatistician():
    def __init__(self):
        self.green_redistricting_wins = 0
        self.purple_redistricting_wins = 0
        self.total_green_district_wins = 0
        self.total_purple_district_wins = 0
        self.ratios = {}

    def log_statistics(self, voters):
        """ Logs (25) voter statistics """

        self.green_district_wins = 0
        self.purple_district_wins = 0
        
        districts = self.get_voters_by_district(voters)

        for district_num in range(len(districts)):
            party_count = self.count_party_color_in_each_district(district_num, districts)
            self.determine_district_winner(party_count)
        
        self.determine_redistrict_winner()

    def get_voters_by_district(self, voters):
        """ Returns a list of districts that contains the respective voters """ 
        districts = []
        for i in range(1, 6):
            district = list(filter(lambda x: x.district == i, voters.voters))
            districts.append(district)
        return districts

    def count_party_color_in_each_district(self, district_num, districts):
        """ Counts how many of each party there is per district """
        party_count = {}
        party_count['green'] = 0
        party_count['purple'] = 0   

        for voter_num in range(len(districts[district_num])):
            if districts[district_num][voter_num].party.color == 'green':
                party_count['green'] += 1
            else:
                party_count['purple'] += 1 
        
        return party_count

    def determine_district_winner(self, party_count):
        """ Determines which party won district """
        if party_count['green'] > party_count['purple']:
            self.green_district_wins += 1
            self.total_green_district_wins += 1
        else:
            self.purple_district_wins += 1
            self.total_purple_district_wins += 1
    
    def determine_redistrict_winner(self):
        """ Determines which party won re-districting """
        key1 = self.green_district_wins
        key2 = self.purple_district_wins
        if (key1, key2) not in self.ratios:
            self.ratios[(key1, key2)] = 1
        else:
            self.ratios[(key1, key2)] += 1

        if self.green_district_wins > self.purple_district_wins:
            self.green_redistricting_wins += 1
        else:
            self.purple_redistricting_wins += 1

    @property
    def percent_green_redistricting_wins(self):
        return (self.green_redistricting_wins / NUM_REDISTRICTINGS)

    @property
    def percent_purple_redistricting_wins(self):
        return (self.purple_redistricting_wins / NUM_REDISTRICTINGS)

    @property
    def percent_green_district_wins(self):
        return (self.total_green_district_wins / (NUM_REDISTRICTINGS * 5))
    @property
    def percent_purple_district_wins(self):
        return (self.total_purple_district_wins / (NUM_REDISTRICTINGS * 5))

    def print_statistics(self):
        """ Prints statistics and writes statistics to output file """
        out = '\n'
        out += '{:>50}'.format('----- Redistrict Win Ratio Stats -----\n')
        out += '{:<15} {:<15} {:<15} {:<15}\n'.format('Winner', 'Green wins', 'Purple wins', 'Pct times occured')
        for key, value in self.ratios.items():
            if key[0] > key[1]:
                winner = 'Green'
            else:
                winner = 'Purple'
            out += '{:<15} {:<15} {:<15} {:<15.2%}\n'.format(winner, key[0], key[1], value/NUM_REDISTRICTINGS)
        out += '\n'
        out += '{:>35}'.format('-------- Percent Win Stats ---------\n')
        out += '{:<10} {:>25}\n'.format('', 'Pct Redistrictings Won')#, 'Pct Districts Won')
        out += '{0:<10} {1:>25.2%}\n'.format('Green', self.percent_green_redistricting_wins)#, self.percent_green_district_wins)
        out += '{0:<10} {1:>25.2%}\n'.format("Purple", self.percent_purple_redistricting_wins)#, self.percent_purple_district_wins)
        print(out)

        with open('HW2output.txt', 'w') as f:
            f.write(out)

if __name__ == '__main__':
    main()