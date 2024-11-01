# INPUT NEURONS :
# Age - age
# Rnd - random input
# Blr - blockage left right
# Bfd - blockage forward
# Pop - population density
# Plr - population gradient left right
# Pfd - population gradient forward
# LPf - population long-range forward
# LMy - last movement Y
# LMx - last movement X
# LBf - blockage longrange forward
# BDy - north/south border distance
# BDx - esat/west border distance
# Gen - genetic similarity of forward neighbor
# Lx - east/west world locaion
# Ly - north/south world location
# BDd - nearest border distance
# BDd nearest border location

from neurons import *
from input_neurons import *


# ! DONT USE 
# ! EDIT /TEST FOLDER


class Age(Neuron):
    def __init__(self, name,type, age_value):
        super().__init__("Age", 'input', name)
        self.age_value = age_value

    def activate(self):
        self.value = self.age_value

class Rnd(Neuron):
    def __init__(self, name, type):
        super().__init__("Rnd", 'input', name)
        self.Rnd_value = random.random()
    def activate(self):
        self.value = self.Rnd_value

# Lx - east/west world locaion
class Lx(Neuron):
    def __init__(self, name, type):
        super().__init__("Lx",'input', name)
        self.value = 0

class Ly(Neuron):
    def __init__(self, name, type):
        super().__init__("Ly",'input', name)
        self.value = 0

