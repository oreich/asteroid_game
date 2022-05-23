from screen import Screen
from random import randint
import math

# this is a backup file
class Asteroid:
    """
    class asteroid create asteroid object
    """
    ASTR_SIZE = 3
    ASTR_RADIUS = ASTR_SIZE * 10 - 5

    def get_astr_speed(self):
        """
        :return: the random speed of the asteroid
        """
        while True:
            x = randint(-4, 4)
            if x != 0:
                speed = x
                break
        return speed

    def __init__(self, screen):
        """
        the constructor
        :param screen: screen object
        """
        self.screen = screen
        self.x_axis = randint(self.screen.SCREEN_MIN_X,
                              self.screen.SCREEN_MAX_X)
        self.y_axis = randint(self.screen.SCREEN_MIN_Y,
                              self.screen.SCREEN_MAX_Y)
        self.x_speed = self.get_astr_speed()
        self.y_speed = self.get_astr_speed()
        self.size = self.ASTR_SIZE

    def coordinates_calculator(self, min_x, max_x, min_y, max_y):
        """
        calculate the coordinates of the ship according to where he is
        and his speed, with the limits of the board as given
        :return: new location of the asteroid
        """
        new_spot_x = min_x + (self.x_axis + self.x_speed - min_x) % (
                max_x - min_x)
        new_spot_y = min_y + (self.y_axis + self.y_speed - min_y) % (
                max_y - min_y)
        return new_spot_x, new_spot_y

    def move(self):
        """
        this function respons on the movement of the asteroid
        :return: None
        """
        self.x_axis, self.y_axis = self.coordinates_calculator(
            Screen.SCREEN_MIN_X,
            Screen.SCREEN_MAX_X,
            Screen.SCREEN_MIN_Y,
            Screen.SCREEN_MAX_X)

    def get_astr_radius(self, astr_size):
        """

        :param astr_size: teh size of the colapssed prev asteroid
        :return: new size of the asteroid
        """
        return astr_size * 10 - 5

    def has_intersection(self, obj):
        """
        checking if the obj has the same location as the asteroid
        :param obj:
        :return: True if they in the same location .False else
        """
        distance = math.sqrt(math.pow((obj.x_axis - self.x_axis), 2) +
                             math.pow((obj.y_axis - self.y_axis), 2))
        if distance <= self.get_astr_radius(self.size) + obj.get_radius():
            return True
        return False

    def set_size(self):
        """
        change the size
        :return: None
        """
        self.size -= 1
