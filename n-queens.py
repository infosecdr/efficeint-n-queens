#!/usr/bin/env python2

#  Jim Hoagland's solution to printing all solutions to 8 queens (Cracking the Coding Interview problem 8.12)

from collections import deque

class BoardPosition(object):
    """Represents a single position on the chess board"""
    def __init__(self, row, col):
        self.col = col
        self.row = row

    def __str__(self):
        return "({},{})".format(self.row, self.col)

class NQueensBoard(object):
    """A board with state tracking for N queens solving"""
    def __init__(self, n):
        self.n = n # board size
        self.ar = deque(range(0, n)) # avail rows
        self.ac = set(range(0, n)) # avail columns
        self.ud_used = [False for i in range(0, 2 * n - 1)] # up (positive) slope diagnals that have been used (index is c + r)
        self.dd_used = [False for i in range(0, 2 * n - 1)] # down (negative) slope diagnals that have been used (index is c - r + (n-1))
        self.placed = deque() # placed queens (instances of BoardPosition), in order of placement

    def __str__(self):
        return "\n".join([
            "N=" + str(self.n) + "; " + str([str(qp) for qp in self.placed]),
            "ar: " + str(self.ar),
            "ac: " + str(self.ac),
            "ud used: " + str(filter(lambda x: self.ud_used[x], xrange(0, len(self.ud_used)))),
            "dd used: " + str(filter(lambda x: self.dd_used[x], xrange(0, len(self.dd_used))))
        ])

    def up_diag_number_calc(self, bp):
        """calculate the up diagnal index for a board position"""
        return bp.row + bp.col
    def down_diag_number_calc(self, bp):
        """calculate the down diagnal index for a board position"""
        return (self.n - 1) + (bp.col - bp.row)

    def rows_avail(self):
        return len(self.ar)

    def all_avail_placements_in_an_avail_row(self):
        """given this board state, return a BoardPosition for valid placements of a queen in some single available row"""
        # possible TODO: make this into a generator
        if not self.ar:
            return None
        r = self.ar[0] # chose an available row

        valid_placements = []
        for c in self.ac: # for each available column
            qp = BoardPosition(r, c)
            if self.ud_used[self.up_diag_number_calc(qp)] or self.dd_used[self.down_diag_number_calc(qp)]:
                continue # not an avail position due to diagnal
            valid_placements.append(qp)
        return valid_placements

    def place_queen(self, qp):
        """place a queen on the board, updating state tracking"""
        #print "placing {}".format(qp)
        self.ar.remove(qp.row)
        self.ac.remove(qp.col)
        self.ud_used[self.up_diag_number_calc(qp)] = True
        self.dd_used[self.down_diag_number_calc(qp)] = True
        self.placed.append(qp)

    def unplace_last_queen(self):
        """unplace the most recently placed queen on the board, updating state tracking"""
        qp = self.placed.pop()
        #print "unplacing {}".format(qp)
        self.ar.appendleft(qp.row) # it doesn't matter if the row is put back in the original position
        self.ac.add(qp.col)
        # since the queen in qp was a valid placement, we know the diagnals are clear now
        self.ud_used[self.up_diag_number_calc(qp)] = False
        self.dd_used[self.down_diag_number_calc(qp)] = False

    def print_queens(self):
        print ', '.join([str(qp) for qp in self.placed])

def print_solns_for_board(b):
    """print all the solutions available given the current board state"""
    if b.rows_avail() > 0:
        for qp in b.all_avail_placements_in_an_avail_row():
            # for all queen positions in some new row...
            #print b
            b.place_queen(qp) # place queen on board
            print_solns_for_board(b)  # recurse with new board; may print some solutions
            b.unplace_last_queen() # remove last queen (the one we placed above) to allow us to try a different one
            # note: for case with i queens left to place on b, will recurse between 0 and i-1 times
    else:
        # all placed
        b.print_queens()


def print_n_queens_solns(n):
    if n < 0:
        return
    board = NQueensBoard(n)
    print_solns_for_board(board)

if __name__ == "__main__":
    print "8 queens solutions:"
    print_n_queens_solns(8)

    print "10 queens solutions:"
    print_n_queens_solns(10)

