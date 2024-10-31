import random
import numpy as np

# Nöron sınıfı
class Neuron:
    def __init__(self, neuron_type, name):
        self.neuron_type = neuron_type  # 'input', 'internal', 'output'
        self.name = name
        self.value = 0.0
        self.connections = []  # Bağlantılar (hedef nöron ve ağırlık)

    def connect(self, target_neuron, weight):
        if len(self.connections) < 24:  # Bağlantı sınırı 24
            self.connections.append((target_neuron, weight))

    def activate(self):
        if self.neuron_type != 'input':  # Input nöronları aktive olmaz
            total_input = sum(neuron.value * weight for neuron, weight in self.connections)
            self.value = np.tanh(total_input)  # Aktivasyon fonksiyonu

# Neural Network sınıfı
class NeuralNetwork:
    def __init__(self, input_neurons, internal_neurons, output_neurons):
        self.input_neurons = input_neurons
        self.internal_neurons = internal_neurons
        self.output_neurons = output_neurons
        self.all_neurons = input_neurons + internal_neurons + output_neurons
        self.create_random_connections()

    def create_random_connections(self):
        for neuron in self.input_neurons:
            targets = random.sample(self.internal_neurons + self.output_neurons, k=random.randint(1, 3))
            for target in targets:
                weight = random.uniform(-1, 1)
                neuron.connect(target, weight)

        for neuron in self.internal_neurons:
            targets = random.sample(self.internal_neurons + self.output_neurons, k=random.randint(1, 3))
            for target in targets:
                weight = random.uniform(-1, 1)
                neuron.connect(target, weight)

    def set_input_values(self, input_data):
        for neuron, value in zip(self.input_neurons, input_data):
            neuron.value = np.clip(value, -4.0, 4.0)

    def feed_forward(self):
        for neuron in self.internal_neurons + self.output_neurons:
            neuron.activate()

    def get_output_values(self):
        return {neuron.name: neuron.value for neuron in self.output_neurons}

# Agent sınıfı
class Agent:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

        # Input nöronlarını oluştur
        input_neurons = [
            Neuron('input', 'Lx'), Neuron('input', 'Ly'), Neuron('input', 'Age'), 
            Neuron('input', 'Rnd'), Neuron('input', 'Blr'), Neuron('input', 'Bfd'), 
            Neuron('input', 'Plr'), Neuron('input', 'Pfd'), Neuron('input', 'LMy'), 
            Neuron('input', 'LMx'), Neuron('input', 'BDy'), Neuron('input', 'BDx'), 
            Neuron('input', 'Gen'), Neuron('input', 'BDd'), Neuron('input', 'LPf')
        ]

        # 3 internal nöron
        internal_neurons = [Neuron('internal', f'H{i}') for i in range(3)]

        # Output nöronlarını oluştur
        output_neurons = [
            Neuron('output', 'Mfd'), Neuron('output', 'Mrn'), Neuron('output', 'Mrv'),
            Neuron('output', 'MX'), Neuron('output', 'MY')
        ]

        # Neural Network oluştur
        self.network = NeuralNetwork(input_neurons, internal_neurons, output_neurons)

    def update(self, simulation_data):
        # Input nöronlarını simülasyon verileriyle besle
        input_values = [
            self.X, self.Y, simulation_data['Age'], random.uniform(-4.0, 4.0),  # Rnd
            simulation_data['Blr'], simulation_data['Bfd'], simulation_data['Plr'],
            simulation_data['Pfd'], simulation_data['LMy'], simulation_data['LMx'],
            simulation_data['BDy'], simulation_data['BDx'], simulation_data['Gen'],
            simulation_data['BDd'], simulation_data['LPf']
        ]
        self.network.set_input_values(input_values)

        # Neural Network'ü çalıştır
        self.network.feed_forward()

        # Output nöronlarını al ve agent'ı hareket ettir
        output_values = self.network.get_output_values()
        self.move(output_values)

    def move(self, output_values):
        if output_values['Mfd'] > 0.5:  # Move forward
            self.Y = (self.Y + 1) % 128
        if output_values['Mrn'] > 0.5:  # Move random
            self.X = (self.X + random.choice([-1, 1])) % 128
        if output_values['Mrv'] > 0.5:  # Move reverse
            self.Y = (self.Y - 1) % 128
        if output_values['MX'] > 0:  # Move east
            self.X = (self.X + 1) % 128
        elif output_values['MX'] < 0:  # Move west
            self.X = (self.X - 1) % 128
        if output_values['MY'] > 0:  # Move north
            self.Y = (self.Y + 1) % 128
        elif output_values['MY'] < 0:  # Move south
            self.Y = (self.Y - 1) % 128