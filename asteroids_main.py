from screen import Screen
from asteroid import Asteroid
from torpedo import Torpedo
from ship import Ship
import sys
import math

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    this is the main class, which is how we run the game
    and combine all the other classes
    """

    NUM_MAX_TORPEDO = 10
    WIN_MESSAGE = 'You are awsom !!! You actually win!!!'
    WIN_TITLE = 'You are great!!'
    LOOSE_MESSEGE = 'Im sorry you loose )-: maybe try in another day'
    LOOSE_TITLE = 'You are not a looser but you loose'
    QUIT_MESSEGE = 'Ok we will meet you in another day'
    QUIT_TITLE = 'You decide to quit'
    CRASH_MASSEGE = 'oops you got crashed darling'
    CRASH_TITLE = 'Ouch !! It hurt!!'
    THE_BIGGEST_ASTEROID = 3
    THE_MEDIUM_ASTEROID = 2
    THE_SMALLEST_ASTEROID = 1
    END_OF_AMOUNT = 0

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.ship = Ship(self.__screen)
        self.astr_list = self.get_amount_of_astr(asteroids_amount)
        self.torpedo_list = []
        self.torpedo = Torpedo(self.__screen, self.ship)
        self.current_score = 0

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def get_amount_of_astr(self, amount):
        """return list of the asteroids who take part in the game
        :return list of the asteroids"""
        a_lst = []
        for i in range(amount):
            astr = Asteroid(self.__screen)
            a_lst.append(astr)
            if astr.x_axis == self.ship.x_axis and \
                    astr.y_axis == self.ship.y_axis:  # in case of crashing into a ship
                a_lst.remove(astr)
                amount += 1
        for ast in a_lst:  # poot the asteroids on the screen
            self.__screen.register_asteroid(ast, ast.size)
        return a_lst

    def astr_new_speed(self, tor, astr):
        """the math to calculate the asteroid speed"""
        ground = math.sqrt(math.pow(astr.x_speed, 2) + math.pow(astr.y_speed, 2))
        astr_new_speed_x = (tor.x_speed + astr.x_speed) / ground
        astr_new_speed_y = (tor.y_speed + astr.y_speed) / ground
        return astr_new_speed_x, astr_new_speed_y

    def astr_creation(self, list1, astr, param, torpedo):
        """create a new asteroid in the right location and the right size
                with the consideration of the torpedo speed, the size he was
                before the crash and math param to get different direction when
                 required for more details see mange_astr func"""
        new_astr = Asteroid(self.__screen)

        # new size to the asteroid
        new_astr.size = astr.size - 1

        # new speed for the asteroid
        x, y = self.astr_new_speed(torpedo, astr)
        # asteroids directions
        if param == '+':
            new_astr.x_speed = x
            new_astr.y_speed = y
        else:
            new_astr.x_speed = -x
            new_astr.y_speed = -y

        # same location as the destroided asteroid
        new_astr.x_axis = astr.x_axis
        new_astr.y_axis = astr.y_axis

        list1.append(new_astr)
        self.__screen.register_asteroid(new_astr,
                                        new_astr.size)

    def mange_astr(self):
        """
        this function response to the relations of the asteroids with
         all the other objects in the game
        """
        copy_astr_list = self.astr_list.copy()

        # if the ship run out of lives - the player loose
        if self.ship.lives == self.END_OF_AMOUNT:
            self.end_game(self.LOOSE_TITLE, self.LOOSE_MESSEGE)

        # if there is no asteroids left - the player wins
        if len(copy_astr_list) == 0:
            return True

        # for the options of asteroids get intersection whit a ship.
        # the ship loosing life, the asteroids gone.
        for i in copy_astr_list:
            copy_astr_list = self.astr_list.copy()
            astr = i
            astr.move()
            self.__screen.draw_asteroid(astr, astr.x_axis,
                                        astr.y_axis)
            if astr.has_intersection(self.ship):
                self.ship.lives -= 1
                self.__screen.remove_life()
                self.__screen.show_message(self.CRASH_TITLE, self.CRASH_MASSEGE)
                self.__screen.unregister_asteroid(astr)
                copy_astr_list.remove(i)
                self.astr_list = copy_astr_list

            # for the options of asteroids get shot by torpedo.
            # the asteroids get smaller (or gone) and the player earn points.
            for j in self.torpedo_list:
                if astr.has_intersection(j):
                    if astr.size == self.THE_BIGGEST_ASTEROID:  # the biggest size
                        self.current_score += 20
                        self.astr_creation(copy_astr_list, astr, '-', j)
                        self.astr_creation(copy_astr_list, astr, '+', j)
                    elif astr.size == self.THE_MEDIUM_ASTEROID:
                        self.current_score += 50
                        self.astr_creation(copy_astr_list, astr, '-', j)
                        self.astr_creation(copy_astr_list, astr, '+', j)
                    elif astr.size == self.THE_SMALLEST_ASTEROID:
                        self.current_score += 100
                    self.__screen.set_score(self.current_score)
                    self.__screen.unregister_asteroid(astr)
                    self.__screen.unregister_torpedo(j)
                    self.torpedo_list.remove(j)
                    copy_astr_list.remove(i)
                    self.astr_list = copy_astr_list

    def manage_torpedo(self):
        """this function response to the torpedo shoot.
               shoot when space pressed and no more than the max limit"""
        if self.__screen.is_space_pressed():
            if len(self.torpedo_list) <= self.NUM_MAX_TORPEDO:
                add_torped = Torpedo(self.__screen, self.ship)
                self.__screen.register_torpedo(add_torped)
                self.torpedo_list.append(add_torped)
        for torped in self.torpedo_list:
            if torped.life_time == self.END_OF_AMOUNT:
                self.torpedo_list.remove(torped)
                self.__screen.unregister_torpedo(torped)
            else:
                torped.reduce_life()
                torped.move(torped)
                self.__screen.draw_torpedo(torped, torped.x_axis, torped.y_axis,
                                           torped.nose_direction)

    def end_game(self, title, messege):
        """

        :param title: title to show
        :param messege: messege to show
        :return: None end the game and exit
        """
        self.__screen.show_message(title, messege)
        self.__screen.end_game()
        sys.exit()

    def _game_loop(self):
        """
        this function response on the game float
        :return: None
        """
        if self.__screen.should_end():  # player choose to quit, exit the game
            self.end_game(self.QUIT_TITLE, self.QUIT_MESSEGE)
        self.ship.move()  # ship movement
        self.manage_torpedo()  # torpedo things
        if self.mange_astr():  # when no more asteroids
            self.end_game(self.WIN_TITLE, self.WIN_MESSAGE)
        else:
            self.mange_astr()  # game keep running


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
