from NeuralNetwork import NeuralNetwork
from Neuron import Neuron
from Agent import Agent
import random
import copy
grid_size = 64
# Mutasyon işlemi
def mutate_network(agent):
    network = agent.network

    # %1 ihtimalle mutasyon işlemi gerçekleştirin
    if random.random() < 0.01:
        # Rastgele bir değişiklik türü seçin
        mutation_type = random.choice(["add_connection", "remove_connection", "change_weight", "change_target"])

        if mutation_type == "add_connection" and len(network.all_connections) < 24:
            # Yeni bir bağlantı oluştur
            source_neuron = random.choice(network.all_neurons)
            target_neuron = random.choice(network.all_neurons)
            weight = random.uniform(-4.0, 4.0)
            source_neuron.connect(target_neuron, weight)

        elif mutation_type == "remove_connection" and len(network.all_connections) > 1:
            # Mevcut bir bağlantıyı kaldır
            source_neuron = random.choice(network.all_neurons)
            if source_neuron.connections:
                source_neuron.connections.pop()

        elif mutation_type == "change_weight":
            # Birkaç bağlantının ağırlığını değiştir
            for connection in random.sample(network.all_connections, k=min(3, len(network.all_connections))):
                weight = connection[1]  # Mevcut ağırlık
                mutation_amount = random.uniform(-0.5, 0.5)  # Küçük değişiklik
                new_weight = max(-4.0, min(4.0, weight + mutation_amount))
                connection[1] = new_weight

        elif mutation_type == "change_target":
            # Bir bağlantının hedef nöronunu değiştir
            source_neuron = random.choice(network.all_neurons)
            if source_neuron.connections:
                index = random.randint(0, len(source_neuron.connections) - 1)
                new_target = random.choice(network.all_neurons)
                source_neuron.connections[index] = (new_target, source_neuron.connections[index][1])

# Yeni jenerasyon oluşturma
def create_new_generation(agents, grid):
    # Hayatta kalan ajanları seçin
    survivors = [agent for agent in agents if agent.survived]

    # Eğer hayatta kalanlar varsa, bunlardan yeni ajanlar üretin
    if survivors:
        new_agents = []
        for _ in range(len(agents)):
            parent = random.choice(survivors)
            new_agent = copy.deepcopy(parent)  # Klonlayarak yeni bir ajan oluştur
            mutate_network(new_agent)  # Yeni ajanı mutasyona uğrat
            new_agents.append(new_agent)
        return new_agents
    else:
        # Eğer hiç hayatta kalan yoksa, rastgele yeni ajanlar oluştur
        return [Agent(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1), grid=grid) for _ in range(len(agents))]