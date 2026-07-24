memory = {}


def remember(pair, value):
    previous = memory.get(pair, value)

    change = value - previous

    memory[pair] = value

    return previous, change