import numpy as np
import random

class Neuron:
    def __init__(self, neuron_type, name):
        self.neuron_type = neuron_type
        self.name = name
        self.value = 0.0
        self.connections = []
        self.recievedConnections = []
        self.totalInputsSum = 0.0
        self.totalInputsCount = len(self.recievedConnections)

    def connect(self, target_neuron, weight):
        self.connections.append((target_neuron, weight))

    def activate(self):
        if self.neuron_type != 'input':  # Input nöronları aktive olmaz
            total_input = sum(neuron.value * weight for neuron, weight in self.recievedConnections)
            self.value = np.tanh(total_input)  # -1.0 ile 1.0 arasında çıktı
            if (self.neuron_type == 'internal') and (self.recievedConnections == []):
                self.value = 1.0

    # Bağlantıları, ağırlıkları ve kendi değerini yazdırmak için bir fonksiyon
    #
    # def print_debug_info(self, output_neurons):
    #    output_connections = [conn for conn in self.connections if conn[0] in output_neurons]
    #    if output_connections:
    #        print(f"Neuron {self.name}: Value = {self.value}")
    #        for target_neuron, weight in output_connections:
    #            print(f"  -> Connected to {target_neuron.name} with weight {weight}")
