##
## QuanticComputing [WSL: Ubuntu-24.04]
## File description:
## quantum_sort
##

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute


def quantum_compare(a: int, b: int) -> bool:
    # Create circuit with 1 qubit and 1 classical bit
    qr = QuantumRegister(1, 'q')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr, cr)

    # Encode numbers (if a > b, apply X on qubit)
    if a > b:
        qc.x(qr[0])

    # Measure qubit into classical bit
    qc.measure(qr[0], cr[0])

    # Execute circuit
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    print("\n🔬 Circuit for comparison between", a, "and", b, ":")
    print("Initial state: |0⟩")
    if a > b:
        print("After X gate: |1⟩ (a > b)")
    else:
        print("No X gate applied: |0⟩ (a ≤ b)")
    print("Measurement result:", list(counts.keys())[0])
    print(qc.draw(output='text'))

    # Return true if a > b (if we measure '1')
    return list(counts.keys())[0] == '1'


def quantum_bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    array_sorted = arr.copy()

    print(f"\n🔄 Starting quantum sort for: {array_sorted}")

    # Bubble sort
    for i in range(n):
        for j in range(0, n - i - 1):
            print(f"⚡ Quantum comparison between {array_sorted[j]} and {array_sorted[j+1]}")
            if quantum_compare(array_sorted[j], array_sorted[j + 1]):
                array_sorted[j], array_sorted[j+1] = array_sorted[j+1], array_sorted[j]
                print(f"🔄 Swap performed: {array_sorted}")

    return array_sorted



def main():
    print("🌟 Welcome to Quantum Bubble Sort! 🌟")
    numbers = [4, 2, 47, 1, 5, 51, 1]
    print("📋 Original list:", numbers)

    sorted_numbers = quantum_bubble_sort(numbers)
    print("\n✨ Sorted list:", sorted_numbers)


if __name__ == "__main__":
    main()

