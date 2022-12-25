"""Module for intermediate data representations"""

import dataclasses


@dataclasses.dataclass
class Individual:
    x_pos: float
    y_pos: float
    colour: tuple = (0, 0, 255)
    text: str = ''
