from screen import Screen
import math
from copy import deepcopy


class Torpedo:
    """
    class torpedo create new torpedo obejct
    """
    TORPEDO_RADIUS = 4
    TORPEDO_LIFE = 200

    def __init__(self, screen, ship):
        """
        the constructor
        :param screen: screen object
        :param ship: Ship object
        """
        self.ship = ship
        self.screen = screen
        self.x_axis = deepcopy(ship.x_axis)
        self.y_axis = deepcopy(ship.y_axis)
        self.nose_direction = deepcopy(ship.nose_direction)
        self.x_speed =  self.ship.x_speed + 2 * math.cos(
            math.radians(self.nose_direction))
        self.y_speed = self.ship.y_speed + 2 * math.sin(
            math.radians(self.nose_direction))
        self.life_time = self.TORPEDO_LIFE



    def coordinates_calculator(self, min_x, max_x, min_y, max_y):
        """
        calculate the coordinates of the torpedo according to where he is
        and his speed, with the limits of the board as given
        """

        new_spot_x = min_x + (self.x_axis + self.x_speed - min_x) % (
                max_x - min_x)
        new_spot_y = min_y + (self.y_axis + self.y_speed - min_y) % (
                max_y - min_y)
        return new_spot_x, new_spot_y

    def move(self, torpedo):
        """the movement of the torpedo"""
        self.x_axis, self.y_axis = self.coordinates_calculator(
            Screen.SCREEN_MIN_X,
            Screen.SCREEN_MAX_X,
            Screen.SCREEN_MIN_Y,
            Screen.SCREEN_MAX_X)
        self.screen.draw_torpedo(torpedo, self.x_axis, self.y_axis,
                                 self.nose_direction)

    def get_radius(self):
        """
        :return: the radius of the torpedo
        """
        return self.TORPEDO_RADIUS

    def reduce_life(self):
        """
        reducing one life time from the torpedo every call of the function
        :return: None
        """
        self.life_time -= 1
