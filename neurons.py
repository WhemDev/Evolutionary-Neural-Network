import numpy as np
import random

# Nöron sınıfı
class Neuron:
    def __init__(self, neuron_type, name, input_function=None):
        self.neuron_type = neuron_type  # 'input', 'output', 'internal'
        self.name = name
        self.value = 0.0
        self.connections = []
        self.weigt = 0.0
        self.input_function = input_function  # Özel giriş fonksiyonu

    def connect(self, target_neuron, weight):
        self.connections.append((target_neuron, weight))

    def activate(self):
        # Eğer giriş nöronuysa, özel giriş fonksiyonunu kullanarak değer alır
        if self.neuron_type == 'input' and self.input_function is not None:
            self.value = self.input_function()
        else:
            # İç ve çıkış nöronları gelen bağlantılardan sinyal alır
            total_input = sum(neuron.value * weight for neuron, weight in self.connections)
            self.value = np.tanh(total_input)  # tanh aktivasyon fonksiyonu        
