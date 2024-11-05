# Evolutionary Neural Network

EvoNet is a neural network simulation that combines evolutionary principles and dynamic neural adaptation. It allows creatures to evolve and adapt to different environmental conditions, refining their neural networks over generations to improve their survival and efficiency.

I built it from scratch, so there are still many bugs and logical issues to resolve. I’m continuously working on refining the code to make it more stable and efficient.

## Features
- **Evolutionary Algorithm**: Creatures optimize their neural connections and input handling to adapt to their surroundings.
- **Dynamic Neural Architecture**: Creatures have the freedom to configure their neural networks, connecting input, internal, and output neurons as needed.
- **Tanh Activation Function**: Internal and output neurons use the tanh activation function to process signals in the range of -1.0 to 1.0.
- **Connection Limits**: Each creature is restricted to a maximum of 24 connections to balance complexity and performance.

## Structure
- **Input Neurons**: Produce signals in the range of -4.0 to 4.0.
- **Internal Neurons**: Can connect to both other internal neurons and output neurons, using the tanh activation function.
- **Output Neurons**: Generate responses to the environment, with outputs transformed by the tanh activation function.

## Installation and Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/WhemDev/NeuralNetwork.git
   ```
2. Install the required dependencies.
3. Run main.py to start the simulation.

Contributions

Take a look at logs and generation images to see results!

We welcome contributions! Feel free to open an issue or submit a pull request if you have ideas or improvements to share.
