import cirq_google

# Print the Sycamore processor layout
print(cirq_google.Sycamore)

# Optional: access details about the qubits
qubits = cirq_google.Sycamore.qubits
print(f"Number of qubits: {len(qubits)}")
print("First 5 qubits:", qubits[:5])
