import typing

from dataclasses import dataclass


MAX_CARDS = 7
MAX_CARDS_AT_LOCATION = 4
NUM_LOCATIONS = 3
ROUNDS = 6


class Action:
    def act(self):
        pass


@dataclass
class EndTurn:
    def valid(self, player, game):
        return True


@dataclass
class Play:
    card_index: int
    location_index: int

    def valid(self, player, game):
        if self.card_index >= len(player.cards):
            return False
        if self.location_index >= NUM_LOCATIONS:
            return False
        return True

    def act(self, player, game):
        card = player.cards.pop(self.card_index)
        player.cards_at_location[self.location_index].append(card)
        card.location_index = self.location_index
        player.reveal_queue.append(card)
        player.locations_revealed_this_turn.append(self.location_index)


class Trigger:
    pass


@dataclass
class OneTimeEffect:
    condition: typing.Any
    outcome: typing.Any


@dataclass
class OnAction(Trigger):
    condition: typing.Any
    outcome: typing.Any


class OnReveal(OnAction):
    def __init__(self, outcome):
        self.condition = lambda event: event == Reveal
        self.outcome = outcome


@dataclass
class NextTurn(Trigger):
    trigger: Trigger


class Player:
    def __init__(self, deck_info):
        self.cards_at_location = [[], [], []]
        self.deck = [Card(card_info, self) for card_info in deck_info]
        self.cards = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        self.powers = [0, 0, 0]
        self.effects = []
        self.reveal_queue = []
        self.locations_revealed_this_turn = []

    def __repr__(self):
        lines = []
        for i in range(NUM_LOCATIONS):
            lines.append(f"{self.cards_at_location[i]}")
        return "\n".join(lines)


@dataclass
class CardInfo:
    energy: int
    power: int

    @staticmethod
    def ability(game, player, location_index, card):
        pass


@dataclass
class Card:
    info: CardInfo

    def __init__(self, info: CardInfo, player: Player):
        self.info = info
        self.power = info.power
        self.energy = info.energy
        self.ability = info.ability
        self.revealed = False
        self.location_index = None
        self.player = player

    def add_power(self, delta):
        self.power += delta
        self.player.powers[self.location_index] += delta


class Event:
    pass


@dataclass
class Reveal:
    card: Card
