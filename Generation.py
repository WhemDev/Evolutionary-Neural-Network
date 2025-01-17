from neuralNetwork import NeuralNetwork
from neuron import Neuron
from agent import Agent
import numpy as np
import random
import copy
grid_size = 64
mut = 0
# Mutasyon işlemi
def mutate_network(agent):
    network = agent.network
    global mut
    # %1 ihtimalle mutasyon işlemi gerçekleştirin
    if random.random() < 0.01:

        # Rastgele bir değişiklik türü seçin
        mutation_type = random.choice(["add_connection", "remove_connection", "change_weight", "change_target"])
        mut += 1
        if mutation_type == "add_connection" and len(network.connections) < 12:
            # Yeni bir bağlantı oluştur
            default_connection_output_neuron = np.random.choice(network.output_neurons)
            default_connection_sender_neuron = np.random.choice(network.input_neurons + network.internal_neurons)
            weight = round(random.uniform(-4.0, 4.0), 4)
            default_connection_sender_neuron.connect(default_connection_output_neuron, weight)

            default_connection_output_neuron.recievedConnections.append((default_connection_sender_neuron, weight))
            default_connection_output_neuron.totalInputsSum += weight * default_connection_sender_neuron.value
            network.connections.append([default_connection_sender_neuron, default_connection_output_neuron, weight])

        elif mutation_type == "remove_connection" and len(network.connections) > 1:
            # Mevcut bir bağlantıyı kaldır
            source_neuron = random.choice(network.all_neurons)
            if source_neuron.connections:
                source_neuron.connections.pop()

        elif mutation_type == "change_weight":
            # Birkaç bağlantının ağırlığını değiştir
            for connection in random.sample(network.connections, k=min(3, len(network.connections))):
                weight = connection[2]
                new_weight = random.uniform(-4, 4)
                connection[2] = new_weight

        elif mutation_type == "change_target":
            # Bir bağlantının hedef nöronunu değiştir
            source_neuron = random.choice(network.all_neurons)
            if source_neuron.connections:
                index = random.randint(0, len(source_neuron.connections) - 1)
                new_target = random.choice(network.all_neurons)
                source_neuron.connections[index] = (new_target, source_neuron.connections[index][1])

# Yeni jenerasyon oluşturma
def create_new_generation(agents, grid):
    global mut
    # Hayatta kalan ajanları seçin
    survivors = [agent for agent in agents if agent.survived]

    # Eğer hayatta kalanlar varsa, bunlardan yeni ajanlar üretin
    if survivors:

        new_agents = []
        for _ in range(len(survivors)):
            parent = random.choice(survivors)
            new_agent = Agent(random.randint(5, 59), random.randint(0, grid_size - 1), grid=grid)
            new_agent.network = copy.deepcopy(parent.network)

            new_agents.append(new_agent)
        for _ in range(len(agents) - len(survivors)):
            parent = random.choice(survivors)
            new_agent = Agent(random.randint(5, 59), random.randint(0, grid_size - 1), grid=grid)
            new_agent.network = copy.deepcopy(parent.network)

            mutate_network(new_agent)  # Yeni ajanı mutasyona uğrat
            new_agents.append(new_agent)
        file_path = f'log/mutationCount.txt'
        with open(file_path, 'a') as file:
            file.write(f"{mut}\n")

        return new_agents
    else:
        # Eğer hiç hayatta kalan yoksa, rastgele yeni ajanlar oluştur
        print("none survivors")
        return [Agent(random.randint(5, 59), random.randint(0, grid_size - 1), grid=grid) for _ in range(len(agents))]