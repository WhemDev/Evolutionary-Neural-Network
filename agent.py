import random

from input_neurons import *
from output_neurons import *

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
            'Mrv': Mrv('Mrv')   # Mrv class from output_neurons
        }

        # Combine all neurons
        self.all_neurons = (
            list(self.input_neurons.values())
            + self.internal_neurons
            + list(self.output_neurons.values())
        )

        # Create random connections

        print("NEURONS: ")
        print(self.input_neurons)
        print(self.internal_neurons)
        print(self.output_neurons)
        print(self.all_neurons)

        # Create random connections
        self.create_random_connections()

    def create_random_connections(self):
        # Connect input neurons to output neurons as per the given rule
        input_neurons = list(self.input_neurons.values())
        output_neurons = list(self.output_neurons.values())
        print("connection")
        print(input_neurons)
        print(output_neurons)
        for neuron in input_neurons:
            print(neuron.name)
            targets = random.sample(output_neurons, k=random.randint(1, len(output_neurons)))
            print(targets)
            for target in targets:
                print(target.name)
                weight = random.uniform(-1, 1)
                neuron.connect(target, weight)
                print("Neuron connections: ", neuron.connections)

    def activate_network(self):
        # Set input neuron values from the agent's data
        self.input_neurons['Lx'].value = self.X  # Normalizing X coordinate
        self.input_neurons['Ly'].value = self.Y  # Normalizing Y coordinate
        print("input neurons")

        print(self.input_neurons['Lx'].value)
        print(self.input_neurons['Ly'].value)
        # Activate internal and output neurons
        for neuron in self.internal_neurons + list(self.output_neurons.values()):
            neuron.activate()

    def move(self):
        move_x = 0
        move_y = 0
        # Use output neurons to determine movement
        print(self.output_neurons['Mrn'])
        if self.output_neurons['Mrn'].value:
            print(self.output_neurons['Mrn'].name)
            if self.output_neurons['Mrn'].direction == 'north': move_y = 1
            elif self.output_neurons['Mrn'].direction == 'south': move_y = -1
            elif self.output_neurons['Mrn'].direction == 'east': move_x = 1
            elif self.output_neurons['Mrn'].direction == 'west': move_x = -1

        
        if self.output_neurons['Mrv'].value: move_x = -1
        print(self.X, self.Y)
        # Update agent's position
        self.X = (self.X + move_x) % 128
        self.Y = (self.Y + move_y) % 128
        print(self.X, self.Y)

    def update(self):
        # Activate the network and then move
        self.activate_network()
        self.move()

agent= Agent(['Lx', 'Ly'], ['Mrn', 'Mrv'])
agent.update()
agent.update()
agent.update()
agent.update()
agent.update()