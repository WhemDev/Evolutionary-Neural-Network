import numpy as np

# Nöron sınıfı
class Neuron:
    def __init__(self, neuron_type, name):
        self.neuron_type = neuron_type
        self.name = name
        self.value = 0.0
        self.connections = []

    def connect(self, target_neuron, weight):
        if len(self.connections) < 24:  # Bağlantı sınırı
            self.connections.append((target_neuron, weight))

    def activate(self):
        if self.neuron_type != 'input':  # Input nöronları aktive olmaz
            total_input = sum(neuron.value * weight for neuron, weight in self.connections)
            print(f"{self.name} Total Input: {total_input}")
            self.value = np.tanh(total_input)  # -1.0 ile 1.0 arasında çıktı
            print(f"{self.name} Activated Value: {self.value}")

    # Bağlantıları ve ağırlıkları yazdırmak için bir fonksiyon
    def print_connections(self):
        print(f"Neuron {self.name} Connections:")
        for target_neuron, weight in self.connections:
            print(f"  -> {target_neuron.name} with weight {weight}")

# Neural Network sınıfı
class NeuralNetwork:
    def __init__(self, input_neurons, internal_neurons, output_neurons):
        self.input_neurons = input_neurons
        self.internal_neurons = internal_neurons
        self.output_neurons = output_neurons
        self.all_neurons = input_neurons + internal_neurons + output_neurons
        self.create_weighted_connections()

    def create_weighted_connections(self):
        # Input nöronlarını internal ve output nöronlarına bağla
        for neuron in self.input_neurons:
            # Bağlantı ağırlıklarını input nöronunun değerine göre belirle
            for target in self.internal_neurons + self.output_neurons:
                weight = np.clip(neuron.value * 4.0, -4.0, 4.0)  # -4.0 ile 4.0 arasında normalize et
                neuron.connect(target, weight)

        # Internal nöronları diğer internal ve output nöronlarına bağla
        for neuron in self.internal_neurons:
            for target in self.internal_neurons + self.output_neurons:
                weight = np.clip(neuron.value * 4.0, -4.0, 4.0)  # Internal nöronlar için de ağırlık belirle
                neuron.connect(target, weight)

    def set_input_values(self, input_data):
        for neuron in self.input_neurons:
            neuron.value = np.clip(input_data[neuron.name], -1.0, 1.0)  # -1.0 ile 1.0 arasında normalize et

    def feed_forward(self):
        for neuron in self.internal_neurons:
            neuron.activate()
        for neuron in self.output_neurons:
            neuron.activate()

    def print_all_connections(self):
        print("Printing all neuron connections and weights:")
        for neuron in self.all_neurons:
            neuron.print_connections()

# Agent sınıfı
class Agent:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.last_move_x = 0  # Son hareketin X bileşeni
        self.last_move_y = 0  # Son hareketin Y bileşeni

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
        # Input değerlerini ayarla ve network'ü çalıştır
        self.network.set_input_values(simulation_data)
        self.network.feed_forward()

        # Output nöronlarından gelen değerlere göre hareket et
        output_values = self.network.get_output_values()
        self.move(output_values)

    def move(self, output_values):
        # Hareket fonksiyonu
        if output_values['Mfd'] > 0.2:  # Eşik değeri
            self.Y = (self.Y + 1) % 64
            self.last_move_y = 1
        elif output_values['Mrv'] > 0.2:
            self.Y = (self.Y - 1) % 64
            self.last_move_y = -1
        else:
            self.last_move_y = 0

        if output_values['MX'] > 0.2:
            self.X = (self.X + 1) % 64
            self.last_move_x = 1
        elif output_values['MX'] < -0.2:
            self.X = (self.X - 1) % 64
            self.last_move_x = -1
        else:
            self.last_move_x = 0


agent = Agent(10, 20)

agent.network.print_all_connections()