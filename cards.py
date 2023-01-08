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
                card.add_buff(Buff(2))

        return OnReveal(on_reveal)


@dataclass
class StarLord(CardInfo):
    def __init__(self):
        self.energy = 2
        self.power = 2

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            if location_index in game.opponent(player).locations_revealed_this_turn:
                card.add_buff(Buff(3))

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

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            if location_index > 0:
                game.locations[location_index - 1].add_buff(LocationBuff(player, 2))
            if location_index < 2:
                game.locations[location_index + 1].add_buff(LocationBuff(player, 2))

        return OnReveal(on_reveal)


@dataclass
class Punisher(CardInfo):
    def __init__(self):
        self.energy = 3
        self.power = 2

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            card.add_buff(PunisherBuff())

        return OnReveal(on_reveal)


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

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            location = game.locations[location_index]
            location.add_buff(DoubleBuff())

        return OnReveal(on_reveal)


@dataclass
class Gamora(CardInfo):
    def __init__(self):
        self.energy = 5
        self.power = 7

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            if location_index in game.opponent(player).locations_revealed_this_turn:
                card.add_buff(Buff(6))

        return OnReveal(on_reveal)


@dataclass
class Hulk(CardInfo):
    def __init__(self):
        self.energy = 6
        self.power = 12

@dataclass
class Galactus(CardInfo):
    def __init__(self):
        self.energy = 6
        self.power = 3

    @staticmethod
    def ability(game, player, location_index, card):
        def on_reveal():
            if len(player.cards_at_locations[location_index]) == 1:
                game.locations = [game.locations[location_index]]
                game.players[0].cards_at_locations = [game.players[0].cards_at_locations[location_index]]
                game.players[1].cards_at_locations = [game.players[1].cards_at_locations[location_index]]

        return OnReveal(on_reveal)



@dataclass
class Rock(CardInfo):
    def __init__(self):
        self.energy = 1
        self.power = 0
