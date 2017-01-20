from random import randint
from grid_class import Grid, MetaGrid
from point_class import Point
from game_class import Game, MetaGame
from game_player import GamePlayer, MetaGamePlayer

class MetaBattleship(MetaGrid, MetaGame, MetaGamePlayer):
    pass

class Battleship(Grid, Game):
    __metaclass__ = MetaBattleship

    ships = {
        # 'carrier' : 5,
        # 'battleship' : 4,
        # 'cruiser' : 3,
        'submarine': 3,
        'destroyer': 2
    }
    grid_column = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I': 8,
        'J': 9,
    }

    def __init__(self,name):
        self.player_name = GamePlayer(name)
        self.computer_name = GamePlayer('Computer')
        self.computer_grid = Grid(10, 10)
        self.computer_tracker = Grid(10, 10)
        self.comp_ship_pos = {}
        self.computer_grid_set = self.comp_ships_place()
        self.computer_ships = self.list_ships(self.comp_ship_pos)
        self.comp_win = []
        self.comp_called_points = {
            'Hits' : [],
            'Miss' : [],
        }
        self.player_grid = Grid(10,10)
        self.player_tracker = Grid(10,10)
        self.ship_pos = {}
        self.place_ships()
        self.player_ships = self.list_ships(self.ship_pos)
        self.player_called_points = {
            'Hits' : [],
            'Miss' : [],
        }
        self.player_win = []


    # asks the user to enter a point and checks if point is in
    @staticmethod
    def _guess_point():
        try:
            user_col = raw_input('Enter the column (A-J) of the point\t').capitalize()
            col_num = Battleship.grid_column[user_col]

        except KeyError:
            print 'the column you entered is not in range'
            # user_col = raw_input('Enter the column (A-J) of the point\t').capitalize()
            # col_num = Battleship.grid_column[user_col]
            Battleship._guess_point()

        try:
            user_r = int(raw_input('Enter the row (0-9) of the point\t'))
        except ValueError:
            print 'you must enter a numerical number (0-9) for the row index'
            user_r = int(raw_input('Enter the row (0-9) of the point\t'))

        if user_r not in range(10):
            print 'the row you entered is not in range'
            user_r = int(raw_input('Enter the row (0-9) of the first point the ship begins at\t'))
        quit_game = raw_input('Would you like to quit the game (yes or no) ').lower()
        if quit_game == 'yes':
            quit = True
        else:
            quit = False

        return user_r, col_num, user_col, quit

    @staticmethod
    def computer_guess(computer_tracker, comp_called_points):
        random_row = randint(0,9)
        random_column = randint(0,9)
        computer_guess_hit = Point(random_row, random_column, 'X')
        computer_guess_miss = Point(random_row, random_column, '@')

        if computer_tracker.get_point(computer_guess_hit) in comp_called_points['Hits']:
            print 'point already called, was a HIT'
            return Battleship.computer_guess(computer_tracker, comp_called_points)
        elif computer_tracker.get_point(computer_guess_miss) in comp_called_points['Miss']:
            print 'point already called, was a MISS'
            return Battleship.computer_guess(computer_tracker, comp_called_points)
        else:
            return random_row, random_column

    @staticmethod
    def check_player(player_tracker, player_called_points):
        player_row, player_col, user_col,quit = Battleship._guess_point()
        player_guess_hit = Point(player_row, player_col, 'X')
        player_guess_miss = Point(player_row, player_col, '@')
        if player_tracker.get_point(player_guess_hit) in player_called_points['Hits']:
            print 'Point already called, was a HIT'
            return Battleship.check_player(player_tracker, player_called_points)
        elif player_tracker.get_point(player_guess_miss) in player_called_points['Miss']:
            print 'Point already called, was a MISS'
            return Battleship.check_player(player_tracker, player_called_points)
        else:
            return player_row, player_col, user_col, quit

    @staticmethod
    def list_ships(ship_dictionary):
        list_ships = []
        for ship, position in ship_dictionary.iteritems():
            list_ships += position
        return list_ships

    def place_ships(self):
        for ship, ship_size in Battleship.ships.iteritems():
            print '\nThe {} has a size of {} units.'.format(ship, ship_size)

            points_taken = []
            for shipper, position in self.ship_pos.iteritems():
                points_taken += position
            print 'Cannot place points at-->'.format(ship), points_taken

            # gives a set of points to place the ship on
            def ship_range():
                print 'Enter first point your ship starts at'
                print 'The ship will either be placed downwards vertically or towards the right horizontally from this point\n'

                ship_positions =[]
                start_row, start_num, user_col, quit = Battleship._guess_point()
                if quit == True:
                    GamePlayer.quit_game(quit)
                first_point = Point(start_row, start_num, '&')
                ship_positions.append(first_point)

                orientation = raw_input('\nHow would you like to place your ship? Enter either: vertical or horizontal\t')
                row_boundary = start_row + (ship_size - 1)
                col_boundary = start_num + (ship_size - 1)
                if row_boundary > 9 or start_row == 9:
                    orientation = 'h'
                elif col_boundary > 9 or start_num ==9:
                    orientation = 'v'

                if orientation == 'v':
                    first_row = start_row
                    for size in range(ship_size - 1):
                        if first_row == 9:
                            start_row -= 1
                            ship_point = Point(start_row, start_num, '&')
                            ship_positions.append(ship_point)
                        else:
                            start_row += 1
                            ship_point = Point(start_row, start_num, '&')
                            ship_positions.append(ship_point)
                else:
                    first_num = start_num
                    for size in range(ship_size - 1):
                        if first_num == 9:
                            start_num -= 1
                            ship_point = Point(start_row, start_num, '&')
                            ship_positions.append(ship_point)
                        else:
                            start_num += 1
                            ship_point = Point(start_row, start_num, '&')
                            ship_positions.append(ship_point)

                quit_game = raw_input('Would you like to quit the game (yes or no) ').lower()
                if quit_game == 'yes':
                    quit = True
                    GamePlayer.quit_game(quit)

                return ship_positions

            ship_positions = ship_range()
            for pos in ship_positions:
                if self.player_grid.get_point(pos) in points_taken:
                    print '\nCannot place ship:  ',ship_positions
                    print '<<Point taken, cannot place ship in these spots: >>', points_taken
                    print self.pretty_grid()
                    ship_positions = ship_range()
                    break
                else:
                    pass

            self.ship_pos[ship] = ship_positions

            for point in ship_positions:
                alter_point = point
                self.player_grid.set_point(alter_point)
            print '\nYour ships are placed here:  ', self.ship_pos
        return self.ship_pos

    def comp_ships_place(self):
        carrier_row = 0
        self.comp_ship_pos['carrier'] = []
        for i in range(5):
            carrier_point = Point(carrier_row, 0, '&')
            self.computer_grid.set_point(carrier_point)
            self.comp_ship_pos['carrier'].append(carrier_point)
            carrier_row += 1

        battle_row = 3
        battle_column = 3
        self.comp_ship_pos['battleship'] = []
        for j in range(4):
            battleship_point = Point(battle_row, battle_column, '&')
            self.computer_grid.set_point(battleship_point)
            self.comp_ship_pos['battleship'].append(battleship_point)
            battle_row += 1

        cruiser_row = 5
        cruiser_column = 7
        self.comp_ship_pos['cruiser'


        ] = []
        for k in range(3):
            cruiser_point = Point(cruiser_row, cruiser_column, '&')
            self.computer_grid.set_point(cruiser_point)
            self.comp_ship_pos['cruiser'].append(cruiser_point)
            cruiser_column += 1

        sub_row = 9
        sub_column = 5
        self.comp_ship_pos['submarine'] = []
        for m in range(3):
            sub_point = Point(sub_row, sub_column, '&')
            self.computer_grid.set_point(sub_point)
            self.comp_ship_pos['submarine'].append(sub_point)
            sub_column += 1

        des_row = 0
        des_column = 9
        self.comp_ship_pos['destroyer'] = []
        for n in range(2):
            des_point = Point(des_row, des_column, '&')
            self.computer_grid.set_point(des_point)
            self.comp_ship_pos['destroyer'].append(des_point)
            des_row += 1

        return self.comp_ship_pos

    @staticmethod
    def pretty_print_grid(desired_grid):
        x_values = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        y_values = range(10)
        grid_string = [' '.join(x_values)]
        for row_index, row in enumerate(desired_grid.public_grid()):
            row_values = map(lambda x: x.get_value(), row)
            grid_string.append(str(y_values[row_index]) + ' ' + ' '.join(row_values))
        return "\n".join(grid_string) + '\n'


    def player_t(self, turn, guess, opponent_grid, list_ships, letter, tracker_grid, called_points, turn_name, turn_win):
        if opponent_grid.get_point(guess) in list_ships:
            print '\n{} got a HIT at ({},{})'.format(turn, letter, guess.get_x())
            point_hit = Point(guess.get_x(), guess.get_y(), 'X')
            tracker_grid.set_point(point_hit)
            called_points['Hits'].append(point_hit)
            opponent_grid.set_point(point_hit)
            turn_name.set_score(1)
            turn_win.append(opponent_grid.get_point(guess))

        else:
            print '\n{} got a MISS at ({},{})'.format(turn, letter, guess.get_x())
            point_miss = Point(guess.get_x(), guess.get_y(), '@')
            tracker_grid.set_point(point_miss)
            called_points['Miss'].append(point_miss)
            opponent_grid.set_point(point_miss)
        return ''


    def player_turn(self):
        quit = False
        while self.is_game_over() == False:
            print 'Computer:', self.computer_name.get_score()
            print '{}: {}\n'.format(self.player_name.get_name(), self.player_name.get_score())

            comp_row, comp_col = Battleship.computer_guess(self.computer_grid, self.comp_called_points)
            for letter, col_num in Battleship.grid_column.iteritems():
                if col_num == comp_col:
                    col_letter = letter
            computer_guess = Point(comp_row, comp_col, '&')
            self.player_t('Computer', computer_guess, self.player_grid, self.player_ships, col_letter, self.computer_tracker, self.comp_called_points, self.computer_name, self.comp_win)
            print '\nYour Ship Board:'
            print Battleship.pretty_print_grid(self.player_grid)
            # print self.pretty_grid()
            self.is_game_over()

            print 'Your Tracking Board:'
            # print Battleship.print_tracker(self.player_tracker)
            print Battleship.pretty_print_grid(self.player_tracker)
            player_row, player_col, user_col, quit = Battleship.check_player(self.player_tracker, self.player_called_points)
            player_guess = Point(player_row, player_col, '&')
            GamePlayer.quit_game(quit)
            self.player_t('You', player_guess, self.computer_grid, self.computer_ships, user_col, self.player_tracker, self.player_called_points, self.player_name, self.player_win)
            self.is_game_over()
        quit = True
        return quit


    def is_game_over(self):
        if len(self.computer_ships) == len(self.player_win):
            print 'YOU WIN!!'
            print 'Computer:', self.computer_name.get_score()
            print '{}: {}'.format(self.player_name.get_name(), self.player_name.get_score())
            return True
        elif len(self.player_ships) == len(self.comp_win):
            print 'COMP WIN!!'
            print 'Computer:', self.computer_name.get_score()
            print '{}: {}'.format(self.player_name.get_name(), self.player_name.get_score())
            return True
        else:
            return False


    def __repr__(self):
        x_values = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        y_values = range(10)
        grid_string = [' '.join(x_values)]
        for row_index, row in enumerate(self.player_grid.public_grid()):
            row_values = map(lambda x: x.get_value(), row)
            grid_string.append(str(y_values[row_index]) + ' '+ ' '.join(row_values))
        return "\n".join(grid_string) + '\n'

def main():
    name = raw_input('Enter your player name:')
    player = Battleship(name)
    quit = player.player_turn()
    GamePlayer.quit_game(quit)



main()