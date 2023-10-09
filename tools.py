def generate_round_robin_sequences(n, m):
    sequences = []
    elements = list(range(0, n))
    num_elements = len(elements)

    for i in range(num_elements):
        sequence = []

        for j in range(m):
            idx = (i + j) % num_elements
            sequence.append(elements[idx])

        sequences.append(sequence)

    return sequences