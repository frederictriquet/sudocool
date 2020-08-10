import json, copy
from grid import Grid
from tools import loadJson
from rule_factory import RuleFactory
from constraint_manager import ConstraintManager
from subset_manager import SubsetManager

class Solver:
    def __init__(self, puzzleFileName: str):
        puzzleDefinition = loadJson(puzzleFileName)
        self.initialGrid = Grid(puzzleDefinition['givens'])
        self.currentGrid = copy.deepcopy(self.initialGrid)
        self.currentRow = 1
        self.currentColumn = 1
        self.statusStack = []
        self.statusStack.append({ 'grid': self.currentGrid, 'row': self.currentRow, 'column': self.currentColumn})
        self.rules = self.loadRules(puzzleDefinition['rules'])

    # def processSubsets(self, subsets: list):
    #     for subset in subsets:
    #         print(f'{subset["name"]}')

    def loadRules(self, rules: list) -> list:
        result = []
        for ruleDefinition in rules:
            rule = RuleFactory.buildRule(ruleDefinition)
            if rule != None:
                result.append(rule)
        return result

    def run(self):
        while not self.gridIsSolved(): # and not self.gridIsBroken():
            cell = self.findFreeCell()
            if cell is None:
                print('cannot find free cell')
                break
            cell.value = cell.value + 1
            if cell.value == 10:
                print('cannot find a value')
                break

            self.currentGrid = copy.deepcopy(self.currentGrid)
            self.statusStack.append({ 'grid': self.currentGrid, 'row': self.currentRow, 'column': self.currentColumn})
            print(f'stack = {len(self.statusStack)}')

        if self.gridIsSolved():
            print("SOLVED")
            self.currentGrid.show()
        else:
            print("NOT SOLVED")
            self.currentGrid.show()

    def findFreeCell(self):
        cell = self.currentGrid.getCell(self.currentRow, self.currentColumn)
        while cell and cell.isGiven:
            self.currentRow, self.currentColumn = self.nextCell(self.currentRow, self.currentColumn)
            cell = self.currentGrid.getCell(self.currentRow, self.currentColumn)
            print(self.currentRow, self.currentColumn)
        return cell


    def nextCell(self, row, column):
        if column == 9:
            c = 1
            r = row + 1
        else:
            c = column + 1
            r = row
        if r == 10:
            return 0,0
        return r,c

    def gridIsSolved(self) -> bool:
        constraintsOK = self.checkConstraints()
        # print(f'ALL CONSTRAINTS ARE OK: {constraintsOK}')
        return constraintsOK
    
    def checkConstraints(self) -> bool:
        result = True
        for subset in ConstraintManager.subsets:
            # print(f'processing {subset}')
            for constraint in ConstraintManager.subsets[subset]:
                constraintResult = self.verifyConstraint(constraint, subset)
                # print(f'   {constraint} -> {constraintResult}')
                if not constraintResult:
                    result = False
                    return result
        return result
    
    def verifyConstraint(self, constraint: dict, subset: str) -> bool:
        if constraint['name'] == 'no duplicates':
            return self.verifyNoDuplicates(subset)
        elif constraint['name'] == 'all 9':
            return self.verifyAll9(subset)
        elif constraint['name'] == 'sum equals to value':
            return self.verifySumEqualsToValue(subset, constraint['value'])
        else:
            print(f'unknown constraint {constraint} applied on subset {subset}')
            return False

    def verifyNoDuplicates(self, subset: str) -> bool:
        values = set()
        for cellDefinition in SubsetManager.subsets[subset]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                if cell.value in values:
                    return False
                else:
                    values.add(cell.value)
        return True
    
    def verifyAll9(self, subset: str) -> bool:
        values = { x: False for x in range(1,10) }
        for cellDefinition in SubsetManager.subsets[subset]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                values.pop(cell.value, 0)
        return len(values) == 0
    
    def verifySumEqualsToValue(self, subset: str, value: int) -> bool:
        sum = 0
        for cellDefinition in SubsetManager.subsets[subset]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                sum = sum + cell.value
        return sum == value
