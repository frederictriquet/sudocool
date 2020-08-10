from tools import loadJson


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

