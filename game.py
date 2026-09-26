"""Taiwan Big Two rules, independent of the renderer.

Card ids retain the original project mapping: 2,3,...,K,A; clubs,
diamonds, hearts, spades. Passing withdraws a player until a new trick.
"""
import original_rules as rules
from itertools import combinations
import random


def strength(card):
    return rules.one_card([card], 1)


def classify(cards):
    cards = sorted(cards)
    if len(set(cards)) != len(cards) or any(c not in range(52) for c in cards):
        return None
    size = len(cards)
    if size == 1:
        return (1, rules.one_card(cards, size))
    if size == 2:
        score = rules.two_card(cards)
        return (2, score) if score else None
    if size == 5:
        kind = rules.five_card(cards)
        if not kind:
            return None
        score = (rules.fk_big(cards) if kind == 8000 else
                 rules.full_house_big(cards) if kind == 6000 else
                 rules.straight_taiwan_big(cards, size))
        return (kind // 1000, score)
    if size == 13:
        kind = rules.thirteen_card(cards)
        return (kind // 1000, rules.one_card(cards, size)) if kind else None
    return None


def beats(cards, table):
    if classify(cards) is None:
        return False
    if not table:
        return True
    if classify(table) is None:
        return False
    return rules.compare_card(sorted(table), len(table), sorted(cards), len(cards)) == 1


NAMES = {1: '單張', 2: '對子', 5: '順子', 6: '葫蘆', 8: '鐵支', 9: '同花順', 10: '一條龍', 11: '同花一條龍'}


class Game:
    def __init__(self, seed=None):
        rng = random.Random(seed)
        deck = list(range(52))
        rng.shuffle(deck)
        self.hands = [sorted(deck[i::4], key=strength) for i in range(4)]
        self.turn = next(i for i, hand in enumerate(self.hands) if 4 in hand)
        self.owner = self.turn
        self.table = []
        self.passed = set()
        self.opening = True
        self.winner = None
        self.played = []

    def legal(self, cards):
        if (self.winner is not None or not cards or len(set(cards)) != len(cards)
                or not set(cards).issubset(self.hands[self.turn])):
            return False
        if not self.table:
            rules.start3c = int(self.opening)
            return rules.valid_first_put_card(sorted(cards), len(cards)) == 1
        return beats(cards, self.table)

    def moves(self):
        hand = self.hands[self.turn]
        result = []
        for size in (1, 2, 5, 13):
            if size > len(hand):
                continue
            for cards in combinations(hand, size):
                if self.legal(cards):
                    result.append(cards)
        return result

    def suggest(self):
        moves = self.moves()
        if not moves:
            return ()
        if not self.table:
            return min(moves, key=lambda c: (-len(c), classify(c)))
        return min(moves, key=lambda c: (classify(c), -len(c)))

    def play(self, cards):
        if not self.legal(cards):
            return False
        self.table = sorted(cards, key=strength)
        self.owner = self.turn
        self.opening = False
        for card in cards:
            self.hands[self.turn].remove(card)
            self.played.append(card)
        if not self.hands[self.turn]:
            self.winner = self.turn
        else:
            self.advance()
        return True

    def pass_turn(self):
        if self.winner is not None or not self.table or self.turn == self.owner:
            return False
        self.passed.add(self.turn)
        self.advance()
        return True

    def advance(self):
        if len(self.passed) == 3:
            self.turn = self.owner
            self.passed.clear()
            self.table = []
            return
        self.turn = (self.turn + 1) % 4
        while self.turn in self.passed or self.turn == self.owner:
            self.turn = (self.turn + 1) % 4
