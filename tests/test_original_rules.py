"""Regression tests against the actual pre-redesign source, not a rules summary."""
import ast
from pathlib import Path
import random
import unittest
import original_rules
from game import Game, beats, classify

SOURCE = Path(__file__).resolve().parents[1] / 'art/legacy_main.py.txt'

class OriginalRuleTests(unittest.TestCase):
    def test_rule_functions_are_unchanged(self):
        old = ast.parse(SOURCE.read_text(encoding='utf-8'))
        current = ast.parse(Path(original_rules.__file__).read_text(encoding='utf-8'))
        functions = {n.name: ast.dump(n, include_attributes=False) for n in old.body if isinstance(n, ast.FunctionDef)}
        for node in current.body:
            if isinstance(node, ast.FunctionDef):
                self.assertEqual(ast.dump(node, include_attributes=False), functions[node.name], node.name)
        self.assertEqual(original_rules.rule, 'Taiwan')

    def test_comparisons_match_original(self):
        old = ast.parse(SOURCE.read_text(encoding='utf-8'))
        needed = {'straight_taiwan_big','one_card','two_card','five_card','thirteen_card','fk_big','full_house_big','compare_card','valid_first_put_card'}
        module = ast.Module(body=[n for n in old.body if isinstance(n,ast.FunctionDef) and n.name in needed],type_ignores=[])
        baseline = {'rule':'Taiwan','start3c':0}
        exec(compile(module,str(SOURCE),'exec'),baseline)
        rng = random.Random(417)
        hands = [[c] for c in range(52)]
        for rank in range(13):
            hands.extend([[rank*4,rank*4+1],[rank*4+2,rank*4+3]])
            other=(rank+1)%13
            hands.extend([[rank*4+i for i in range(3)]+[other*4,other*4+1],
                          [rank*4+i for i in range(4)]+[other*4]])
        for start in range(9):
            for suit in range(4):hands.append([4*r+suit for r in range(start,start+5)])
            hands.append([4*r+rng.randrange(4) for r in range(start,start+5)])
        hands.extend([[48,0,5,10,15],list(range(0,52,4)),[4*r+r%4 for r in range(13)]])
        for _ in range(5000):
            hand=sorted(rng.sample(range(52),5))
            expected=baseline['five_card'](hand)
            actual=classify(hand)
            self.assertEqual(actual[0]*1000 if actual else 0,expected)
        for _ in range(10000):
            table,cards=rng.choices(hands,k=2)
            self.assertEqual(beats(cards,table),baseline['compare_card'](sorted(table),len(table),sorted(cards),len(cards))==1)
        for opening in (0,1):
            for cards in hands+[[4,5,6],[]]:
                baseline['start3c']=opening
                expected=baseline['valid_first_put_card'](sorted(cards),len(cards))==1
                g=Game(0);g.hands[g.turn]=list(range(52));g.opening=bool(opening)
                self.assertEqual(g.legal(cards),expected)

    def test_four_twos_do_not_trigger_added_redeal(self):
        seed=next(seed for seed in range(2000) if self.has_four_twos(seed))
        rng=random.Random(seed);deck=list(range(52));rng.shuffle(deck)
        actual=Game(seed)
        self.assertEqual([set(h) for h in actual.hands],[set(deck[i::4]) for i in range(4)])

    @staticmethod
    def has_four_twos(seed):
        rng=random.Random(seed);deck=list(range(52));rng.shuffle(deck)
        return any(set(range(4)).issubset(deck[i::4]) for i in range(4))

if __name__=='__main__':unittest.main()
