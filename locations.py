from dataclasses import dataclass

from common import *


@dataclass
class Xandar(LocationInfo):
    def get_power(self, card_powers):
        return sum(card_powers) + len(card_powers)


@dataclass
class Ruins(LocationInfo):
    pass
