from __future__ import annotations
from math import sqrt, cos, sin


class Translation2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def hypo(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def from_hypo(hypo, angle) -> Translation2d:
        x = sin(angle) * hypo
        y = cos(angle) * hypo
        return Translation2d(x, y)

    def __sub__(self, other: Translation2d) -> Translation2d:
        return Translation2d(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"Translation2d(x={self.x}, y={self.y})"

    def __repr__(self) -> str:
        return self.__str__()
