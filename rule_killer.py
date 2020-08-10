from abstract_rule import AbstractRule
from grid import Grid

class RuleKiller(AbstractRule):
    def __init__(self, ruleDefinition: object):
        super().__init__(ruleDefinition)

    def apply(self, grid: Grid):
        print('apply killer rule')
        