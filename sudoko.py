from random import choice, choices


class Sudoko:
    def __init__(self, level):
        """
        level : hardness of the game
        grid contain sudoko puzzle data
        """
        self.level = level
        self.grid = self.initiate()
        self.move = []
        self.__omit()

    def initiate(self):
        """
        Initialize initial state of sudoko,
        sudoko board is generated by shuffling the data stored in grid
        and omitting some of them to get a solvable sudoku
        """
        grid = [[7, 3, 5, 6, 1, 4, 8, 9, 2],
                [8, 4, 2, 9, 7, 3, 5, 6, 1],
                [9, 6, 1, 2, 8, 5, 3, 7, 4],
                [2, 8, 6, 3, 4, 9, 1, 5, 7],
                [4, 1, 3, 8, 5, 7, 9, 2, 6],
                [5, 7, 9, 1, 2, 6, 4, 3, 8],
                [1, 5, 7, 4, 9, 2, 6, 8, 3],
                [6, 9, 4, 7, 3, 8, 2, 1, 5],
                [3, 2, 8, 5, 6, 1, 7, 4, 9]]

        # shuffling columns
        for _time in range(2):
            for i in range(3):
                [c1, c2] = choices([3 * i + 0, 3 * i + 1, 3 * i + 2], k=2)
                tmp = []
                for r in range(9):
                    tmp.append(grid[r][c1])
                    grid[r][c1] = grid[r][c2]
                for r in range(9):
                    grid[r][c2] = tmp[r]
        # shuffling rows
        for _time in range(2):
            for i in range(3):
                [r1, r2] = choices([3 * i + 0, 3 * i + 1, 3 * i + 2], k=2)
                tmp = grid[r1]
                grid[r1] = grid[r2]
                grid[r2] = tmp

        # shuffling 3 x 3 boxes
        for _time in range(2):
            [b1, b2] = choices([0, 1, 2], k=2)
            tmp1, tmp2, tmp3 = grid[b1 * 3], grid[b1 * 3 + 1], grid[b1 * 3 + 2]
            grid[b1 * 3] = grid[b2 * 3]
            grid[b1 * 3 + 1] = grid[b2 * 3 + 1]
            grid[b1 * 3 + 2] = grid[b2 * 3 + 2]
            grid[b2 * 3], grid[b2 * 3 + 1], grid[b2 * 3 + 2] = tmp1, tmp2, tmp3

        return grid

    def __omit(self):
        number = 30
        pair = [(i, j) for i in range(9) for j in range(9)]
        while number > 0:
            p = choice(pair)
            val = self.grid[p[0]][p[1]]
            self.grid[p[0]][p[1]] = -1
            if self.solvable() == False:
                self.grid[p[0]][p[1]] = val
            else:
                number -= 1
                pair.remove(p)


    def check(self):
        """
        Check the solved grid is correct or not
        """
        # checking rows and 3 x 3 boxes
        for r in range(9):
            if r % 3 == 0:
                box = [[False for i in range(10)],
                       [False for i in range(10)],
                       [False for i in range(10)]]
            row = [False for i in range(10)]
            for c in range(9):
                if row[self.grid[r][c]]:
                    print(f"{self.grid[r][c]} appear again in row {r + 1}")
                    return False
                row[self.grid[r][c]] = True
                box_idx = c // 3
                if box[box_idx][self.grid[r][c]]:
                    b = box_idx + r // 3 * 3
                    print(f"{self.grid[r][c]} appear again in box {b + 1}")
                    return False
                box[box_idx][self.grid[r][c]] = True
            for i in range(1, 10):
                if row[i] == False:
                    print(f"Missing {i} in row {r}")
                    return False
            if r % 3 == 2:
                for i in range(1, 10):
                    if box[0][i] == False or box[1][i] == False or box[2][i] == False:
                        print(f"Missing {i} in box {r // 3}")
                        return False

        # checking columns
        for c in range(9):
            col = [False for i in range(10)]
            for r in range(9):
                if col[self.grid[r][c]]:
                    print(f"{self.grid[r][c]} appear again in col {c + 1}")
                    return False
                col[self.grid[r][c]] = True
            for i in range(1, 10):
                if col[i] == False:
                    print(f"Missing {i} in column {c} ")
                    return False
        print("Valid")
        return True

    def reset(self):
        """
        Reset game to new begining
        """
        self.grid = self.initiate()
        self.__omit()

    def __check_row(self, r):
        """
        Check given row contains unique value or not
        """
        row = [False for i in range(10)]
        for c in range(9):
            if self.grid[r][c] == -1:
                continue
            if row[self.grid[r][c]]:
                return False
            row[self.grid[r][c]] = True
        return True

    def __check_column(self, c):
        """
        Check given column contains unique value or not
        """
        col = [False for i in range(10)]
        for r in range(9):
            if self.grid[r][c] == -1:
                continue
            if col[self.grid[r][c]]:
                return False
            col[self.grid[r][c]] = True
        return True

    def __check_box(self, r, c):
        """
        Check given 3x3 box contains unique value or not
        """
        box = [False for i in range(10)]
        r, c = r // 3 * 3, c // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.grid[r + i][c + j] == -1:
                    continue
                if box[self.grid[r + i][c + j]]:
                    return False
                box[self.grid[r + i][c + j]] = True
        return True

    def __backtrack(self, r, c):
        """
        Check given board is solvable or not
        return True when board is solvable
        otherwise False
        """
        if r == 8 and c == 8:
            if self.grid[r][c] != -1:
                if self.__check_row(r) and self.__check_column(c) and self.__check_box(r, c):
                    return True
                return False
            for v in range(1, 10):
                self.grid[r][c] = v
                if self.__check_row(r) and self.__check_column(c) and self.__check_box(r, c):
                    self.grid[r][c] = -1
                    return True
            self.grid[r][c] = -1
            return False

        for v in range(1, 10):
            self.grid[r][c] = v
            if self.__check_row(r) and self.__check_column(c) and self.__check_box(r, c):
                rr, cc = r, c
                while self.grid[rr][cc] != -1:
                    cc += 1
                    if rr == 8 and cc == 8:
                        self.grid[r][c] = -1
                        return self.__backtrack(rr, cc)
                    if cc == 9:
                        cc,  rr = 0, rr + 1
                if self.grid[rr][cc] == -1 and self.__backtrack(rr, cc):
                    self.grid[r][c] = -1
                    return True
            self.grid[r][c] = -1
        return False

    def solvable(self) -> bool:
        """
        Check given board is solvable or not
        return True when board is solvable
        otherwise False
        """
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != -1:
                    continue
                if self.__backtrack(r, c):
                    return True
                else:
                    return False
        return True

    def __str__(self):
        """
        Prettier printing
        """
        result = "\v\t┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓\n"
        middle = "\t┣───┼───┼───╂───┼───┼───╂───┼───┼───┫\n"
        bmiddle = "\t┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫\n"
        for r in range(9):
            s = "\t┃"
            for c in range(9):
                if self.grid[r][c] == -1:
                    s += "   "
                else:
                    s += " " + str(self.grid[r][c]) + " "
                if c % 3 == 2:
                    s += "┃"
                else:
                    s += "│"
            result += s + "\n"
            if r < 8:
                if r % 3 == 2:
                    result += bmiddle
                else:
                    result += middle
        result += "\t┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛\n"
        return result

    def set(self, r, c, val):
        if r > 8 or r < 0 or c < 0 or c > 8:
            print("Out of range")
            return
        self.grid[r][c] = val
        self.move.append((r, c))

    def get(self, r, c):
        if r > 8 or r < 0 or c < 0 or c > 8:
            print("Out of range")
            return
        return self.grid[r][c]

    def undo(self):
        if len(self.move) > 0:
            l = self.move[-1]
            self.grid[l[0]][l[1]] = -1
            self.move.remove(l)


if __name__ == "__main__":
    s = Sudoko(1)
    print(s)
    num = 10
    while num > 0:
        [r, c, val] = input(" : ").split()
        r = int(r)
        c = int(c)
        val = int(val)
        s.set(r, c, val)
        print(s)
        num -= 1
    print(s.check())
