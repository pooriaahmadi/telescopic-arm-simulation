from typing import List
from Translation2d import Translation2d
import math
from Units import degrees_to_radians


class Arm:
    def __init__(self, telescopic_min_length: float, telescopic_max_length: float, wrist_length: float, pivot_point: Translation2d) -> None:
        self.telescopic_min_length = telescopic_min_length
        self.telescopic_max_length = telescopic_max_length
        self.wrist_length = wrist_length
        self.pivot_point = pivot_point

    def calculate(self, destination: Translation2d, wrist_angle: float):
        arm_end_point = destination - self.wrist_components(wrist_angle)
        arm_isolated = arm_end_point - self.pivot_point

        arm_pivot_angle = 0 if arm_isolated.y == 0 else math.atan(
            arm_isolated.x / arm_isolated.y)
        wrist_arm_angle = degrees_to_radians(180) - wrist_angle - \
            math.atan(arm_isolated.y / arm_isolated.x)
        arm_length = math.sqrt(arm_isolated.x**2 + arm_isolated.y**2)

        if arm_length < self.telescopic_min_length:
            arm_length = self.telescopic_min_length
        elif arm_length > self.telescopic_max_length:
            arm_length = self.telescopic_max_length
        return arm_isolated, arm_length, arm_pivot_angle, wrist_arm_angle

    def wrist_components(self, angle: float) -> Translation2d:
        x = math.cos(angle) * self.wrist_length
        y = math.sin(angle) * self.wrist_length

        return Translation2d(x, y)
