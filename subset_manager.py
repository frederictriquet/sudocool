from tools import loadJson
from grid import Grid
class SubsetManager:

    loadedSubsetFilenames = set()
    subsets = {}

    @staticmethod
    def loadSubset(subsetFilename):
        if subsetFilename not in SubsetManager.loadedSubsetFilenames:
            # print(f'load {subsetFilename}')
            subsets = loadJson(subsetFilename)
            for subset in subsets:
                name = subset['name']
                cells = SubsetManager.buildCells(subset['cells'])
                SubsetManager.subsets[name] = cells
                SubsetManager.loadedSubsetFilenames.add(subsetFilename)
        # print(SubsetManager.subsets)
    
    @staticmethod
    def buildCells(flatCells: list) -> list:
        itr = iter(flatCells)
        return [ [x,y] for x,y in zip(itr,itr) ]

    @staticmethod
    def initGridSubset():
        SubsetManager.subsets['grid'] =  [ [x,y] for x in range(1,10) for y in range(1,10) ]

    @staticmethod
    def cellDefinitionsOf(subsetName: str):
        for cellDefinition in SubsetManager.subsets[subsetName]:
            yield cellDefinition[0], cellDefinition[1]

    @staticmethod
    def cellsOf(grid: Grid, subsetName: str):
        for row, column in SubsetManager.cellDefinitionsOf(subsetName):
            cell = grid.getCell(row, column)
            if cell:
                yield cell

    @staticmethod
    def cellsWithValueOf(grid: Grid, subsetName: str):
        for cell in SubsetManager.cellsOf(grid, subsetName):
            if cell.value > 0:
                yield cell
