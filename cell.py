class Cell:

    def __init__(self, value):
        self.value = value
        self.isGiven = value != 0
        if not self.isGiven:
            self.candidates = list(range(1,10))
        else:
            self.candidates = []
