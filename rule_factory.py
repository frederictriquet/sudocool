
from abstract_rule import AbstractRule
from rule_sudoku import RuleSudoku
from rule_killer import RuleKiller

class RuleFactory:
    @staticmethod
    def buildRule(ruleDefinition: dict) -> AbstractRule:
        name = ruleDefinition['name']
        if name == 'sudoku':
            return RuleSudoku(ruleDefinition)
        if name == 'killer':
            return RuleKiller(ruleDefinition)
        return None
