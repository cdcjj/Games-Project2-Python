from grid_class import Grid, MetaGrid
from point_class import Point
from game_class import Game, MetaGame
from game_player import GamePlayer, MetaGamePlayer

class MetaConnect(MetaGrid, MetaGame, MetaGamePlayer):
    pass

class Connect_4(Grid, Game):
    __metaclass__ = MetaConnect

    def __init__(self, name1, name2):
        self.board = Grid(6, 7)
        self.win = 4
        self.player_1 = GamePlayer(name1)
        self.player_2 = GamePlayer(name2)
        self.play_1_pieces = []
        self.play_2_pieces = []
        self.all_pieces = self.play_1_pieces + self.play_2_pieces

    def choose_column(self):
        try:
            column_choice = int(raw_input('Enter the column(0-6) you would like to add your piece to: '))

        except ValueError:
            print 'you must enter a numerical number (0-6) for the column index'
            column_choice = int(raw_input('Enter the column(0-6) you would like to add your piece to: '))

        if column_choice not in range(7):
            print 'the column you entered is not in range (0-6)'
            column_choice, quit = self.choose_column()
        quit_game = raw_input('Would you like to quit the game (yes or no) ').lower()
        if quit_game == 'yes':
            quit = True
        else:
            quit = False

        return column_choice, quit

    def place_point(self,row_index,chosen_column):
        pone_pt = Point(row_index, chosen_column, 'X')
        ptwo_pt = Point(row_index, chosen_column, 'O')
        if self.board.get_point(pone_pt) in self.play_1_pieces or self.board.get_point(ptwo_pt) in self.play_2_pieces:
            row_index -= 1
            if row_index < 0:
                print 'Column full, need to choose another column'
                column_index, quit = self.choose_column()
                row_ind = 5
                return self.place_point(row_ind, column_index)
            else:
                return self.place_point(row_index, chosen_column)
        else:
            return row_index, chosen_column

    def player_turn(self):
        while self.is_game_over() == False:
            row_index = 5
            print '{} choose column:'.format(self.player_1.get_name())
            p_one_column, quit = self.choose_column()
            GamePlayer.quit_game(quit)
            one_row, one_column = self.place_point(row_index, p_one_column)
            play_1_point = Point(one_row, one_column, 'X')
            self.board.set_point(play_1_point)
            self.play_1_pieces.append(play_1_point)
            print self.pretty_board()
            if self.is_game_over() == True:
                break

            row_index = 5
            print '{} choose column: '.format(self.player_2.get_name())
            p_two_column, quit = self.choose_column()
            GamePlayer.quit_game(quit)
            two_row, two_column = self.place_point(row_index, p_two_column)
            play_2_point = Point(two_row, two_column, 'O')
            self.board.set_point(play_2_point)
            self.play_2_pieces.append(play_2_point)
            print self.pretty_board()
            self.is_game_over()
            if self.is_game_over() == True:
                break
        quit = True
        return quit

    def check_if_win(self, player, orientation):
        if player == 'Player_1':
            move_list = self.play_1_pieces
            piece = 'X'
            name = self.player_1.get_name()
        else:
            move_list = self.play_2_pieces
            piece = 'O'
            name = self.player_2.get_name()
        for row in range(6):
            for col in range(7):
                if orientation == 'horizontal':
                    list_points = [Point(row, col, piece), Point(row, col + 1, piece),
                                   Point(row, col + 2, piece),Point(row, col + 3, piece)]
                elif orientation == 'vertical':
                    list_points = [Point(row, col, piece), Point(row + 1, col, piece),
                                   Point(row + 2, col, piece), Point(row + 3, col, piece)]
                elif orientation == 'diag up':
                    list_points = [Point(row, col, piece), Point(row - 1, col + 1, piece),
                                   Point(row - 2, col + 2, piece), Point(row - 3, col + 3, piece)]
                elif orientation == 'diag down':
                    list_points = [Point(row, col, piece), Point(row + 1, col + 1, piece),
                                   Point(row + 2, col + 2, piece), Point(row + 3, col + 3, piece)]

                score = 0
                for point in list_points:
                    try:
                        if self.board.get_point(point) in move_list:
                            score += 1
                        else:
                            score += 0
                    except IndexError:
                        score += 0
                if score == 4:
                    print '{} WINS!!'.format(name)
                    print 'Connect 4 at: {}'.format(list_points)
                    return True
        return False

    def is_game_over(self):
        player1 = 'Player_1'
        player2 = 'Player_2'
        orien_v = 'vertical'
        orien_h = 'horizontal'
        orien_up = 'diag up'
        orien_dwn = 'diag down'
        if self.check_if_win(player1, orien_v):
            return True
        elif self.check_if_win(player2, orien_v):
            return True
        elif self.check_if_win(player1, orien_h):
            return True
        elif self.check_if_win(player2, orien_h):
            return True
        if self.check_if_win(player1, orien_up):
            return True
        elif self.check_if_win(player2, orien_up):
            return True
        if self.check_if_win(player1, orien_dwn):
            return True
        elif self.check_if_win(player2, orien_dwn):
            return True

        return False

    def pretty_board(self):
        x_values = ['0', '1', '2', '3', '4', '5', '6']
        grid_string = [' '.join(x_values)]
        for row_index, row in enumerate(self.board.public_grid()):
            row_values = map(lambda x: x.get_value(), row)
            grid_string.append(' '.join(row_values))
        return "\n".join(grid_string) + '\n'

    def __repr__(self):
        x_values = ['0','1','2','3','4','5','6']
        grid_string = [' '.join(x_values)]
        for row_index, row in enumerate(self.board.public_grid()):
            row_values = map(lambda x: x.get_value(), row)
            grid_string.append(' '.join(row_values))
        return "\n".join(grid_string) + '\n'

def main():
    name1 = raw_input('Enter the name of player 1:')
    name2 = raw_input('Enter the name of player 2:')
    play = Connect_4(name1, name2)
    print play
    quitting = play.player_turn()
    GamePlayer.quit_game(quitting)

main()