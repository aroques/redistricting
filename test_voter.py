import unittest
from HW2ARoques import Voter, District

class TestVoter(unittest.TestCase):

    def setUp(self):
        NUM_VOTERS = 25
        self.voters = []
        for i in range(0, NUM_VOTERS):
            voter = Voter()
            self.voters.append(voter)

    def tearDown(self):
        pass

    def test_each_district_contains_5(self):
        for district, count in District.count.items():
            self.assertEqual(count, 5)

    def test_each_voter_has_party(self):
        for voter in self.voters:
            self.assertIsNotNone(voter.party)
    
        
        # with self.assertRaises(ValueError):
        #     calc.divide(10, 0)

if __name__ == '__main__':
    unittest.main()