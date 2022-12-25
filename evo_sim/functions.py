import functools
import numpy as np
import random


def cosine_part(*, amp: float, phi: float, f: float, n_points: int):
    time = np.arange(n_points) / float(n_points)
    return amp * np.cos(2 * np.pi * f * time + 2 * np.pi * phi)


def hill(n_points: int, scale: float = 1.0, pos_y: float = 0.0):
    f1 = 2
    f2 = 7
    f3 = 20
    f4 = 0.5

    _cosine_part = functools.partial(cosine_part, n_points=n_points)

    part_1 = _cosine_part(
        amp=1.0,
        phi=random.random(),
        f=f1,
    )
    part_2 = _cosine_part(
        amp=0.25,
        phi=random.random(),
        f=f2,
    )
    part_3 = _cosine_part(
        amp=0.1,
        phi=random.random(),
        f=f3,
    )
    part_4 = _cosine_part(
        amp=1.65,
        phi=random.random(),
        f=f4,
    )

    cos_sum = part_1 + part_2 + part_3 + part_4 + 2

    # Normalize
    cos_sum = np.abs(cos_sum)
    max_height = np.max(cos_sum)
    return scale * (cos_sum / max_height) + pos_y
