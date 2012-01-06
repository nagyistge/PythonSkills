import unittest
from Skills.GameInfo import GameInfo
from Skills.Glicko.GlickoCalculator import GlickoCalculator
from Skills.Match import Match
from Skills.Matches import Matches
from Skills.Team import Team

class CalculatorTests(object):

    ERROR_TOLERANCE_TRUESKILL = 0.085
    ERROR_TOLERANCE_MATCH_QUALITY = 0.0005

    def assertRating(self, expected_mean, expected_stdev, actual):
        self.assertAlmostEqual(expected_mean, actual.mean, None,
                               "expected mean of %.14f, got %.14f" % (expected_mean, actual.mean),
                               CalculatorTests.ERROR_TOLERANCE_TRUESKILL)
        self.assertAlmostEqual(expected_stdev, actual.stdev, None,
                               "expected stdev of %.14f, got %.14f" % (expected_stdev, actual.stdev),
                               CalculatorTests.ERROR_TOLERANCE_TRUESKILL)

    def assertMatchQuality(self, expected_match_quality, actual_match_quality):
        #self.assertEqual(expected_match_quality, actual_match_quality, "expected match quality of %f, got %f" % (expected_match_quality, actual_match_quality))
        self.assertAlmostEqual(expected_match_quality, actual_match_quality, None,
                               "expected match quality of %.15f, got %.15f" % (expected_match_quality, actual_match_quality),
                               CalculatorTests.ERROR_TOLERANCE_MATCH_QUALITY)

class GlickoTests(unittest.TestCase, CalculatorTests):

    def setUp(self):
        self.calculator = GlickoCalculator()

    def test_one_on_one(self):
        game_info = GameInfo()

        player1 = Team({1: (1500, 200)})
        player2 = Team({2: (1400, 30)})
        player3 = Team({3: (1550, 100)})
        player4 = Team({4: (1700, 300)})

        matches = Matches([Match([player1, player2], [1, 2]),
                           Match([player1, player3], [2, 1]),
                           Match([player1, player4], [2, 1])])

        new_ratings = self.calculator.calculate_new_ratings(game_info, matches, 1)

        #self.assertMatchQuality(1.0, self.calculator.calculate_match_quality(game_info, matches))

        self.assertRating(1464.1, 151.4, new_ratings.rating_by_id(1))

if __name__ == "__main__":
    unittest.main()
