from random import randint
import math
from screen import Screen


class Ship:
    """
    class Ship create new ship and response to move the ship (that mean
     to change the location) with the screen object the class can draw on the
      screen
    """
    ROTATION_DEG = 7
    SHIP_RADIUS = 1
    SHIP_LIVES = 3
    INITIAL_SPEED = 0
    INITIAL_DIRECTION = 0.0

    def __init__(self, screen):
        """
        the constructor of the class
        :param screen: screen object
        """
        self.screen = screen
        self.x_axis = randint(self.screen.SCREEN_MIN_X, self.screen.SCREEN_MAX_X)
        self.y_axis = randint(self.screen.SCREEN_MIN_Y, self.screen.SCREEN_MAX_Y)
        self.nose_direction = self.INITIAL_DIRECTION
        self.x_speed = self.INITIAL_SPEED
        self.y_speed = self.INITIAL_SPEED
        self.lives = self.SHIP_LIVES

    def coordinates_calculator(self, min_x, max_x, min_y, max_y):
        """ calculate the coordinates of the ship according to where he is
                and his speed, with the limits of the board as given"""
        new_spot_x = min_x + ((self.x_axis + self.x_speed - min_x) % (
                max_x - min_x))
        new_spot_y = min_y + ((self.y_axis + self.y_speed - min_y) % (
                max_y - min_y))
        return new_spot_x, new_spot_y

    def move(self):
        """
        the main function of this section. responsible to the movement of the
        ship on the screen
        """
        # do i need to move left or right
        if self.screen.is_left_pressed():
            self.nose_direction += self.ROTATION_DEG
        if self.screen.is_right_pressed():
            self.nose_direction -= self.ROTATION_DEG

        # do i need to accelarate
        if self.screen.is_up_pressed():
            self.ship_acceleration()
        if self.screen.is_back_pressed():
            self.ship_slowdown()
        if self.screen.is_s_pressed():
            self.ship_stop()

        # the calculator of the new coordination
        self.x_axis, self.y_axis = self.coordinates_calculator(
            Screen.SCREEN_MIN_X,
            Screen.SCREEN_MAX_X,
            Screen.SCREEN_MIN_Y,
            Screen.SCREEN_MAX_X)

        # now draw me to screen
        self.screen.draw_ship(self.x_axis, self.y_axis,
                              self.nose_direction)

    def ship_stop(self):
        self.x_speed = 0
        self.y_speed = 0
        return self.x_speed, self.y_speed

    def ship_slowdown(self):
        """
        the math equation for acceleration
        :return: the new speed of the ship
        """
        self.x_speed -= math.cos(math.radians(self.nose_direction))
        self.y_speed -= math.sin(math.radians(self.nose_direction))
        return self.x_speed, self.y_speed

    def ship_acceleration(self):
        """
        the math equation for acceleration
        :return: the new speed of the ship
        """
        self.x_speed += math.cos(math.radians(self.nose_direction))
        self.y_speed += math.sin(math.radians(self.nose_direction))
        return self.x_speed, self.y_speed

    def get_radius(self):
        """
        :return: the radius of the ship
        """
        return self.SHIP_RADIUS
