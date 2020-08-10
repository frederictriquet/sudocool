from cell import Cell

class Grid:

    def __init__(self, givens : list):
        # self.cells = [ [ Cell() for x in range(9)] for y in range(9) ]
        self.cells = []
        for givenRow in givens:
            row = []
            for givenValueChar in givenRow:
                givenValue = int(givenValueChar)
                row.append(Cell(givenValue))
            self.cells.append(row)

    def getCell(self, sudoku_row: int, sudoku_column: int):
        if sudoku_row < 1 or 9 < sudoku_row or sudoku_column < 1 or 9 < sudoku_column:
            return None
        return self.cells[sudoku_row-1][sudoku_column-1]

    def setValue(self, sudoku_row: int, sudoku_column: int, value: int):
        cell = self.getCell(sudoku_row, sudoku_column)
        if cell:
            cell.value = value

    def show(self):
        for row in range(9):
            if row == 3 or row == 6:
                print("-"*6 + '+' + "-"*7 + '+' + '-'*6)
            for column in range(9):
                if column == 3 or column == 6:
                    print('| ', end='')
                cell = self.getCell(row+1, column+1)
                value = cell.value
                if value == 0:
                    value = '.'
                print(f'{value} ', end='')
            print('')
