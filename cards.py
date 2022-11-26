from dataclasses import dataclass

from common import *

always = lambda x: True


@dataclass
class Hawkeye(CardInfo):
    def __init__(self):
        self.energy = 1
        self.power = 1

    @staticmethod
    def ability(game, player, location_index, card):
        return OnPlay(
            always, Addability(OneTimeability(NextTurn(OnPlayCardInfo()), BuffMe(2)))
        )


@dataclass
class Quicksilver(CardInfo):
    def __init__(self):
        self.energy = 1
        self.power = 2


@dataclass
class MistyKnight(CardInfo):
    def __init__(self):
        self.energy = 1
        self.power = 2


@dataclass
class Medusa(CardInfo):
    def __init__(self):
        self.energy = 2
        self.power = 2

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            if location_index == 1:
                card.add_power(2)

        return OnReveal(on_reveal)


@dataclass
class StarLord(CardInfo):
    def __init__(self):
        self.energy = 2
        self.power = 2

    @staticmethod
    def ability(game, player, location_index, card):
        # if the opponent played a card here this turn, +3
        def on_reveal():
            if location_index in game.opponent(player).locations_revealed_this_turn:
                card.add_power(3)

        return OnReveal(on_reveal)


@dataclass
class Shocker(CardInfo):
    def __init__(self):
        self.energy = 2
        self.power = 3


@dataclass
class MisterFantastic(CardInfo):
    def __init__(self):
        self.energy = 3
        self.power = 2


@dataclass
class Punisher(CardInfo):
    def __init__(self):
        self.energy = 3
        self.power = 2


@dataclass
class Namor(CardInfo):
    def __init__(self):
        self.energy = 4
        self.power = 5


@dataclass
class IronMan(CardInfo):
    def __init__(self):
        self.energy = 5
        self.power = 0


@dataclass
class Gamora(CardInfo):
    def __init__(self):
        self.energy = 5
        self.power = 7


@dataclass
class Hulk(CardInfo):
    def __init__(self):
        self.energy = 6
        self.power = 12


@dataclass
class Rock(CardInfo):
    def __init__(self):
        self.energy = 1
        self.power = 0
