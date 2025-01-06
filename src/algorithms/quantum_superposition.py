##
## QuanticComputing [WSL: Ubuntu-24.04]
## File description:
## quantum_superposition
##

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def create_quantum_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate for superposition
    qc.measure(0, 0)  # Measure the qubit
    return qc


def execute_circuit(qc: QuantumCircuit, shots: int = 1000) -> dict:
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=shots)
    result = job.result()
    return result.get_counts(qc)


def save_histogram(counts: dict, filename: str = 'quantum_results.png'):
    plt.style.use('dark_background')
    figure = plot_histogram(counts, color='#00FF00')
    plt.savefig(filename, facecolor='black', edgecolor='black')
    print(f"Histogram saved as '{filename}'")


def main():
    # Create and execute quantum circuit
    qc = create_quantum_circuit()
    counts = execute_circuit(qc)

    # Display and save results
    print("Measurement results:", counts)
    save_histogram(counts)


if __name__ == "__main__":
    main()

