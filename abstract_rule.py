import abc
from abc import ABC, abstractmethod

from constraint_manager import ConstraintManager
from grid import Grid
from subset_manager import SubsetManager
from tools import loadJson


class AbstractRule(ABC):
    def __init__(self, ruleDefinition: dict):
        self.name = ruleDefinition['name']
        self.loadRules(ruleDefinition['file'])

    @abstractmethod
    def apply(self, grid: Grid):
        pass

    def loadRules(self, rulesFilename: str):
        rules = loadJson(rulesFilename)
        if 'use subset files' in rules:
            self.loadSubsets(rules['use subset files'])
        for constraintsForSubset in rules['constraints']:
            self.loadConstraintsForSubset(constraintsForSubset)
        # print("SUBSETS")
        # print(ConstraintManager.subsets)
    
    def loadConstraintsForSubset(self, constraintsForSubset):
        subset = constraintsForSubset['subset']
        for constraint in constraintsForSubset['constraints']:
           ConstraintManager.addConstraintToSubset(constraint, subset) 
    
    # def loadConstraint(self, constraint: dict):
    #     ConstraintManager.addConstraintToSubsets(constraints['constraint'], constraints['apply to subsets'])
        # print("CONSTRAINTS")
        # print(ConstraintManager.constraints)

    def loadSubsets(self, subsetFilenames : list):
        for subsetFilename in subsetFilenames:
            SubsetManager.loadSubset(subsetFilename)
