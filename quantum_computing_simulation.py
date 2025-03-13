import numpy as np
import itertools

class QuantumGate:
    def __init__(self, matrix):
        self.matrix = matrix

    def apply(self, state):
        return np.dot(self.matrix, state)

class QuantumCircuit:
    def __init__(self, qubits):
        self.qubits = qubits
        self.state = self.initialize_state()

    def initialize_state(self):
        return np.array([1] + [0] * (2**self.qubits - 1))

    def apply_gate(self, gate, target_qubit):
        identity = np.identity(2**self.qubits)
        gate_matrix = gate.matrix
        for i in range(2**self.qubits):
            for j in range(len(gate_matrix)):
                index = (i // (2**target_qubit)) * (2**target_qubit) + (i % (2**target_qubit))
                identity[i][index] = gate_matrix[j // 2][j % 2] if (i % 2 == j) else identity[i][index]
        self.state = np.dot(identity, self.state)

    def measure(self):
        probabilities = np.abs(self.state)**2
        outcomes = np.arange(len(probabilities))
        return np.random.choice(outcomes, p=probabilities)

class HadamardGate(QuantumGate):
    def __init__(self):
        h_matrix = 1/np.sqrt(2) * np.array([[1, 1], [1, -1]])
        super().__init__(h_matrix)

class PauliXGate(QuantumGate):
    def __init__(self):
        x_matrix = np.array([[0, 1], [1, 0]])
        super().__init__(x_matrix)

class PauliYGate(QuantumGate):
    def __init__(self):
        y_matrix = np.array([[0, -1j], [1j, 0]])
        super().__init__(y_matrix)

class PauliZGate(QuantumGate):
    def __init__(self):
        z_matrix = np.array([[1, 0], [0, -1]])
        super().__init__(z_matrix)

class CNOTGate(QuantumGate):
    def __init__(self):
        cnot_matrix = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1],
                                 [0, 0, 1, 0]])
        super().__init__(cnot_matrix)

class QuantumSimulator:
    def __init__(self, qubits):
        self.circuit = QuantumCircuit(qubits)

    def add_gate(self, gate, target_qubit):
        self.circuit.apply_gate(gate, target_qubit)

    def run(self):
        return self.circuit.measure()

def main():
    num_qubits = 2
    simulator = QuantumSimulator(num_qubits)

    # Add gates to the simulator
    hadamard = HadamardGate()
    simulator.add_gate(hadamard, 0)  # Apply H to qubit 0

    cnot = CNOTGate()
    simulator.add_gate(cnot, 1)  # Apply CNOT with control on qubit 0 and target qubit 1

    # Run the simulation
    result = simulator.run()
    print(f'Measurement result: {result}')

if __name__ == "__main__":
    main()

# Simulation of multiple runs
def multiple_runs(simulations):
    results = []
    for i in range(simulations):
        num_qubits = 2
        simulator = QuantumSimulator(num_qubits)
        hadamard = HadamardGate()
        simulator.add_gate(hadamard, 0)
        cnot = CNOTGate()
        simulator.add_gate(cnot, 1)
        result = simulator.run()
        results.append(result)
    return results

def run_and_collect_data(simulations):
    results = multiple_runs(simulations)
    counts = np.bincount(results, minlength=4)
    print("\nSimulation results for {} runs:".format(simulations))
    for i, count in enumerate(counts):
        print(f'Outcome {i}: {count}')

run_and_collect_data(1000)

# Visualization of probabilities
import matplotlib.pyplot as plt

def plot_probability_distribution(simulations):
    results = multiple_runs(simulations)
    counts = np.bincount(results, minlength=4)
    probabilities = counts / simulations
    
    plt.bar(range(len(probabilities)), probabilities)
    plt.xticks(range(len(probabilities)))
    plt.xlabel('Outcome')
    plt.ylabel('Probability')
    plt.title('Outcome Probability Distribution')
    plt.show()

plot_probability_distribution(1000)

# Extended functionality: random quantum circuit generation
def random_circuit(num_qubits, depth):
    gates = [HadamardGate(), PauliXGate(), PauliYGate(), PauliZGate(), CNOTGate()]
    circuit = QuantumCircuit(num_qubits)

    for _ in range(depth):
        gate = np.random.choice(gates)
        target_qubit = np.random.randint(0, num_qubits)
        if isinstance(gate, CNOTGate):
            control_qubit = target_qubit
            target_qubit = (target_qubit + 1) % num_qubits
        else:
            control_qubit = None
        
        circuit.apply_gate(gate, target_qubit)

    return circuit

random_circuit = random_circuit(3, 5)
print("Random circuit state: ", random_circuit.state)

# Extended: quantum state visualization
from qiskit.visualization import plot_histogram

def visualize_circuit(circuit):
    from qiskit import QuantumCircuit
    from qiskit.visualization import plot_bloch_multivector

    qiskit_circuit = QuantumCircuit(circuit.qubits)
    for gate in circuit.gates:
        if isinstance(gate, HadamardGate):
            qiskit_circuit.h(0)
        elif isinstance(gate, PauliXGate):
            qiskit_circuit.x(0)
        elif isinstance(gate, CNOTGate):
            qiskit_circuit.cx(0, 1)

    backend = Aer.get_backend('statevector_simulator')
    statevector = execute(qiskit_circuit, backend).result().get_statevector()
    plot_bloch_multivector(statevector)

visualize_circuit(random_circuit)

# Save and Load Quantum Circuit to/from a file
import json

def save_circuit_to_file(circuit, filename):
    with open(filename, 'w') as f:
        json.dump(circuit.state.tolist(), f)

def load_circuit_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        loaded_circuit = QuantumCircuit(len(data))
        loaded_circuit.state = np.array(data)
        return loaded_circuit

# Example of saving and loading circuit state
save_circuit_to_file(random_circuit, 'quantum_circuit.json')
loaded_circuit = load_circuit_from_file('quantum_circuit.json')
print("Loaded circuit state: ", loaded_circuit.state)

# Performance benchmarking
def benchmark_simulator(runs=1000):
    import time
    start = time.time()
    for _ in range(runs):
        simulator = QuantumSimulator(2)
        simulator.add_gate(HadamardGate(), 0)
        simulator.add_gate(CNOTGate(), 1)
        simulator.run()
    end = time.time()
    print(f'Benchmarking {} runs took {end - start:.5f} seconds')

benchmark_simulator(1000)