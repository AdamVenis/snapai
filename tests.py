import unittest

from snap import *
from cards import *
from locations import *

ROCKS = [Rock()] * 12
RUINS = [Ruins()] * 3

"""
categories of resolution order

onreveal
ongoing
end of turn (jotunheim)
end of game (captain marvel)



TestCase

MisterFantastic mid, IronMan left

Colossus Deathlok

Nightcrawler - move action

Punisher against squirrel girl in another lane

Spectrum doesn't buff Ongoing that have been Enchantress'd

Qs:
- does punisher get buff before card is revealed? relevant for e.g. invisible woman and shangchi
    A: yes







Forge into Punisher, gets hit with Enchantress

Simple Cards to add:
Spectrum
NightCrawler
Squirrel Girl


Simple Locations:

Xander (+1 ongoing)
Baxter Building
Atlantis (+5 if only card there)
"""


class TestEverything(unittest.TestCase):
    def setUp(self):
        self.new_game()

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
        self.finish_round_and_assert_powers([[2, 2, 0], [0, 0, 0]])
        self.play_card(MisterFantastic(), 1)
        self.finish_round_and_assert_powers([[4, 4, 2], [0, 0, 0]])

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

        game = self.new_game()
        self.play_card(IronMan(), 1)
        self.play_card(Medusa(), 1)
        self.finish_round_and_assert_powers([[0, 8, 0], [0, 0, 0]])

        game = self.new_game()
        self.play_card(IronMan(), 0)
        self.play_card(Punisher(), 0)
        self.finish_round_and_assert_powers([[4, 0, 0], [0, 0, 0]])
        game.step(EndTurn())
        self.play_card(Rock(), 0)
        self.finish_round_and_assert_powers([[6, 0, 0], [0, 0, 0]])

    def test_galactus(self):
        game = self.new_game()
        self.play_card(Galactus(), 0)
        self.finish_round_and_assert_powers([[3], [0]])
        assert(len(self.game.locations) == 1)

        game = self.new_game()
        self.play_card(MistyKnight(), 0)
        self.play_card(Galactus(), 0)
        self.finish_round_and_assert_powers([[5, 0, 0], [0, 0, 0]])
        assert(len(self.game.locations) == 3)


    def test_cosmo(self):
        game = self.new_game()
        self.ensure_p1_initiative()
        self.play_card(Cosmo(), 0)
        game.step(EndTurn())
        self.play_card(StarLord(), 0)
        self.finish_round_and_assert_powers([[3, 0, 2], [2, 0, 0]])


    # ------- LOCATIONS --------

    def test_xandar(self):
        game = self.game
        self.set_all_locations(Xandar())
        self.play_card(MistyKnight(), 0)
        self.play_card(MistyKnight(), 1)
        self.play_card(MistyKnight(), 1)
        self.finish_round_and_assert_powers([[3, 6, 0], [0, 0, 0]])

        game = self.new_game()
        self.set_all_locations(Xandar())
        self.play_card(IronMan(), 0)
        self.finish_round_and_assert_powers([[2, 0, 0], [0, 0, 0]])

    def test_games(self):
        env = Env(p1_deck=ROCKS, p2_deck=ROCKS, location_infos=RUINS)
        agents = [RandomAgent(), RandomAgent()]
        results = collections.defaultdict(int)
        for _ in range(100):
            env.reset()
            result = play_game(env, agents)
            results[result] += 1

        return {k: v / 100 for k, v in results.items()}

    def new_game(self):
        self.game = Game(ROCKS, ROCKS, RUINS)
        return self.game

    def play_card(self, card_info, location_index):
        self.game.current_player().cards[0] = Card(card_info)
        self.game.step(Play(0, location_index))

    def set_all_locations(self, location_info):
        for i in [0, 1, 2]:
            self.game.locations[i] = Location(location_info)

    def finish_round_and_assert_powers(self, expected_powers):
        current_round = self.game.current_round
        while self.game.current_round == current_round:
            self.game.step(EndTurn())
        self.assertEqual(expected_powers, self.game.get_powers())


    def ensure_p1_initiative(self):
        self.play_card(MistyKnight(), 2)
        self.game.step(EndTurn())
        self.game.step(EndTurn())


if __name__ == "__main__":
    unittest.main()
