import numpy as np
import random
from neuralNetwork import NeuralNetwork
from neuron import Neuron

class Agent:
    def __init__(self, x, y, grid):
        self.X = x
        self.Y = y

        self.survived = False
        self.genome = ""

        self.grid = grid
        self.last_move_x = 0
        self.last_move_y = 0

        # Input neurons
        input_neurons = [
            Neuron('input', 'Lx'), Neuron('input', 'Ly'), Neuron('input', 'Age'),
            Neuron('input', 'Rnd'), 
            Neuron('input', 'Plr'), Neuron('input', 'Pfd'), Neuron('input', 'LMy'),
            Neuron('input', 'LMx'), Neuron('input', 'BDy'), Neuron('input', 'BDx'),
            Neuron('input', 'BDd'), Neuron('input', 'LPf')
        ]
       
        # 3 internal neurons
        internal_neurons = [Neuron('internal', f'N{i}') for i in range(3)]

        # assing the default internal neuron value (1.0)
        for internal in internal_neurons:
            internal.value = 1.0

        # Output/Action neurons
        output_neurons = [
            Neuron('output', 'Mfd'), Neuron('output', 'Mrn'), Neuron('output', 'Mrv'),
            Neuron('output', 'MX'), Neuron('output', 'MY')
        ]

        # ! Create Neural Network
        self.network = NeuralNetwork(input_neurons, internal_neurons, output_neurons)

        # connections to genome
        self.Con2Gen(self.network.connections)

        self.grid[self.Y-1][self.X-1] = 1

    def Con2Gen(self, connections):
        for connection in connections:
            # inputname-weight-outputname\n
            self.genome += f'{connection[0].name} ' + f'{connection[2]} ' + f'{connection[1].name}' + '-'+f'{connection[0].value}' +' '+ f'{connection[1].value}'+'\n'

    def update(self, simulation_data):
        self.network.set_input_values(simulation_data)
        self.network.feed_forward()

        # Debugging: Toplam bağlantı sayısını ve output nöronlarına bağlantıları yazdır
        # self.network.print_debug_info()

        self.output_values = self.network.get_output_values()
        self.move(self.output_values)


    # OUTPUT NEURONS : 
    #   DONE  Mfd - move forward
    #   DONE  Mrn - move random
    #   DONE  Mrv - move reverse
    #   DONE  MX - move east/west (+/-)
    #   DONE  MY - move north/south (+/-)

    def move(self, output_values):
        new_x, new_y = self.X, self.Y
        if output_values['Mrn'] > 0:
            directions = ['n', 'e', 's', 'w']
            choice = np.random.choice(directions)
            if choice == 'n':
                new_y += 1
            if choice == 'e':
                new_x= self.X + 1
            if choice == 's':
                new_y += -1
            if choice == 'w':
                new_x = self.X - 1

        if output_values['Mfd'] > 0:
            new_x = self.X + 1

        if output_values['Mrv'] > 0:
            new_x = self.X - 1
            
        if output_values['MX'] > 0:
            new_x= self.X + 1
            
        if output_values['MX'] < -0:
            new_x = self.X - 1
            
        if output_values['MY'] > 0:
            new_y += 1
            
        if output_values['MY'] < -0:
            new_y += -1
        
        # Çakışmayı önlemek için pozisyon kontrolü
        if (0 <= new_x <= 64) and (0 <= new_y <= 64):
            if (self.grid[new_y-1][new_x-1] == 0):  # 64 ten yüksek mi kontrol
                #calculate last move   30 -> 31 = +1  yeni - eski
                self.last_move_x = new_x - self.X
                self.last_move_y = new_y - self.Y

                self.grid[self.Y-1][self.X-1] = 0  # Eski pozisyonu boşalt
                self.X, self.Y = new_x, new_y  # Yeni pozisyona geç
                self.grid[self.Y-1][self.X-1] = 1  # Yeni pozisyonu işaretle
                return
        self.last_move_x = 0
        self.last_move_y = 0

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
grid = [[0 for _ in range(64)] for _ in range(64)]
## Agent'ı oluştur ve güncelle
agent = Agent(33, 30, grid)
print(agent.genome)
agent.update(simulation_data)