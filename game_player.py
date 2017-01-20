class MetaGamePlayer(type):
    pass

class GamePlayer(object):
    __metaclass__ = MetaGamePlayer
    def __init__(self, name = '', quit = False):
        self._name = name
        self._score = 0
        # self._quit = GamePlayer.quit_game(quit)

    @staticmethod
    def quit_game(quit):
        if quit== True:
            print ''
            print 'Thank you for playing'
            print 'Quitting Game'
            raise SystemExit
        return ''

    def get_name(self):
        return self._name

    def get_score(self):
        return self._score

    def set_name(self,name):
        self._name = name

    def set_score(self, number):
        self._score += number

    def __repr__(self):
        return "Player name: \t\t {}\n"\
               "Score:       \t\t {}\n".format(self._name, self._score)




