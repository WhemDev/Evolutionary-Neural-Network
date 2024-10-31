# OUTPUT NEURONS : 
# Mfd - move forward
# Mrn - move random
# Mrv - move reverse
# MX - move east/west (+/-)
# MY - move north/south (+/-)

import numpy as np
from neurons import *

# Mfd - move forward
class Mfd(Neuron):
    def __init__(self, name,type="Output", input = 0):
        super().__init__("Mfd","Output")
        totalWeight = 0
        count = 0
        for connection in self.connections:
            count+=1
            totalWeight += connection[1]

        self.weigt = totalWeight/count
        
        if np.where(self.weight): self.activate
    def activate(self):
        self.value = np.where(input)

# Mrn - move random - (-/+) if - do not activate if + self activate
class Mrn(Neuron):
    def __init__(self, name,type = "Output",  input = 0):
        super().__init__("Mrn","Output")
        self.input = input
        if np.where(input): self.activate
    def activate(self):
        self.value = np.where(input)
        self.direction = random.choice(['north', 'east', 'south', 'west'])

# Mrv - move reverse
class Mrv(Neuron):
    def __init__(self, name,type="Output", input=0):
        super().__init__("Mrv", "Output")
        self.input = input
        if np.where(input): self.activate
    def activate(self):
        self.value = np.where(input)

# MX - move east/west (+/-)
class MX(Neuron):
    def __init__(self, name,type="Output", input=0):
        super().__init__("MX","Output")
        self.input = input
        if np.where(input): self.activate
    def activate(self):
        self.value = np.where(input)
        if np.where(input): self.direction = 'east' 
        else: self.direction = 'west'

# MY - move north/south (+/-)
class MY(Neuron):
    def __init__(self, name,type="Output", input=0):
        super().__init__("MY","Output")
        self.input = input
        if np.where(input): self.activate
    def activate(self):
        self.value = np.where(input)
        if np.where(input): self.direction = 'north' 
        else: self.direction = 'south'


