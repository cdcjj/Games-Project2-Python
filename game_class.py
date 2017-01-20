class MetaGame(type):
    pass

class Game(object):
    __metaclass__ = MetaGame

    def player_turn(self):
        pass
    def is_game_over(self):
        pass