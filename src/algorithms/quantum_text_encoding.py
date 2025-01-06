##
## QuanticComputing [WSL: Ubuntu-24.04]
## File description:
## quantum_hello_world
##

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute


def text_to_binary(text: str) -> str:
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary: str) -> str:
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        text += chr(int(byte, 2))
    return text


def process_chunk(chunk: str) -> tuple[str, QuantumCircuit]:
    binary_chunk = text_to_binary(chunk)
    n_qbits = len(binary_chunk)

    # Create quantum and classical registers
    qr = QuantumRegister(n_qbits, 'q')
    cr = ClassicalRegister(n_qbits, 'c')
    qc = QuantumCircuit(qr, cr)

    # Encode binary data into quantum state
    for i, bit in enumerate(binary_chunk):
        if bit == '1':
            qc.x(qr[i])

    # Measure qbits
    qc.measure(qr, cr)

    # Execute circuit
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    measured = list(counts.keys())[0]
    return measured[::-1], qc


def print_header():
    print("\n" + "=" * 50)
    print("🔬 Quantum Message Processing")
    print("=" * 50 + "\n")


def process_message_chunks(message: str, chunk_size: int) -> tuple[str, list]:
    result_binary = ""
    circuits = []

    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]
        print(f"📦 Processing chunk {i // chunk_size + 1}: '{chunk}'")

        chunk_binary, circuit = process_chunk(chunk)
        result_binary += chunk_binary
        circuits.append(circuit)

        print(f"   Binary representation: {text_to_binary(chunk)}")
        print(f"   Quantum measurement: {chunk_binary}\n")

    return result_binary, circuits


def display_circuits(circuits: list):
    print("🔋 Quantum Circuits Generated:")
    print("-" * 50)
    for i, circuit in enumerate(circuits):
        print(f"\n🔷 Circuit for chunk {i + 1}:")
        print(circuit.draw())
        print("-" * 50)


def print_results_summary(message: str, decoded_message: str, chunk_size: int):
    print("\n📊 Results Summary:")
    print("-" * 50)
    print(f"📝 Original message: '{message}'")
    print(f"🎯 Decoded message: '{decoded_message}'")
    print(f"📦 Total chunks processed: {len(message) // chunk_size + (1 if len(message) % chunk_size else 0)}")
    print("=" * 50 + "\n")


def quantum_text_encoding(message: str, chunk_size: int = 3) -> str:

    print_header()
    result_binary, circuits = process_message_chunks(message, chunk_size)

    display_circuits(circuits)

    decoded_message = binary_to_text(result_binary)
    print_results_summary(message, decoded_message, chunk_size)

    return decoded_message


def main():
    print("\n🌟 Welcome to Quantum Message Processor 🌟\n")
    message = input("✍️  Enter your message: ")
    quantum_text_encoding(message)


if __name__ == "__main__":
    main()

