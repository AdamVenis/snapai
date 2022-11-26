import collections
import enum
from dataclasses import dataclass
import random
import typing

from cards import *
from common import *

"""
TODO:
- add tests
- figure out a resolution strategy for on reveal/ongoing/calculating powers
- add locations

Interesting interactions:
- if nightcrawler moves to cloak, it counts as his only move
- hulk + elysium + swap power/energy => 5/5
"""

"""
you were:
- figuring out how to pass parameters into events
    maybe the effect is On(event_type, condition, result)
    or maybe just Trigger(condition, result)
    and the condition includes matching event type /shrug
"""


STARTER_DECK = [
    Hawkeye(),
    Quicksilver(),
    MistyKnight(),
    Medusa(),
    StarLord(),
    Shocker(),
    MisterFantastic(),
    Punisher(),
    Namor(),
    IronMan(),
    Gamora(),
    Hulk(),
]

ALL_ACTIONS = [EndTurn()] + [
    Play(i, j) for i in range(MAX_CARDS) for j in range(NUM_LOCATIONS)
]


class GameResult(enum.Enum):
    UNFINISHED = 0
    P1_WIN = 1
    P2_WIN = 2
    DRAW = 3


class Event(enum.Enum):
    PLAY_CARD = 0


class Game:
    def __init__(self, p1_deck, p2_deck):
        self.result = GameResult.UNFINISHED
        self.players = [Player(list(p1_deck)), Player(list(p2_deck))]
        self.initiative_index = random.randint(0, 1)
        self.current_round = 0
        self.max_rounds = ROUNDS
        self.current_player_index = 0

    def get_initiative(self):
        p1_locations, p2_locations = 0, 0
        p1, p2 = self.players
        for loc in range(NUM_LOCATIONS):
            if p1.powers[loc] > p2.powers[loc]:
                p1_locations += 1
            elif p1.powers[loc] < p2.powers[loc]:
                p2_locations += 1
        if p1_locations > p2_locations:
            return 0
        elif p1_locations < p2_locations:
            return 1

        p1_total = sum(p1.powers)
        p2_total = sum(p2.powers)
        if p1_total > p2_total:
            return 0
        elif p1_total < p2_total:
            return 1
        else:
            return 0.5

    def get_powers(self):
        return [player.powers for player in self.players]

    def check_result(self):
        initiative = self.get_initiative()
        next_initiative = random.randint(0, 1) if initiative == 0.5 else initiative

        self.initiative_index = next_initiative
        if self.current_round == self.max_rounds:
            if initiative == 0:
                self.result = GameResult.P1_WIN
            elif initiative == 1:
                self.result = GameResult.P2_WIN
            elif initiative == 0.5:
                self.result = GameResult.DRAW

    def finish_round(self):
        for player in self.players:
            while player.reveal_queue:
                card = player.reveal_queue.pop(0)
                card.revealed = True
                player.powers[card.location_index] += card.power
                ability = card.ability(self, player, card.location_index, card)
                if ability is not None:
                    player.effects.append(ability)
                self.trigger(Reveal)

        for player in self.players:
            player.locations_revealed_this_turn.clear()

    def start_round(self):
        for player in self.players:
            if len(player.cards) < MAX_CARDS and len(player.deck) > 0:
                player.cards.append(player.deck.pop())

    def current_player(self):
        return self.players[self.current_player_index]

    def step(self, action):
        self.check_result()
        if self.result != GameResult.UNFINISHED:
            return self.result

        if type(action) == EndTurn:
            self.current_player_index = (self.current_player_index + 1) % 2
            if self.current_player_index == 0:
                self.finish_round()
                self.current_round += 1
                self.start_round()
        else:
            action.act(self.current_player(), self)

        return self.result

    def trigger(self, event):
        for player in self.players:
            for i, effect in enumerate(player.effects):
                while effect.condition(event):
                    effect.outcome()
                    player.effects.pop(i)
                    if not player.effects:
                        break
                    effect = player.effects[i]

    def opponent(self, player):
        return self.players[0] if player == self.players[1] else self.players[1]

    def __repr__(self):
        lines = []
        p1, p2 = self.players
        p1_powers, p2_powers = self.get_powers()
        for i in range(NUM_LOCATIONS):
            line = f"{p1.cards_at_location[i]} ({p1_powers[i]} - {p2_powers[i]}) {p2.cards_at_location[i]}"
            lines.append(line)
        return "\n".join(lines)


class EndTurnAgent:
    def get_action(self, game):
        return EndTurn()


class RandomAgent:
    def get_action(self, game):
        current_player = game.current_player()
        valid_actions = [
            action for action in ALL_ACTIONS if action.valid(current_player, game)
        ]
        return random.choice(valid_actions)


class Env:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.reset()

    def reset(self):
        self.game = Game(**self.kwargs)


def play_game(env, agents):
    game = env.game
    while game.result == GameResult.UNFINISHED:
        agent = agents[game.current_player_index]
        action = agent.get_action(game)
        game.step(action)
    return game.result


def winrate(env, agents, num_episodes):
    results = collections.defaultdict(int)
    for _ in range(num_episodes):
        env.reset()
        result = play_game(env, agents)
        results[result] += 1

    return {k: v / num_episodes for k, v in results.items()}


def evaluate_winrates(env, num_episodes):
    # print(winrate(env, [EndTurnAgent(), EndTurnAgent()], num_episodes))
    # print(winrate(env, [RandomAgent(), EndTurnAgent()], num_episodes))
    print(winrate(env, [RandomAgent(), RandomAgent()], num_episodes))


if __name__ == "__main__":
    env = Env(p1_deck=STARTER_DECK, p2_deck=STARTER_DECK)

    evaluate_winrates(env, num_episodes=1000)
