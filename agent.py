import random

from input_neurons import *
from output_neurons import *


# ! DONT USE 
# ! EDIT /TEST FOLDER


class Agent:
    def __init__(self, input_names, output_names, internal_count=1):
        self.spawnX = random.randint(0, 128)
        self.spawnY = random.randint(0, 128)
        self.X = self.spawnX
        self.Y = self.spawnY
        self.age = 0

        # Create neurons
        self.input_neurons = {name: Neuron("input", name) for name in input_names}

        # Create internal neurons
        self.internal_neurons = [Neuron("internal", f"N{i}") for i in range(internal_count)]


        # Create output neurons with their specific classes
        self.output_neurons = {
            'Mrn': Mrn('Mrn'),  # Mrn class from output_neurons
            'Mrv': Mrv('Mrv'),
            'Mfd': Mfd('Mfd'),
            'MX': MX('MX'),
            'MY': MY('MY')
        }

        # Combine all neurons
        self.all_neurons = (
            list(self.input_neurons.values())
            + self.internal_neurons
            + list(self.output_neurons.values())
        )

        # Create random connections
        self.create_random_connections()

    def create_random_connections(self):
        # Connect input neurons to output neurons as per the given rule
        input_neurons = list(self.input_neurons.values())
        output_neurons = list(self.output_neurons.values())
        for neuron in input_neurons:
            targets = random.sample(output_neurons, k=random.randint(1, len(output_neurons)))

            for target in targets:
                weight = random.uniform(-1, 1)
                neuron.connect(target, weight)
                print("connection: ")
                print(target, weight)
            print("neuron connections ")
            print(neuron.connections)

    def activate_network(self):
        # Set input neuron values from the agent's data
        self.input_neurons['Lx'].value = self.X  # Normalizing X coordinate
        self.input_neurons['Ly'].value = self.Y  # Normalizing Y coordinate
        
        # Activate internal and output neurons
        for neuron in self.internal_neurons + list(self.output_neurons.values()):
            neuron.activate()

    def move(self, all_positions):
        move_x = 0
        move_y = 0

        # Mrn
        if self.output_neurons['Mrn'].value:
            if self.output_neurons['Mrn'].direction == 'north': move_y = 1
            elif self.output_neurons['Mrn'].direction == 'south': move_y = -1
            elif self.output_neurons['Mrn'].direction == 'east': move_x = 1
            elif self.output_neurons['Mrn'].direction == 'west': move_x = -1

        # Mrv
        if self.output_neurons['Mrv'].value: move_x = -1

        # MX
        if self.output_neurons['MX'].value:
            if self.output_neurons['MX'].direction == 'east': move_x = 1
            elif self.output_neurons['MX'].direction == 'west': move_x = -1
        # MY
        if self.output_neurons['MY'].value:
            if self.output_neurons['MY'].direction == 'north': move_y = 1
            elif self.output_neurons['MY'].direction == 'south': move_y = -1

        # Mfd
        if self.output_neurons['Mfd'].value: move_x = 1


        print(self.X, self.Y)
        # Update agent's position
        new_x = (self.X + move_x) 
        new_y = (self.Y + move_y)

        if 0 <= new_x < 128 and 0 <= new_y < 128:
        # Yeni pozisyon başka bir agent ile çakışıyor mu kontrol et
            if (new_x, new_y) not in all_positions:
                # Eski pozisyonu setten kaldırmadan önce kontrol et
                if (self.X, self.Y) in all_positions:
                    all_positions.remove((self.X, self.Y))  # Eski pozisyonu kaldır
                # Yeni pozisyonu ekle
                self.X = new_x
                self.Y = new_y
                all_positions.append((self.X, self.Y))

        print("moved")
        print(self.X, self.Y)

    def update(self, all_positions):
        # Activate the network and then move
        self.activate_network()
        self.move(all_positions)


agent = Agent(['Lx', 'Ly'], ["Mfd", "Mrn", "Mrv", "MX", "MY"])
agent.update([])
agent.update([])

# Case 1: 
# MRN - MX - MY +1 +1 x2