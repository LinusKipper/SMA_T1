class PseudoRandomNumbers:
    def __init__(self, seed: int):
        self.seed = seed
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.count = 0  

    def next(self) -> float:
        self.seed = (self.a * self.seed + self.c) % self.m
        self.count += 1
        return self.seed / self.m

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.next()
