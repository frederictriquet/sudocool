from cell import Cell
from tools import loadJson

class Grid:

    def __init__(self, givens):
        if isinstance(givens, str):
            givens = loadJson(givens)
        self.cells = []
        for givenRow in givens:
            row = []
            for givenValueChar in givenRow:
                if givenValueChar != ' ':
                    if givenValueChar == '.':
                        givenValueChar = '0'
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

    def showFull(self):
        for row in range(9):
            if row == 3 or row == 6:
                print("-"*33 + '-+-' + "-"*33 + '-+-' + '-'*33)
            print(" "*33 + ' | ' + " "*33 + ' | ' + ' '*33)
            for column in range(9):
                if column == 3 or column == 6:
                    print(' | ', end='')
                cell = self.getCell(row+1, column+1)
                value = cell.value
                if value == 0:
                    value = '[' + ''.join(map(str,cell.candidates)) + ']'
                elif cell.isGiven:
                    value = f'{value}.'
                print(f'{value:^11}', end = '')
            print('')
            print(" "*33 + ' | ' + " "*33 + ' | ' + ' '*33)

    # def isSolved(self) -> bool:
    #     return constraintsOK
    
    def isBroken(self) -> bool:
        for a in self.cells:
            for b in a:
                if b.value == 0 and len(b.candidates) == 0:
                    return True
        return False

    def promoteSingleCandidates(self) -> bool:
        hasPromoted = False
        for a in self.cells:
            for b in a:
                if b.value == 0 and len(b.candidates) == 1:
                    b.value = b.candidates[0]
                    hasPromoted = True
        return hasPromoted

  