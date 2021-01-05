#!/usr/bin/python
# -*- coding: utf8 -*-"

import unittest
import mastermind

class MasterMindTest(unittest.TestCase):

    def testCombinations3Colors0Slots(self):
        self.assertEqual(mastermind.combinations([0, 1, 2], 0), [[]])

    def testCombinations3Colors1Slot(self):
        self.assertEqual(mastermind.combinations([0, 1, 2], 1), [[0], [1], [2]])

    def testCombinations0Color0Slot(self):
        self.assertEqual(mastermind.combinations([], 0), [[]])

    def testCombinations0Color1Slot(self):
        self.assertEqual(mastermind.combinations([], 1), [])

    def testCombinations2Colors3Slots(self):
        self.assertEqual(
                sorted(mastermind.combinations([0, 1], 3)),
                [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]])

    # Property based test
    def testCombinationsNumberIsPower(self):
        for nb_colors in range(0, 8):
            for nb_slots in range(0, 4):
                self.assertEqual(len(mastermind.combinations(list(range(nb_colors)), nb_slots)), pow(nb_colors, nb_slots))

    def testScoreProposalNoCommon(self):
        self.assertEqual(mastermind.score_proposal([0, 0, 0, 0], [1, 1, 1, 1]), (0, 0))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [4, 5, 6, 7]), (0, 0))

    def testScoreProposalMisplaced(self):
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [1, 4, 5, 6]), (1, 0))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [4, 5, 1, 2]), (2, 0))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [1, 2, 3, 6]), (3, 0))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [1, 2, 3, 0]), (4, 0))

    def testScoreProposalGood(self):
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [0, 4, 5, 6]), (0, 1))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [4, 1, 2, 5]), (0, 2))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [6, 1, 2, 3]), (0, 3))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [0, 1, 2, 3]), (0, 4))

    def testScoreProposalMisplacedAndGood(self):
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [0, 4, 5, 1]), (1, 1))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [3, 1, 2, 5]), (1, 2))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [6, 1, 3, 2]), (2, 1))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [0, 1, 3, 2]), (2, 2))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [3, 1, 0, 2]), (3, 1))

    def testScoreProposalRepetitions(self):
        self.assertEqual(mastermind.score_proposal([1, 1, 2, 3], [0, 4, 1, 6]), (1, 0))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [1, 1, 5, 6]), (0, 1))
        self.assertEqual(mastermind.score_proposal([1, 1, 1, 1], [0, 1, 2, 3]), (0, 1))
        self.assertEqual(mastermind.score_proposal([0, 1, 2, 3], [1, 1, 1, 1]), (0, 1))
        self.assertEqual(mastermind.score_proposal([1, 1, 2, 3], [1, 1, 1, 1]), (0, 2))
        self.assertEqual(mastermind.score_proposal([1, 1, 2, 3], [1, 1, 3, 2]), (2, 2))

    def testScoreProposalMisc(self):
        self.assertEqual(mastermind.score_proposal([0, 4, 3, 4], [4, 3, 6, 3]), (2, 0))
        self.assertEqual(mastermind.score_proposal([0, 0, 1, 2], [3, 0, 4, 0]), (1, 1))

    def testPropsalsScoresStatsAll(self):
        colors = [0, 1, 2, 3]
        slots = 4
        result = mastermind.proposals_scores_stats_all(mastermind.combinations(colors, slots), colors, slots)
        for (prop, scores) in result.iteritems():
            # Winning always result in 1 combination being kept
            self.assertEqual(scores[(0, 4)], 1)
            # All combinations must be covered and have only one score associated
            self.assertEqual(sum(scores.values()), 256)
        #for prop in [(0, 1, 2, 3), (0, 0, 1, 2), (0, 0, 1, 1), (0, 0, 0, 1), (0, 0, 0, 0)]:
        #    print("%s => " % (prop,))
        #    for (score, nb) in scores.iteritems():
        #        print("      %s: %s" % (score, nb))
        # If only 1 of the digits is good, it leaves only 4
        # possibilities: all 0, all 1, all 2 and all 3
        self.assertEqual(result[(0, 1, 2, 3)][(0, 1)], 4)
        # 1 misplaced is not possible, it would be good as we only have 4 colors
        self.assertEqual(result[(0, 1, 2, 3)][(1, 0)], 0)
        for i in range(4):
            # Eliminating a single color keeps 3^4 possibilities
            self.assertEqual(result[(i, i, i, i)][(0, 0)], 81)
            # Confirming a given color is present somewhere keeps 4*3^3 possiblities
            self.assertEqual(result[(i, i, i, i)][(0, 1)], 108)
            # And if present twice, we have 6*3^2 possibilities
            self.assertEqual(result[(i, i, i, i)][(0, 2)], 54)
            # And if present three times, we have 4*3^1 possibilities
            self.assertEqual(result[(i, i, i, i)][(0, 3)], 12)
            # Of course only one winning combination
            self.assertEqual(result[(i, i, i, i)][(0, 4)], 1)
            # And we already checked that the total was 256, so there's nothing more

    def testPropsalsScoresStatsCandidates(self):
        colors = [0, 1, 2, 3]
        slots = 4
        # Let's only take some combinations
        candidates = [c for c in mastermind.combinations(colors, slots) if c[0] == 0 and c[1] == c[2]]
        result = mastermind.proposals_scores_stats_candidates(candidates)
        for (prop, scores) in result.iteritems():
            # Winning always result in 1 combination being kept
            self.assertEqual(scores[(0, 4)], 1)
            # All combinations must be covered and have only one score associated
            self.assertEqual(sum(scores.values()), len(candidates))
        #for prop in [(0, 1, 2, 3), (0, 0, 1, 2), (0, 0, 1, 1), (0, 0, 0, 1), (0, 0, 0, 0)]:
        #    print("%s => " % (prop,))
        #    for (score, nb) in scores.iteritems():
        #        print("      %s: %s" % (score, nb))
        # We can't have score = (0, 0) as we know the first digit is 0.
        self.assertEqual(result[(0, 0, 0, 0)][(0, 0)], 0)
        # If only 1 of the digits is good, it's necessarly the 0 so it
        # eliminates combinations containing 0 in other digits. It leaves
        # 9 possibilities: (1,2 or 3) for digits 2 & 3 and (1, 2 or 3) for
        # digits 4.
        self.assertEqual(result[(0, 0, 0, 0)][(0, 1)], 9)
        # If 2 digits are good, it's necessarly the first and last so it
        # eliminates combinations containing 0 in digits 2 & 3. It leaves
        # 3 possibilities (the 3 possible digits for 2&3).
        self.assertEqual(result[(0, 0, 0, 0)][(0, 2)], 3)
        # Similarly: digits 1, 2 and 3 are 0, last one can be (1, 2 or 3)
        self.assertEqual(result[(0, 0, 0, 0)][(0, 3)], 3)

    def testPropsalsEliminationExpectation(self):
        colors = list(range(4))
        slots = 4
        result = mastermind.proposals_elimination_expectation(mastermind.combinations(colors, slots), colors, slots, False)
        #max_k, max_v = None, None
        #for (k, v) in result.iteritems():
        #    if v is None or v > max_v:
        #        max_k, max_v = k, v
        #    print("%s -> %s" % (k, v))
        #print("Max: %s -> %s" % (max_k, max_v))

    def testPickCombinationsNoColor(self):
        result = mastermind.pick_combination([], 4)
        self.assertEqual(result, [])

    def testPickCombinations(self):
        for nb_slots in range(8):
            for nb_colors in range(1, 8):
                colors = list(range(nb_colors))
                result = mastermind.pick_combination(colors, nb_slots)
                self.assertEqual(len(result), nb_slots)
                for c in result:
                    self.assertIn(c, colors)


if __name__ == '__main__':
    unittest.main()
