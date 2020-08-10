
class ConstraintManager:
    # constraints = {}
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
        # print(constraint)
        if subset not in ConstraintManager.subsets:
            ConstraintManager.subsets[subset] = []
        ConstraintManager.subsets[subset].append(constraint)