from point_class import Point

class MetaGrid(type):
    pass

class Grid(Point):
    __metaclass__ = MetaGrid

    def __init__(self, row, column):
        self._row = row
        self._column = column
        self._grid = self.create_grid()

        # super(Grid, self).__init__(x, y, value)

    def create_grid(self):
        grid = []
        for row_index in range(self._row):
            grid.append([])
            for column_index in range(self._column):
                grid[-1].append(Point(row_index, column_index, '.'))
        return grid

    def public_grid(self):
        return self._grid

    def pretty_grid(self):
        pass

    def __repr__(self):
        grid_string = []
        for row in self._grid:
            row_values = map(lambda x: x.get_value(), row)
            grid_string.append(' '.join(row_values))
        return "\n".join(grid_string) + '\n'


    def get_point(self, point):
        return self._grid[point.get_x()][point.get_y()]

    def set_point(self, point):
        self._grid[point.get_x()][point.get_y()] = point

def main():
    pass

main()
