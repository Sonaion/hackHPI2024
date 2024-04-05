class Consumption:
    def __init__(self, values: list):
        self.values = values
        self.max = max(values)
        self.min = min(values)
        self.total = sum(values)