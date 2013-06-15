#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import random


class Same_M(object):
    """
    The same-game model that manages the game state.
    """

    def __init__(self, cols, rows, values, seed=None):
        """
        A new game model cols wide, rows high, and using the
        given list of values.\n\nAn optional seed offers replayability.
        """

        self.cols = cols
        self.rows = rows
        self.score = 0
        # listeners get notified of model events
        self.listeners = []
        # allow replaying the same game
        if seed:
            random.seed(seed)
        # fill the matrix with random choices
        self.matrix = [[random.choice(values) for x in range(cols)]
            for y in range(rows)]

    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, event_name, data):
        for listener in self.listeners:
            listener(event_name, data)

    def get_neighbours(self, row, col):
        """
        Get a matrix of neighbor cells, and their neighbors.
        """

        # do not select zero values
        if self.matrix[row][col] == 0:
            return None

        # we use a local func to ease code reuse.
        def mark_hotspots(row, col, n_row, n_col):
            # test for a neighboring match
            if self.matrix[row][col] == self.matrix[n_row][n_col]:
                # neighbor n_ equals in value
                hotspot = (n_row, n_col)
                # we use the tested list to avoid stacking
                # the same cell twice
                if not hotspot in tested:
                    # mark current cell as hot
                    matches[n_row][n_col] = 1
                    # add this hotspot to the stack
                    # so it's neighbors get tested
                    stack.append(hotspot)
                    # remember not to check this cell in the future
                    tested.append(hotspot)

        # start with an empty matrix
        matches = [[0 for x in range(self.cols)]
                    for y in range(self.rows)]
        # starting cell is selected
        matches[row][col] = 1
        # ... and tested
        tested = [(row, col)]
        # ... and in the stack for testing (we need to start somewhere)
        stack = [(row, col)]
        # while there are cells to test for friendly neighbors
        while len(stack) > 0:
            # test the four cardinal points around this cell.
            row, col = stack.pop()
            # west / left
            if (col > 0):
                mark_hotspots(row, col, row, col - 1)
            # east / right
            if (col < self.cols - 1):
                mark_hotspots(row, col, row, col + 1)
            # north / above
            if (row > 0):
                mark_hotspots(row, col, row - 1, col)
            # south / below
            if (row < self.rows - 1):
                mark_hotspots(row, col, row + 1, col)
        # this clever piece counts how many 1's in each matrix row,
        # then sums up the resulting list to get how many number 1's we have.
        if sum([row.count(1) for row in matches]) > 1:
            return matches
        else:
            return None

    def __remove_matches(self, matches):
        # zero out matches
        for r in range(self.rows):
            for c in range(self.cols):
                if matches[r][c] == 1:
                    self.matrix[r][c] = 0

    def __shift_down(self):
        """
        shift matrix rows down, from the bottom up
        to fill empty spaces. think of it as gravity
        making blocks fall into empty spaces below.
        """

        for c in range(self.cols - 0):
            # as we test a cell to the one below it, start at the 2nd last row.
            r = self.rows - 2
            while r > -1:
                # if this cell has a value, and the one below is empty
                if self.matrix[r][c] > 0 and self.matrix[r + 1][c] == 0:
                    # switch their values
                    self.matrix[r + 1][c] = self.matrix[r][c]
                    self.matrix[r][c] = 0
                    # tell any listeners
                    self.notify('drop_cell', [[r, c], [r + 1, c]])
                    # move the counter down, essentially testing the cell
                    # we just dropped, but in its new position.
                    if r < self.rows - 2:
                        r = r + 1
                else:
                    # nothing to move now. climb up the rows until we find
                    # a cell to drop, or we hit the top.
                    r = r - 1

    def __shift_left(self):
        """
        shift matrix colums left to take up empty spaces.
        """

        def isempty(col):
            """test if a column has no values."""
            for row in range(0, self.rows):
                if self.matrix[row][col] > 0:
                    return False
            return True

        def copyleft(col):
            """copy the column values across."""
            for row in range(0, self.rows):
                self.matrix[row][col] = self.matrix[row][col + 1]
                self.matrix[row][col + 1] = 0
        # test each column from the left
        col = 0
        while col < self.cols - 1:
            if isempty(col) and not isempty(col + 1):
                copyleft(col)
                col = 0
            else:
                col = col + 1

    def select_blocks(self, row, col):
        m = self.get_neighbours(row, col)
        if m:
            self.score = self.score + self.calc_score(m)
            self.__remove_matches(m)
            self.__shift_down()
            self.__shift_left()

    def calc_score(self, matches):
        count = 0
        for row in matches:
            count = count + row.count(1)
        return count * 2

if __name__ == "__main__":

    def print_matrix(mx, words=''):
        print("")
        for i in range(len(mx)):
            if i == 1:
                print('%s   %s' % (mx[i], words))
            else:
                print(mx[i])

    def test_selection():
        s = Same_M(4, 4, [7, 8], 1)
        print_matrix(s.matrix, 'initial state')

        m = s.get_neighbours(3, 2)
        if m:
            print_matrix(m, 'match neighbors at (3, 2)')

        s.select_blocks(3, 2)
        print_matrix(s.matrix, 'remove selection')

        m = s.get_neighbours(3, 0)
        if m:
            print_matrix(m, 'match next at (0, 3)')

        s.select_blocks(3, 0)
        print_matrix(s.matrix, 'remove selection')

    def test_recursion():
        s = Same_M(4, 4, [7, 8], 1)
        m = s.get_neighbours(3, 2)
        if m:
            print_matrix(m, 'matches at (2, 3) via stack')

        m = s.get_neighbours(3, 2)
        if m:
            print_matrix(m, 'matches via recursion')
    #test_recursion()
    test_selection()
