import numpy as np
import random

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
        total_connections = 1
        
        target_connection_count = random.randint(1, 12)

        # ! Default Connection: Atleast one connection with the target of a output neuron has to be connected
        default_connection_output_neuron = np.random.choice(self.output_neurons)
        default_connection_sender_neuron = np.random.choice(self.input_neurons + self.internal_neurons)
        weight = random.uniform(-4.0, 4.0)
        default_connection_sender_neuron.connect(default_connection_output_neuron, weight)

        default_connection_output_neuron.recievedConnections.append((default_connection_sender_neuron, weight))
        default_connection_output_neuron.totalInputsSum += weight * default_connection_sender_neuron.value

        #for i in range(target_connection_count - 1):
            
            #source_neuron = np.random.choice(self.input_neurons + self.internal_neurons)

            #possible_neurons = []

            #if source_neuron.neuron_type == "input":
            #    target_neuron = np.random.choice(self.output_neurons + self.internal_neurons)
            #elif source_neuron.neuron_type == "internal":
            #    combined_except_source = [x for x in (self.output_neurons + self.internal_neurons) if x != source_neuron]
            #    target_neuron = np.random.choice(combined_except_source)
            #weight = random.uniform(-4.0, 4.0)

            ## connect the neurons : 
            #source_neuron.connect(target_neuron, weight)
            #target_neuron.recievedConnections.append((target_neuron, weight))
            #
            ## add the multiplied value to the source
            #target_neuron.totalInputsSum += weight * target_neuron.value
            #total_connections += 1
        a = 0
        while True:
            source_neuron = np.random.choice(self.input_neurons + self.internal_neurons)

            if source_neuron.neuron_type == "input":
                target_neuron = np.random.choice(self.output_neurons + self.internal_neurons)
            elif source_neuron.neuron_type == "internal":
                combined_except_source = [x for x in (self.output_neurons + self.internal_neurons) if x != source_neuron]
                target_neuron = np.random.choice(combined_except_source)
            weight = random.uniform(-4.0, 4.0)

            targetCon = []
            for con in target_neuron.connections:
                targetCon.append(con[0])

            if (source_neuron not in targetCon) and (source_neuron != target_neuron):
                
                source_neuron.connect(target_neuron, weight)
                target_neuron.recievedConnections.append((source_neuron, weight))

                # add the multiplied value to the source
                # ! check the totalInputsSum 
                target_neuron.totalInputsSum += weight * source_neuron.value
                total_connections += 1
                
            a += 1
            if a == 10: break
            if total_connections == target_connection_count-1: break

        self.total_connections = total_connections

    def set_input_values(self, input_data):
        for neuron in self.input_neurons:
            neuron.value = input_data[neuron.name]  # -1.0 ile 1.0 arasında normalize et

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
        print("All Neuron Connections:")
        for neuron in self.all_neurons:
            # Old method : 
            # neuron.print_debug_info(self.output_neurons)
            print("NEURON NAME : ", neuron.name)
            print("NEURON TYPE : ", neuron.neuron_type)
            print("NEURON VALUE : ", neuron.value)
            print("NEURON SENDED CONNECTIONS : ")
            for connection in neuron.connections:
                print("Connected to :", connection[0].name, "\nwith the weight of : ", connection[1])
            print("NEURON RECIEVED CONNECTIONS : ")
            for connection in neuron.recievedConnections:
                print("Connected to :", connection[0].name, "\nwith the weight of : ", connection[1])
            print("---------------------------------")
