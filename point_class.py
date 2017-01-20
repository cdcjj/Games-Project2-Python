class Point(object):
    def __init__(self,  x = 0 , y = 0, value = ''):                      # constructor
        # private instance attributes: x and y, default values = 0
        self._x = x
        self._y = y
        self._value = value

    # Getters
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_value(self):
        return self._value

    # Setters
    def set_x(self, x):
       self._x = x

    def set_y(self, y):
        self._y = y

    def set_value(self, value):
        self._value = value

    def __repr__(self):
         return "({},{}),{}".format(self._x, self._y, self._value)


def main():
    pass

main()