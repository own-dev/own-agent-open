"""
Describes elements' geometry for boards
"""


class Point:
    """
    2D point representing the element on the own's board

    x: int([0; MAX_BOARD_X))
    y: int([0; MAX_BOARD_Y))
    """

    def __init__(self, x: int = 0, y: int = 0, min_x: int = 0, min_y: int = 0, max_x: int = 6, max_y: int = 8):
        # TODO: Grab min-max values ONCE from a board
        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y

        if min_x <= x <= max_x:
            self._x = x
        else:
            raise ValueError('X should be in interval [{}; {}), but current value is {}'
                             .format(self._min_x, self._max_x, x))
        if min_y <= y <= max_y:
            self._y = y
        else:
            raise ValueError('Y should be in interval [{}; {}), but current value is {}'
                             .format(self._min_y, self._max_y, y))

    def __str__(self):
        return '({}; {})'.format(self.x, self.y)

    def __repr__(self):
        return '<{0}.{1} object at {2}>'.format(self.__module__, type(self).__name__, hex(id(self)))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    @property
    def x(self):
        """
        Point's projection on abscissa
        :return: int
        """
        return self._x

    @x.setter
    def x(self, new_val):
        if not self._min_x <= new_val <= self._max_x:
            raise ValueError('Should be in range [{}; {}]'.format(self._min_x, self._max_x))
        self._x = new_val

    @property
    def y(self):
        """
        Point's projection on ordinate
        :return: int
        """
        return self._y

    @y.setter
    def y(self, new_val):
        if not self._min_y <= new_val <= self._max_y:
            raise ValueError('Should be in range [{}; {})'.format(self._min_y, self._max_y))
        self._y = new_val


class Rectangle:
    """
    Rectangle, the main figure on the board
    Can be created at least with one Point(x_start; y_start), or with x,y-shifts, or with an end-point
    Rectangle can become a point if shifts are 0, and start-point equals to end-point.
    """

    # TODO: Make Rect's variables Points, not multiple integers
    def __init__(self, x_start, y_start, x_shift=None, y_shift=None, x_end=None, y_end=None):
        assert isinstance(x_start, int), 'Input parameters for Rectangle should be integers'
        assert isinstance(y_start, int), 'Input parameters for Rectangle should be integers'

        self._x_start = x_start
        self._y_start = y_start

        if x_shift:
            self._x_shift = x_shift
            self._x_end = x_start + x_shift - 1
        elif x_end:
            self._x_end = x_end
            self._x_shift = self._x_end - self._x_start + 1
        else:
            self._x_end = self._x_start
            self._x_shift = 1

        if y_shift:
            self._y_shift = y_shift
            self._y_end = y_start + y_shift - 1
        elif y_end:
            self._y_end = y_end
            self._y_shift = self._y_end - self._y_start + 1
        else:
            self._y_end = self._y_start
            self._y_shift = 1

        self._len = self._x_shift * self._y_shift
        self._is_correct()
        self.i = self._x_start
        self.j = self._y_start

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self._x_end:
            self.i += 1
        elif self.j < self._y_end:
            self.i = self._x_start
            self.j += 1
        else:
            raise StopIteration
        return Point(self.i, self.j)

    def __len__(self):
        return self._len

    def _recalculate(self):
        self._x_shift = self._x_start - self._x_end + 1
        self._y_shift = self._y_start - self._y_end + 1
        self._len = self._x_shift * self._y_shift
        self._is_correct()

    def _is_correct(self):
        """Checks if Start doesn't intersect with End, soft constrain"""
        if self._x_start > self._x_end or self._y_start > self._y_end:
            raise ValueError('Wrong input data for a Rect: from ({}; {}) to ({}; {}).'
                             .format(self._x_start, self._y_start, self._x_end, self._y_end))
        return True

    @property
    def start(self):
        """
        Topmost, leftmost rectangle's point. Start Point
        :return:
        """
        return Point(self._x_start, self._y_start)

    @start.setter
    def start(self, rhd_val):
        assert isinstance(rhd_val, Point), 'Righthand parameter should be Point'
        self._x_start = rhd_val.x
        self._y_start = rhd_val.y
        self._recalculate()

    @property
    def end(self):
        """
        Botmost, rightmost rectangle's point. End Point
        :return:
        """
        return Point(self._x_end, self._y_end)

    @end.setter
    def end(self, rhd_val):
        assert isinstance(rhd_val, Point), 'Righthand parameter should be Point'
        self._x_end = rhd_val.x
        self._y_end = rhd_val.y
        self._recalculate()

    @property
    def width(self):
        """
        x, abscissa
        :return:
        """
        return self._x_shift

    @property
    def height(self):
        """
        y, ordinate
        :return:
        """
        return self._y_shift


