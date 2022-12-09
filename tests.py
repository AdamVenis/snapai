import unittest

from snap import *
from cards import *

ROCKS = [Rock()] * 12

'''
categories of resolution order

onreveal
ongoing
jotunheim



TestCase

Medusa IronMan -> 8 (also IronMan Medusa)

IronMan Punisher -> opponent plays cards

MisterFantastic mid, IronMan left

Colossus Deathlok

Nightcrawler - move action

Punisher against squirrel girl in another lane

Spectrum doesn't buff Ongoing that have been Enchantress'd










Forge into Punisher, gets hit with Enchantress

Simple Cards to add:
Spectrum
NightCrawler
Squirrel Girl


Simple Locations:

Xander (+1 ongoing)
Baxter Building
Atlantis (+5 if only card there)
'''

class TestEverything(unittest.TestCase):
    def setUp(self):
        self.game = Game(ROCKS, ROCKS)

    def test_basic(self):
        game = self.game
        self.play_card(MistyKnight(), 0)
        self.assertEqual([[0, 0, 0], [0, 0, 0]], game.get_powers())
        self.finish_round_and_assert_powers([[2, 0, 0], [0, 0, 0]])

    # invalids:
    # def test_hawkeye(self):
    # game = self.game
    #     game.players[0].cards[0] = Hawkeye()
    #     game.players[0].cards[1] = Shocker()
    #     game.step(Play(0, 0))
    #     self.assertEqual([[1, 0, 0], [0, 0, 0]], game.get_powers())
    #     game.step(EndTurn())
    #     game.step(EndTurn())
    #     game.step(Play(0, 0))
    #     self.assertEqual([[6, 0, 0], [0, 0, 0]], game.get_powers())

    def test_medusa(self):
        game = self.game
        self.play_card(Medusa(), 0)
        self.play_card(Medusa(), 1)
        self.finish_round_and_assert_powers([[2, 4, 0], [0, 0, 0]])

    def test_starlord(self):
        game = self.game

        self.play_card(StarLord(), 0)
        self.play_card(StarLord(), 1)
        game.step(EndTurn())
        self.play_card(Rock(), 1)
        self.finish_round_and_assert_powers([[2, 5, 0], [0, 0, 0]])

    def test_misterfantastic(self):
        game = self.game
        self.play_card(MisterFantastic(), 0)
        self.finish_round_and_assert_powers([[2, 0, 0], [0, 0, 0]])

    def test_punisher(self):
        game = self.game
        self.play_card(Punisher(), 0)
        self.finish_round_and_assert_powers([[2, 0, 0], [0, 0, 0]])
        game.step(EndTurn())
        self.play_card(Rock(), 0)
        self.finish_round_and_assert_powers([[3, 0, 0], [0, 0, 0]])
        game.step(EndTurn())
        self.play_card(Rock(), 0)
        self.finish_round_and_assert_powers([[4, 0, 0], [0, 0, 0]])
        game.step(EndTurn())
        self.play_card(Rock(), 0)
        self.finish_round_and_assert_powers([[5, 0, 0], [0, 0, 0]])

    def test_namor(self):
        game = self.game
        self.play_card(Namor(), 0)
        self.finish_round_and_assert_powers([[5, 0, 0], [0, 0, 0]])

    def test_ironman(self):
        game = self.game
        self.play_card(MistyKnight(), 0)
        self.play_card(IronMan(), 0)
        self.finish_round_and_assert_powers([[4, 0, 0], [0, 0, 0]])

    def test_games(self):
        env = Env(p1_deck=ROCKS, p2_deck=ROCKS)
        agents = [RandomAgent(), RandomAgent()]
        results = collections.defaultdict(int)
        for _ in range(100):
            env.reset()
            result = play_game(env, agents)
            results[result] += 1

        return {k: v / 100 for k, v in results.items()}

    def play_card(self, card_info, location_index):
        self.game.current_player().cards[0] = Card(card_info)
        self.game.step(Play(0, location_index))

    def finish_round_and_assert_powers(self, expected_powers):
        current_round = self.game.current_round
        while self.game.current_round == current_round:
            self.game.step(EndTurn())
        self.assertEqual(expected_powers, self.game.get_powers())


if __name__ == "__main__":
    unittest.main()
