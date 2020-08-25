
from abstract_rule import AbstractRule
from rule_sudoku import RuleSudoku
from rule_killer import RuleKiller
from rule_antiknight import RuleAntiknight

class RuleFactory:
    @staticmethod
    def buildRule(ruleDefinition: dict) -> AbstractRule:
        name = ruleDefinition['name']
        if name == 'sudoku':
            return RuleSudoku(ruleDefinition)
        elif name == 'killer':
            return RuleKiller(ruleDefinition)
        elif name == 'antiknight':
            return RuleAntiknight(ruleDefinition)
        else:
            print(f'@RuleFactory.buildRule: unknown rule name "{name}"')
        return None
