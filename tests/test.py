import numpy as np

# TODO Remake the neuron connections and value assigning amk
# * 1.  Inputların ürettiği/sahip olduğu değerleri 0.0 ila 1.0 arasında olmasını sağla.
# * 2.  Neural connectionları oluştur : En fazla 12 connection olabilir. 
# * 3.  Calculate Connection values : Connection weight -4.0 to 4.0 * neuron output (Exp. Input neuron output => 0.4 * 3.4 <= Connection weight)
# * 4.  Calculate Internal and Action neuron's recieved values => tanh(sum(inputs)) => -1.0 to 1.0
# ! Note:   Internal Neurons Default value => 0.0

# Nöron sınıfı
class Neuron:
    def __init__(self, neuron_type, name):
        self.neuron_type = neuron_type
        self.name = name
        self.value = 0.0
        self.connections = []

    def connect(self, target_neuron, weight):
        self.connections.append((target_neuron, weight))

    def activate(self):
        if self.neuron_type != 'input':  # Input nöronları aktive olmaz

            total_input = sum(neuron.value * weight for neuron, weight in self.connections)

            self.value = np.tanh(total_input)  # -1.0 ile 1.0 arasında çıktı

    # Bağlantıları, ağırlıkları ve kendi değerini yazdırmak için bir fonksiyon
    def print_debug_info(self, output_neurons):
        output_connections = [conn for conn in self.connections if conn[0] in output_neurons]
        if output_connections:
            print(f"Neuron {self.name}: Value = {self.value}")
            for target_neuron, weight in output_connections:
                print(f"  -> Connected to {target_neuron.name} with weight {weight}")

# Neural Network sınıfı
class NeuralNetwork:
    def __init__(self, input_neurons, internal_neurons, output_neurons):
        # Define Neurons
        self.input_neurons = input_neurons
        self.internal_neurons = internal_neurons
        self.output_neurons = output_neurons
        self.all_neurons = input_neurons + internal_neurons + output_neurons
        self.create_limited_connections()

    def create_limited_connections(self):
        max_total_connections = 12  # Maximum possible connection count
        total_connections = 0

        # Output nöronlarına bağlantılar oluştur
        for output_neuron in self.output_neurons:
            # Check connection count
            if total_connections >= max_total_connections:
                break
            # Rastgele bir input veya internal nöron seç ve bağlan
            source_neuron = np.random.choice(self.input_neurons + self.internal_neurons)
            weight = np.clip(source_neuron.value * 4.0, -4.0, 4.0)  # Ağırlık kaynağın değerine göre
            source_neuron.connect(output_neuron, weight)
            total_connections += 1

        # Input ve internal nöronlar arasında kalan bağlantıları oluştur
        for neuron in self.input_neurons + self.internal_neurons:
            if total_connections >= max_total_connections:
                break
            # Rastgele bir hedef internal veya output nöronu seç
            target_neuron = np.random.choice(self.internal_neurons + self.output_neurons)
            weight = np.random.uniform(-4.0, 4.0)  # Rastgele ağırlıklar
            neuron.connect(target_neuron, weight)
            total_connections += 1

        self.total_connections = total_connections

    def set_input_values(self, input_data):
        for neuron in self.input_neurons:
            neuron.value = np.clip(input_data[neuron.name], -1.0, 1.0)  # -1.0 ile 1.0 arasında normalize et

    def feed_forward(self):
        for neuron in self.internal_neurons:
            neuron.activate()
        for neuron in self.output_neurons:
            neuron.activate()

    def get_output_values(self):
        return {neuron.name: neuron.value for neuron in self.output_neurons}

    # Debugging için toplam bağlantı sayısını ve output nöronlarına bağlantıları yazdır
    def print_debug_info(self):
        print(f"Total Connections: {self.total_connections}")
        print("Output Neuron Connections:")
        for neuron in self.all_neurons:
            neuron.print_debug_info(self.output_neurons)

# Agent sınıfı
class Agent:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.last_move_x = 0
        self.last_move_y = 0

        # Input neurons
        input_neurons = [
            Neuron('input', 'Lx'), Neuron('input', 'Ly'), Neuron('input', 'Age'),
            Neuron('input', 'Rnd'), Neuron('input', 'Blr'), Neuron('input', 'Bfd'),
            Neuron('input', 'Plr'), Neuron('input', 'Pfd'), Neuron('input', 'LMy'),
            Neuron('input', 'LMx'), Neuron('input', 'BDy'), Neuron('input', 'BDx'),
            Neuron('input', 'Gen'), Neuron('input', 'BDd'), Neuron('input', 'LPf')
        ]

        # 3 internal neurons
        internal_neurons = [Neuron('internal', f'N{i}') for i in range(3)]

        # Output/Action neurons
        output_neurons = [
            Neuron('output', 'Mfd'), Neuron('output', 'Mrn'), Neuron('output', 'Mrv'),
            Neuron('output', 'MX'), Neuron('output', 'MY')
        ]

        # ! Create Neural Network
        self.network = NeuralNetwork(input_neurons, internal_neurons, output_neurons)

    def update(self, simulation_data):
        self.network.set_input_values(simulation_data)
        self.network.feed_forward()

        # Debugging: Toplam bağlantı sayısını ve output nöronlarına bağlantıları yazdır
        self.network.print_debug_info()

        output_values = self.network.get_output_values()
        self.move(output_values)

    def move(self, output_values):
        if output_values['Mfd'] > 0.2:
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

# Simülasyon verilerini oluştur (örnek veriler)
simulation_data = {
    'Lx': 0.5,
    'Ly': -0.5,
    'Age': 0.3,
    'Rnd': -0.7,
    'Blr': 0.2,
    'Bfd': -0.3,
    'Plr': 0.1,
    'Pfd': -0.4,
    'LMy': 0.0,
    'LMx': 0.0,
    'BDy': 0.6,
    'BDx': -0.6,
    'Gen': 0.8,
    'BDd': -0.2,
    'LPf': 0.4
}

# Agent'ı oluştur ve güncelle
agent = Agent(10, 20)
agent.update(simulation_data)