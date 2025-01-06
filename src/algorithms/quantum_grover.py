##
## QuanticComputing [WSL: Ubuntu-24.04]
## File description:
## quantum_grover
##

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from math import pi, sqrt, ceil
import time

def create_oracle(n_qubits: int, index_target: int) -> QuantumCircuit:
    # Creates an oracle that marks the quantum state corresponding to the target index.
    oracle = QuantumCircuit(n_qubits)

    binary = format(index_target, f'0{n_qubits}b')
    print(f"🎯 Target index ({index_target}) in binary: {binary}")

    # Apply X gates to qubits where target binary digit is 0
    for i, bit in enumerate(binary):
        if bit == '0':
            oracle.x(n_qubits - 1 - i)
    # H -> MCX -> H implements the phase flip
    oracle.h(n_qubits - 1)
    oracle.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    oracle.h(n_qubits - 1)

    # Undo the X gates to restore original state
    for i, bit in enumerate(binary):
        if bit == '0':
            oracle.x(n_qubits - 1 - i)

    return oracle

def diffuser(n_qubits: int) -> QuantumCircuit:
    # Creates a diffuser circuit that amplifies the amplitude of the target state.
    qc = QuantumCircuit(n_qubits)
    for qubit in range(n_qubits):
        qc.h(qubit)
        qc.x(qubit)

    # Apply phase flip to the target state
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)

    # Undo the X and H gates
    for qubit in range(n_qubits):
        qc.x(qubit)
        qc.h(qubit)
    return qc


def classical_search(numbers: list[int], target: int) -> tuple[int, float]:
    start_time = time.time()
    for i, num in enumerate(numbers):
        if num == target:
            return i, time.time() - start_time
    return -1, time.time() - start_time


def grover_search(numbers: list[int], target: int) -> tuple[int, float, QuantumCircuit, float]:
    if target not in numbers:
        raise ValueError(f"❌ Number {target} not found in the list!")

    start_time = time.time()
    target_index = numbers.index(target)
    n_qubits = len(bin(len(numbers) - 1)[2:])

    # Create quantum and classical registers
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr)

    # Apply Hadamard gates to all qubits for superposition
    for qubit in range(n_qubits):
        qc.h(qubit)

    n_iterations = int(ceil(pi / 4 * sqrt(len(numbers))))

    print(f"\n🔍 Searching for index of {target} in list")
    print(f"📍 Target index: {target_index}")
    print(f"🔢 Number of qubits: {n_qubits}")
    print(f"🔄 Number of iterations: {n_iterations}")

    # Apply Grover's algorithm
    # - The oracle (`create_oracle`) identifies the target state by inverting its phase
    # - The diffuser (`diffuser`) amplifies the amplitude of the marked state
    # - After ~√N iterations, the probability of measuring the target state is maximal
    for i in range(n_iterations):
        print(f"⚡ Iteration {i + 1}/{n_iterations}")
        qc.compose(create_oracle(n_qubits, target_index), inplace=True)
        qc.compose(diffuser(n_qubits), inplace=True)

    qc.measure(qr, cr)

    # Execute the circuit
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1000).result()
    counts = result.get_counts(qc)

    # Find the most frequent state
    most_frequent = max(counts.items(), key=lambda x: x[1])
    found_index = int(most_frequent[0], 2)
    probability = most_frequent[1] / 1000


    print(f"\n📊 Quantum State Distribution:")
    print("=" * 80)
    print(f"{'State':^20} | {'Index':^8} | {'Number':^8} | {'Frequency':^12} | {'Probability':^10}")
    print("=" * 80)

    # Sort by count for better visualization
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    for state, count in sorted_counts:
        index = int(state, 2)
        if index < len(numbers):
            prob_percent = count / 10
            if count == most_frequent[1]:
                print(f"🎯 |{state}⟩ {index:^8} | {numbers[index]:^8} | {count:^12} | {prob_percent:^9.1f}% ⭐")
            else:
                print(f"  |{state}⟩ {index:^8} | {numbers[index]:^8} | {count:^12} | {prob_percent:^9.1f}%")

    print("=" * 80)
    print(f"Total measurements: 1000 | Success rate: {most_frequent[1]/10:.1f}%")
    print("=" * 80)

    return found_index, probability, qc, time.time() - start_time

def main() -> None:
    numbers = list(range(0, 100000, 2))
    target = 60504

    try:
        found_index, prob, circuit, quantum_time = grover_search(numbers, target)
        print(f"\n🌟 Quantum result:")
        print(f"  Found index: {found_index} (number {numbers[found_index]})")
        print(f"  Probability: {prob * 100:.1f}%")
        print(f"  ⏱️  Quantum time: {quantum_time:.6f}s")

        index, classical_time = classical_search(numbers, target)
        print(f"\n🔍 Classical result:")
        print(f"  Found index: {index}")
        print(f"  ⏱️  Classical time: {classical_time:.6f}s")

    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

if __name__ == "__main__":
    main()