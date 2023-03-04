import math


def radians_to_degrees(angle: float) -> float:
    return angle * (180 / math.pi)


def degrees_to_radians(angle: float) -> float:
    return angle * (math.pi / 180)
