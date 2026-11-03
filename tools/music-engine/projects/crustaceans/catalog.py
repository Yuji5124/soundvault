"""『甲殻類にも都合があります。』 (crustaceans-have-plans): title, deep-sea, battle and scene themes."""
from pieces_battle import PIECES as BATTLE
from pieces_crust import PIECES as DEEP
from pieces_world import PIECES as WORLD

PIECES = {**DEEP, **BATTLE, **WORLD}
