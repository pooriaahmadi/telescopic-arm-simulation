import pygame
from Arm import Arm
from Translation2d import Translation2d
from Units import degrees_to_radians, radians_to_degrees


arm = Arm(10, 18, 3, Translation2d(2.22, 7.12))

pygame.init()


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


width = 1500
height = 900
screen = pygame.display.set_mode((width, height))
done = False

white = (255, 255, 255)
padding = 20

# load the fonts
font = pygame.font.SysFont("monospace", 24)
font.set_bold(True)

destination = Translation2d(0, 0)
destination_text = font.render(
    f"Target: x={destination.x}, y={destination.y}", True, (0, 0, 255))

mouse_text = font.render(
    f"Mouse: x={destination.x}, y={destination.y}", True, (0, 0, 255))

arm_pivot_text = font.render(f"Arm Pivot: 0", True, (255, 0, 0))
arm_length_text = font.render(f"Arm Pivot: 0", True, (0, 0, 255))
wrist_angle_text = font.render(
    f"Wrist angle(arm relative): 0", True, (255, 208, 0))


mouse_last_x = 0
mouse_last_y = 0

chassis = pygame.image.load("images/chassis.png")
chassis = pygame.transform.smoothscale(
    chassis, (100 * chassis.get_width() / chassis.get_height(), 100))
chassis.convert()

ss = pygame.image.load("images/ss.png")
ss = pygame.transform.smoothscale(
    ss, (580 * ss.get_width() / ss.get_height(), 580))
ss.convert()


arm_base_original = pygame.image.load("images/arm_base.png")
arm_base_original = pygame.transform.smoothscale(
    arm_base_original, (140 * arm_base_original.get_width() / arm_base_original.get_height(), 140))

arm_extend_original = pygame.image.load("images/arm_extend.png")
arm_extend_original = pygame.transform.smoothscale(
    arm_extend_original, (55 * arm_extend_original.get_width() /
                          arm_extend_original.get_height(), 55)
)

intake_original = pygame.image.load("images/intake.png")
intake_original = pygame.transform.smoothscale(
    intake_original, (160 * intake_original.get_width() / intake_original.get_height(), 160))

intake_angle = 0

while not done:
    [mouse_x, mouse_y] = pygame.mouse.get_pos()
    if mouse_last_x != mouse_x or mouse_last_y != mouse_y:
        destination = Translation2d(mouse_x / 50, mouse_y / 50)
        destination_text = font.render(
            f"Target: x={destination.x}, y={destination.y}", True, (0, 0, 255))
        mouse_text = font.render(
            f"Mouse: x={mouse_x}, y={mouse_y}", True, (0, 0, 255))

    mouse_last_x = mouse_x
    mouse_last_y = mouse_y

    [arm_end_point, arm_length, arm_pivot, wrist_angle] = arm.calculate(
        destination, degrees_to_radians(intake_angle))

    arm_pivot_text = font.render(
        f"Arm Pivot: {radians_to_degrees(arm_pivot)}", True, (255, 0, 0))
    arm_length_text = font.render(
        f"Arm length: {arm_length}", True, (0, 0, 255))
    wrist_angle_text = font.render(
        f"Wrist angle(arm relative): {radians_to_degrees(wrist_angle)}", True, (255, 208, 0))

    if arm_pivot < 0:
        arm_pivot += degrees_to_radians(180)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    screen.fill((0, 0, 0))
    screen.blit(destination_text,
                (width - destination_text.get_width() - padding, padding))
    screen.blit(mouse_text,
                (width - mouse_text.get_width() - padding, padding + destination_text.get_height() + 10))

    screen.blit(arm_pivot_text,
                (width - arm_pivot_text.get_width() - padding, 100))
    screen.blit(arm_length_text,
                (width - arm_length_text.get_width() - padding, 130))
    screen.blit(wrist_angle_text,
                (width - wrist_angle_text.get_width() - padding, 160))

    screen.blit(chassis, (padding, height - padding - chassis.get_height()))
    screen.blit(ss, (padding + 10, height -
                padding - chassis.get_height() / 2 - ss.get_height()))
    arm_base, arm_base_rect = rot_center(
        arm_base_original, radians_to_degrees(arm_pivot) - 90, 111, 352)
    screen.blit(arm_base, arm_base_rect)

    arm_base_translation = Translation2d.from_hypo(arm_length, arm_pivot)
    intake, intake_rect = rot_center(
        intake_original, intake_angle, 111 + arm_base_translation.x * 50, 352 + arm_base_translation.y * 50)

    screen.blit(intake, intake_rect)

    if arm_length - arm.telescopic_min_length > 0:
        extendable_translation = Translation2d.from_hypo(
            arm_length - arm.telescopic_min_length, arm_pivot)
        arm_extend, arm_extend_rect = rot_center(
            arm_extend_original, radians_to_degrees(arm_pivot) - 90, 111 + extendable_translation.x * 50, 352 + extendable_translation.y * 50)
        screen.blit(arm_extend, arm_extend_rect)
    else:
        arm_extend, arm_extend_rect = rot_center(
            arm_extend_original, radians_to_degrees(arm_pivot) - 90, 111, 352)
        screen.blit(arm_extend, arm_extend_rect)

    pygame.display.flip()
