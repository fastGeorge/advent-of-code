
class ModularArithmetic:

    def __init__(self, spokes:int, value:int):
        self.spokes = spokes
        self.value = value % spokes

    def mult(self, nbr:int):
        self.value = (self.value * nbr) % self.spokes

    def add(self, nbr:int):
        self.value = (self.value + nbr) % self.spokes

    def pow(self):
        self.value = (self.value * self.value) % self.spokes

class ModularList:

    def __init__(self, value:int):
        self.list = [ModularArithmetic(2, value), ModularArithmetic(3, value), ModularArithmetic(5, value), \
                        ModularArithmetic(7, value) , ModularArithmetic(11, value), ModularArithmetic(13, value), \
                        ModularArithmetic(17, value), ModularArithmetic(19, value), ModularArithmetic(23, value)]

    def isDivisible(self, denominator:int):
        mod = [i for i in self.list if i.spokes == denominator]
        return mod[0].value == 0