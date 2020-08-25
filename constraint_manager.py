
class ConstraintManager:
    constraints = {}
    subsets = {}

    # @staticmethod
    # def addConstraintToSubsets(constraint: str, subsets: list):
    #     if constraint not in ConstraintManager.constraints:
    #         ConstraintManager.constraints[constraint] = set(subsets)
    #     else:
    #         ConstraintManager.constraints[constraint].update(subsets)
    #     for subset in subsets:
    #         if subset not in ConstraintManager.subsets:
    #             ConstraintManager.subsets[subset] = set()
    #         ConstraintManager.subsets[subset].add(constraint)
    
    @staticmethod
    def addConstraintToSubset(constraint: object, subset: str):
        print(f'{subset} <- {constraint}')
        if subset not in ConstraintManager.subsets:
            ConstraintManager.subsets[subset] = []
        ConstraintManager.subsets[subset].append(constraint)

        constraintName = constraint['name']
        if constraintName not in ConstraintManager.constraints:
            ConstraintManager.constraints[constraintName] = set()
        ConstraintManager.constraints[constraintName].add(subset)
    
    @staticmethod
    def dump():
        print('Subsets')
        print(ConstraintManager.subsets)
        print('Constraints')
        print(ConstraintManager.constraints)
    
    @staticmethod
    def getSpecificConstraint(subsetName: str, constraintName: str) -> dict:
        return next((c for c in ConstraintManager.subsets[subsetName] if c['name'] == constraintName), None)