class AllocationGrid:
    """
    Allocation grid representing free/occupied board's elements

    False, 0 – free
    True,  1 – occupied
    """

    def __init__(self, board):
        sizes = board.get_board_size()
        self._max_size_x = sizes['sizeX']
        self._max_size_y = sizes['sizeY']

        # TODO: Make it booleans
        self._grid = board.get_elements_matrix()

    @property
    def grid(self):
        """
        Getter
        :return:
        """
        return self._grid

    @property
    def max_x(self):
        """Current board's horizontal elements length"""
        return self._max_size_x

    @property
    def max_y(self):
        """Current board's vertical elements length"""
        return self._max_size_y

    def is_free(self, i, j):
        """
        Checks if ij-th element is free
        :param i: Column-number, integer interval is [1; max_x]
        :param j: Row-number, integer interval is [1; max_y]
        :return: True if free, False if occupied, None if out of borders
        """
        if i < 0 or j < 0:
            raise IndexError('There is no cell ({}; {}) on the board. Indices start with 0.'
                             .format(i, j))
        if i > self.max_x or j > self.max_y:
            raise IndexError('There is no cell ({}; {}) on the board. Maximums are {} and {}'
                             .format(i, j, self._max_size_x, self._max_size_y))
        if self._grid[i][j]:
            return False
        return True

    def is_occupied(self, i, j):
        """
        Checks whether ij-th element is occupied
        :param i: Column-number, integer interval is [1; max_x]
        :param j: Row-number, integer interval is [1; max_y]
        :return: True if occupied, False if free, None if out of borders
        """
        if i < 0 or j < 0:
            raise IndexError('There is no cell ({}; {}) on the board. Indices start with 0.'
                             .format(i, j))
        if i > self.max_x or j > self.max_y:
            raise IndexError('There is no cell ({}; {}) on the board. Maximums are {} and {}'
                             .format(i, j, self._max_size_x, self._max_size_y))
        if self._grid[i][j]:
            return True
        return False

    def cell_state(self, i, j):
        """
        Returns the state of the ij-th grid's cell
        :param i: Column-number, integer interval is [1; max_x]
        :param j: Row-number, integer interval is [1; max_y]
        :return: True – occupied, False – free, None – out of border
        """
        if i > self.max_x or j > self.max_y:
            return None
        return True if self._grid[i][j] else False

    def is_area_free(self, start, end):
        """
        Checks if given rectangular area is free
        :param start: Point:
        :param end: Point:
        :return: True, if every single-piece element is free, False otherwise;
                 None, if input data is incorrect
        """
        assert isinstance(start, Point), 'Start parameter {} is not a Point'.format(start)
        assert isinstance(end, Point), 'End parameter {} is not a Point'.format(end)

        # TODO: rework it to Rect.is_free()
        for i in range(start.x, end.x):
            for j in range(start.y, end.y):
                if self.is_occupied(i, j):
                    return False
        return True

    def _free(self, i, j):
        """
        Frees the ij-th element
        :param i:
        :param j:
        :return:
        """
        self._grid[i][j] = False
        return True

    def _occupy(self, i, j):
        """
        Occupies the ij-th element
        :param i:
        :param j:
        :return:
        """
        if not self._grid[i][j]:
            self._grid[i][j] = True
            return True
        return False

    def allocate(self, start, end=None):
        """
        Occupies the certain rectangle area
        :param start:
        :param end:
        :return: True if succeeded, False otherwise; None – out of borders
        """
        # Check if the Points are correct
        if not check_point_correct(start):
            return None

        if end is None:
            return self._occupy(start.x, start.y)
        elif not check_point_correct(end):
            return None

        for i in range(start.x, end.x):
            for j in range(start.y, end.y):
                if not self._occupy(i, j):
                    return False
        return True

    def deallocate(self, start, end=None):
        """
        Frees either single-piece element, or the given area
        :param start:
        :param end:
        :return: True if succeded, False otherwise
        """
        # Check if the Points are correct
        if not check_point_correct(start):
            return False

        if end is None:
            self._free(start.x, start.y)
            return True
        else:
            if not check_point_correct(end):
                return False

        for i in range(start.x, end.x):
            for j in range(start.y, end.y):
                self._free(i, j)
        return True


def check_point_correct(point):
    """
    Checks whether the point_i_j exists on the grid
    I.e., correct indices
    :param point:
    :return: True if everything's correct, False otherwise
    """
    assert isinstance(point, Point), '{} is not a Point'.format(point)

    if point.x < 0 or point.y < 0:
        return False

    # TODO: Grab constrains from the Board
    if point.x > 7 or point.y > 9:
        return False

    return True
