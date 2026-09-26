import unittest
from collections import Counter
from game import Game, beats, classify, strength

class RulesTests(unittest.TestCase):
    def test_rank_suit_pair(self):
        self.assertGreater(strength(0), strength(51))
        self.assertTrue(beats([7], [6]))
        self.assertFalse(beats([4,8], [5,6]))
        self.assertTrue(beats([0,1], [48,51]))

    def test_taiwan_straights(self):
        wheel=[48,0,5,10,15]
        normal=[4,9,14,19,20]
        biggest=[0,5,10,15,16]
        self.assertTrue(beats(normal,wheel))
        self.assertTrue(beats(biggest,normal))
        self.assertIsNone(classify([0,36,41,46,51]))

    def test_house_rules_and_bombs(self):
        straight=[4,9,14,19,20]
        house=[8,9,10,12,13]
        bomb=[16,17,18,19,24]
        flush=[4,8,12,16,20]
        self.assertFalse(beats(house,straight))
        self.assertFalse(beats(straight,house))
        self.assertTrue(beats(bomb,house))
        self.assertTrue(beats(flush,bomb))
        self.assertTrue(beats(bomb,[3]))
        self.assertTrue(beats(flush,[0,1]))
        self.assertFalse(beats(house,[3]))
        self.assertIsNone(classify([4,5,6]))
        self.assertIsNone(classify([4,12,24,32,44]))
        self.assertIsNone(classify([4,4]))
        self.assertIsNone(classify([-1]))
        self.assertEqual(classify(list(range(0,52,4)))[0],11)
        self.assertEqual(classify([4*r+r%4 for r in range(13)])[0],10)

    def test_opening_and_pass_reset(self):
        g=Game(7)
        owner=g.turn
        self.assertFalse(g.pass_turn())
        self.assertFalse(g.play([next(c for c in g.hands[owner] if c!=4)]))
        self.assertTrue(g.play([4]))
        for _ in range(3):self.assertTrue(g.pass_turn())
        self.assertEqual(g.turn,owner)
        self.assertEqual(g.table,[])
        self.assertFalse(g.passed)

    def test_withdrawal(self):
        g=Game(0)
        g.hands=[[4,20],[8,24],[12,28],[16,32]]
        g.turn=g.owner=0
        g.play([4]);g.pass_turn()
        self.assertEqual(g.turn,2)
        g.play([12]);g.pass_turn();g.pass_turn()
        self.assertEqual(g.turn,2)
        self.assertFalse(g.table)

    def test_complete_games(self):
        for seed in range(40):
            g=Game(seed)
            for turn in range(300):
                if g.winner is not None:break
                cards=g.suggest()
                self.assertTrue(g.play(cards) if cards else g.pass_turn())
                all_cards=g.played+[c for hand in g.hands for c in hand]
                self.assertEqual(Counter(all_cards),Counter(range(52)))
            self.assertIsNotNone(g.winner,f'Seed {seed} did not finish')
            self.assertEqual(g.hands[g.winner],[])
            self.assertFalse(g.play([4]))
            self.assertFalse(g.pass_turn())

if __name__=='__main__':unittest.main()
