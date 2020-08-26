import copy
from grid import Grid
from tools import loadJson
from rule_factory import RuleFactory
from constraint_manager import ConstraintManager
from subset_manager import SubsetManager
import itertools
# import sys

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
        if 'grid' in ConstraintManager.subsets:
            SubsetManager.initGridSubset()
        ConstraintManager.dump()
        # sys.exit()

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
        # while not self.gridIsSolved(): # and not self.gridIsBroken():
        #     cell = self.findFreeCell()
        #     if cell is None:
        #         print('cannot find free cell')
        #         break
        #     cell.value = cell.value + 1
        #     if cell.value == 10:
        #         print('cannot find a value')
        #         break

        #     self.currentGrid = copy.deepcopy(self.currentGrid)
        #     self.statusStack.append({ 'grid': self.currentGrid, 'row': self.currentRow, 'column': self.currentColumn})
        #     print(f'stack = {len(self.statusStack)}')

        loop = 0
        while self.applyConstraints() or self.currentGrid.promoteSingleCandidates():
            if self.currentGrid.isBroken():
                status = 'B'
            elif self.gridIsSolved():
                status = 'S'
            else:
                status = '.'
            print(f'{status}', end='', flush=True)
            loop += 1
            if loop % 2000 == 0:
                print()
                self.currentGrid.showFull()

        if self.currentGrid.isBroken():
            print("\nBROKEN")
        elif self.gridIsSolved():
            print("\nSOLVED")
        else:
            print("\nNOT SOLVED")
        print(f'{loop} loops')
        self.currentGrid.showFull()

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
        for subsetName in ConstraintManager.subsets:
            # print(f'processing {subset}')
            for constraint in ConstraintManager.subsets[subsetName]:
                constraintResult = self.verifyConstraint(constraint, subsetName)
                # print(f'   {constraint} -> {constraintResult}')
                if not constraintResult:
                    result = False
                    return result
        return result
    
    def verifyConstraint(self, constraint: dict, subsetName: str) -> bool:
        if constraint['name'] == 'no duplicates':
            return self.verifyNoDuplicates(subsetName)
        elif constraint['name'] == 'all 9':
            return self.verifyAll9(subsetName)
        elif constraint['name'] == 'sum equals to value':
            return self.verifySumEqualsToValue(subsetName, constraint['value'])
        else:
            print(f'unknown constraint {constraint} applied on subset {subsetName}')
            return False

    def verifyNoDuplicates(self, subsetName: str) -> bool:
        values = set()
        for cellDefinition in SubsetManager.subsets[subsetName]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                if cell.value in values:
                    return False
                else:
                    values.add(cell.value)
        return True
    
    def verifyAll9(self, subsetName: str) -> bool:
        values = { x: False for x in range(1,10) }
        for cellDefinition in SubsetManager.subsets[subsetName]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                values.pop(cell.value, 0)
        return len(values) == 0
    
    def verifySumEqualsToValue(self, subsetName: str, value: int) -> bool:
        sum = 0
        for cellDefinition in SubsetManager.subsets[subsetName]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                sum = sum + cell.value
        return sum == value


    def applyConstraints(self) -> bool:
        areValuesRemoved = False

        if 'grid' in ConstraintManager.subsets:
            for constraint in ConstraintManager.subsets['grid']:
                areValuesRemoved = areValuesRemoved or self.applyGridConstraintRestriction(constraint)

        # TODO permutter les 2 boucles
        for constraintName in ConstraintManager.constraints:
            for subsetName in ConstraintManager.constraints[constraintName]:
                constraint = ConstraintManager.getSpecificConstraint(subsetName, constraintName)
        # for subsetName in ConstraintManager.subsets:
        #     for constraint in ConstraintManager.subsets[subsetName]:
                # print(constraint)
                areValuesRemoved = areValuesRemoved or self.applyConstraintRestriction(constraint, subsetName)
        return areValuesRemoved

    def applyGridConstraintRestriction(self, constraint: dict) -> bool:
        areValuesRemoved = False
        if constraint['name'] == 'antiknight':
            areValuesRemoved = areValuesRemoved or self.removeValuesFromCandidateAtKnightPosition()
        return areValuesRemoved

    def removeValuesFromCandidateAtKnightPosition(self) -> bool:
        for cellDefinition in SubsetManager.subsets['grid']:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                for targetRow, targetColumn in self.getKnightTargets():
                    targetCell = self.currentGrid.getCell(cellDefinition[0] + targetRow, cellDefinition[1] + targetColumn)
                    if targetCell and targetCell.value == 0 and cell.value in targetCell.candidates:
                        targetCell.candidates.remove(cell.value)

    def getKnightTargets(self):
        yield -2,-1
        yield -2, 1
        yield -1, 2
        yield  1, 2
        yield  2, 1
        yield  2,-1
        yield  1,-2
        yield -1,-2


    def applyConstraintRestriction(self, constraint: dict, subsetName: str) -> bool:
        areValuesRemoved = False
        # print(constraint)
        if constraint['name'] == 'no duplicates':
            areValuesRemoved = areValuesRemoved or self.removeValuesFromCandidate(subsetName)
            if not areValuesRemoved:
                areValuesRemoved = areValuesRemoved or self.promoteHiddenSingles(subsetName)
            if not areValuesRemoved:
                areValuesRemoved = areValuesRemoved or self.spotAndRemoveTuples(subsetName)
        return areValuesRemoved
    
    def removeValuesFromCandidate(self, subsetName: str) -> bool:
        values = set()
        areValuesRemoved = False
        # print(f'{subset}')
        for cellDefinition in SubsetManager.subsets[subsetName]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value > 0:
                values.add(cell.value)
        
        for cellDefinition in SubsetManager.subsets[subsetName]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell and cell.value == 0:
                previousLen = len(cell.candidates)
                cell.candidates = list(set(cell.candidates) - values)
                cell.candidates.sort()
                if previousLen > len(cell.candidates):
                    areValuesRemoved = True

        return areValuesRemoved

    def promoteHiddenSingles(self, subsetName: str) -> bool:
        areValuesRemoved = False
        counts = [ [] for i in range(10) ]
        for cellDefinition in SubsetManager.subsets[subsetName]:
            cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
            if cell.value == 0:
                for value in cell.candidates:
                    counts[value].append(cell)
        for value in range(1,10):
            if len(counts[value]) == 1:
                cell = counts[value][0]
                cell.value = value
                areValuesRemoved = True
                # print(f'hidden single found in {subsetName}: {cell.candidates} -> {value}')
                # print('*',end='')
        return areValuesRemoved

    def spotAndRemoveTuples(self, subsetName: str) -> bool:
        areValuesRemoved = False
        for size in range(2,9):
            areValuesRemoved = areValuesRemoved or self.spotTuple(subsetName, size)
        return areValuesRemoved

    def spotTuple(self, subsetName: str, size: int) -> bool:
        areValuesRemoved = False
        subset = SubsetManager.subsets[subsetName]
        for cellNumbers in itertools.combinations(range(len(subset)),size):
            values = set()
            selectedCellNumbers = set()
            for cellNumber in cellNumbers:
                cellDefinition = subset[cellNumber]
                cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
                if cell.value == 0:
                    values.update(cell.candidates)
                    selectedCellNumbers.add(cellNumber)
            if len(values) == size and len(selectedCellNumbers) == size:
                res = self.removeTupleFromSubset(values,selectedCellNumbers, subset)
                if res:
                    areValuesRemoved = True
        return areValuesRemoved


    def removeTupleFromSubset(self, valuesToRemove: set, protectedCellNumbers: list, subset: list):
        areValuesRemoved = False
        for index, cellDefinition in enumerate(subset):
            if index not in protectedCellNumbers:
                cell = self.currentGrid.getCell(cellDefinition[0], cellDefinition[1])
                if cell.value == 0:
                    previousLen = len(cell.candidates)
                    cell.candidates = list(set(cell.candidates) - valuesToRemove)
                    cell.candidates.sort()
                    if previousLen > len(cell.candidates):
                        areValuesRemoved = True

        return areValuesRemoved
