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
        player.cards_at_locations[self.location_index].append(card)
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
        self.cards_at_locations = [[], [], []]
        self.deck = [Card(card_info) for card_info in deck_info]
        self.cards = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        self.powers = [0, 0, 0]
        self.effects = []
        self.reveal_queue = []
        self.locations_revealed_this_turn = []

    def get_powers(self, game):
        powers = []
        for i in range(len(self.cards_at_locations)):
            print(self.cards_at_locations[i])
            card_powers = [
                card.get_power(game, self)
                for card in self.cards_at_locations[i]
                if card.revealed
            ]
            powers.append(game.locations[i].get_power(game, self, card_powers))
        return powers

    def __repr__(self):
        lines = []
        for cards_at_location in self.cards_at_locations:
            lines.append(f"{self.cards_at_locations[i]}")
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

    def __init__(self, info: CardInfo):
        self.info = info
        self.power = info.power
        self.energy = info.energy
        self.ability = info.ability
        self.revealed = False
        self.location_index = None
        self.buffs = []

    def add_power(self, delta):
        self.buffs.append(Buff(delta))

    def get_power(self, game, player):
        power = self.power
        for buff in self.buffs:
            power = buff.apply(game, player, self, power)
        return power

    def add_buff(self, buff):
        self.buffs.append(buff)


class LocationInfo:
    def get_power(self, card_powers):
        return sum(card_powers)


@dataclass
class Location:
    info: LocationInfo

    def __init__(self, info: LocationInfo):
        self.info = info
        self.buffs = []

    def add_buff(self, buff):
        self.buffs.append(buff)

    def get_power(self, game, player, card_powers):
        power = self.info.get_power(card_powers)
        for buff in self.buffs:
            power = buff.apply(game, player, power)
        return power


class Event:
    pass


@dataclass
class LocationBuff:
    player: Player
    delta: int

    def apply(self, game, player, power):
        if player != self.player:
            return power
        return power + self.delta


@dataclass
class Buff:
    delta: int

    def apply(self, game, player, card, power):
        return power + self.delta


@dataclass
class DoubleBuff:
    def apply(self, game, player, power):
        return power * 2


class PunisherBuff:
    def apply(self, game, player, card, power):
        location_index = card.location_index
        opponent = game.opponent(player)

        return power + len(opponent.cards_at_locations[location_index])


@dataclass
class Reveal:
    card: Card
