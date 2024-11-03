import numpy as np
import random
from NeuralNetwork import NeuralNetwork
from Neuron import Neuron

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

        self.grid[self.Y-1][self.X-1] = 1

    def update(self, simulation_data):
        self.network.set_input_values(simulation_data)
        self.network.feed_forward()

        # Debugging: Toplam bağlantı sayısını ve output nöronlarına bağlantıları yazdır
        # self.network.print_debug_info()

        output_values = self.network.get_output_values()
        self.move(output_values)


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
            
        if output_values['MX'] > 0.3:
            new_x= self.X + 1
            
        if output_values['MX'] < -0.3:
            new_x = self.X - 1
            
        if output_values['MY'] > 0.3:
            new_y += 1
            
        if output_values['MY'] < -0.3:
            new_y += -1
        
        # Çakışmayı önlemek için pozisyon kontrolü
        if (0 <= new_x <= 63) and (0 <= new_y <= 63):
            if (self.grid[new_y][new_x] == 0):  # 64 ten yüksek mi kontrol
                #calculate last move   30 -> 31 = +1  yeni - eski
                self.last_move_x = new_x - self.X
                self.last_move_y = new_y - self.Y

                self.grid[self.Y][self.X] = 0  # Eski pozisyonu boşalt
                self.X, self.Y = new_x, new_y  # Yeni pozisyona geç
                self.grid[self.Y][self.X] = 1  # Yeni pozisyonu işaretle
                return
        self.last_move_x = 0
        self.last_move_y = 0
