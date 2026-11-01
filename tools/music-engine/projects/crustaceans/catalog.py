"""『甲殻類にも都合があります。』 (crustaceans-have-plans): 3 title, 3 deep-sea and 3 battle themes."""
from pieces_battle import PIECES as BATTLE
from pieces_crust import PIECES as DEEP

PIECES = {**DEEP, **BATTLE}
