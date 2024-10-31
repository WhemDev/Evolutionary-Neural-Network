import random
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
            self.value = np.tanh(total_input)  # tanh aktivasyon fonksiyonu
            print(f"{self.name} Activated Value: {self.value}")

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
        self.create_random_connections()

    def create_random_connections(self):
        # Input nöronlarını internal ve output nöronlarına bağla
        for neuron in self.input_neurons:
            targets = random.sample(self.internal_neurons + self.output_neurons, k=random.randint(1, 3))
            for target in targets:
                weight = random.uniform(-1, 1)
                neuron.connect(target, weight)

        # Internal nöronları diğer internal ve output nöronlarına bağla
        for neuron in self.internal_neurons:
            targets = random.sample(self.internal_neurons + self.output_neurons, k=random.randint(1, 3))
            for target in targets:
                weight = random.uniform(-4, 4)
                neuron.connect(target, weight)

    def set_input_values(self, input_data):
        print("NEURON DATA")
        for neuron in self.input_neurons:
            neuron.value = np.clip(input_data[neuron.name], -4.0, 4.0)
            print("neuron name: ", neuron.name)
            print("neuron value: ", neuron.value)
            

    # Neural Network sınıfında feed_forward fonksiyonunu güncelle
    def feed_forward(self):
        for neuron in self.internal_neurons:
            neuron.activate()
            print(f"Internal Neuron {neuron.name} Value: {neuron.value}")  # Internal nöron değerlerini yazdır

        for neuron in self.output_neurons:
            neuron.activate()
            print(f"Output Neuron {neuron.name} Value: {neuron.value}")  # Output nöron değerlerini yazdır

    def get_output_values(self):
        return {neuron.name: neuron.value for neuron in self.output_neurons}

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
        # Lx ve Ly değerlerini simülasyon boyutuna göre normalize et
        Lx_value = (self.X / 64) * 8 - 4  # 0-64 arası X değerini -4 ile 4 arasına çevir
        Ly_value = (self.Y / 64) * 8 - 4  # 0-64 arası Y değerini -4 ile 4 arasına çevir

        # Diğer input nöronları için de uygun atamaları yap
        input_data = {
            'Lx': Lx_value,
            'Ly': Ly_value,
            'Age': (simulation_data['Age'] / 200) * 8 - 4,  # Yaşı normalize et
            'Rnd': random.uniform(-4, 4),  # Rastgele bir input
            'Blr': simulation_data['Blr'],  # Sol-sağ engel bilgisi
            'Bfd': simulation_data['Bfd'],  # İleri engel bilgisi
            'Plr': simulation_data['Plr'],  # Sol-sağ popülasyon gradyanı
            'Pfd': simulation_data['Pfd'],  # İleri popülasyon gradyanı
            'LMy': self.last_move_y,  # Son hareketin Y bileşeni
            'LMx': self.last_move_x,  # Son hareketin X bileşeni
            'BDy': (self.Y / 64) * 8 - 4,  # Kuzey-güney sınır mesafesini normalize et
            'BDx': (self.X / 64) * 8 - 4,  # Doğu-batı sınır mesafesini normalize et
            'Gen': simulation_data['Gen'],  # Genetik benzerlik
            'BDd': (min(self.Y, 64 - self.Y, self.X, 64 - self.X) / 64) * 8 - 4,  # En yakın sınır mesafesi
            'LPf': simulation_data['LPf']  # Uzun mesafeli ileri popülasyon
        }

        # Neural Network'ü input verileriyle çalıştır
        self.network.set_input_values(input_data)
        self.network.feed_forward()

        # Output nöronlarından gelen değerlere göre hareket et
        output_values = self.network.get_output_values()
        print("OUTPUT VALUES: ")
        print(output_values)
        self.move(output_values)
          

    def check_blockage_left_right(self, simulation_data):
        # Sol-sağ engel kontrolü (örnek hesaplama)
        return simulation_data['Blr']

    def check_blockage_forward(self, simulation_data):
        # İleri engel kontrolü (örnek hesaplama)
        return simulation_data['Bfd']

    def calculate_population_gradient_left_right(self, simulation_data):
        # Sol-sağ popülasyon gradyanı (örnek hesaplama)
        return simulation_data['Plr']

    def calculate_population_gradient_forward(self, simulation_data):
        # İleri popülasyon gradyanı (örnek hesaplama)
        return simulation_data['Pfd']

    def calculate_long_range_population_forward(self, simulation_data):
        # Uzun mesafeli ileri popülasyon (örnek hesaplama)
        return simulation_data['LPf']

    def move(self, output_values):
        # Hareket fonksiyonu
        if output_values['Mfd'] > 0.5:  # Move forward
            self.Y = (self.Y + 1) % 64
            self.last_move_y = 1
        elif output_values['Mrv'] > 0.5:  # Move reverse
            self.Y = (self.Y - 1) % 64
            self.last_move_y = -1
        else:
            self.last_move_y = 0

        if output_values['MX'] > 0:  # Move east
            self.X = (self.X + 1) % 64
            self.last_move_x = 1
        elif output_values['MX'] < 0:  # Move west
            self.X = (self.X - 1) % 64
            self.last_move_x = -1
        else:
            self.last_move_x = 0

        if output_values['Mrn'] > 0.5:  # Move random
            direction = random.choice(['north', 'south', 'east', 'west'])
            if direction == 'north':
                self.Y = (self.Y + 1) % 64
            elif direction == 'south':
                self.Y = (self.Y - 1) % 64
            elif direction == 'east':
                self.X = (self.X + 1) % 64
            elif direction == 'west':
                self.X = (self.X - 1) % 64