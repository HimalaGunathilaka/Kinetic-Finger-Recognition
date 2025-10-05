from collections import defaultdict
import struct
import random

def make_markov():
    return defaultdict(lambda: defaultdict(int))

def add_sequence(sequence, markov_data, pad=True):
    if pad:
        sequence = "^^" + sequence
    for i in range(len(sequence) - 2):
        context = sequence[i:i+2]
        next_char = sequence[i+2]
        markov_data[context][next_char] += 1
    return markov_data

def normalize_markov(markov_data):
    normalized = {}
    for context, next_chars in markov_data.items():
        total = sum(next_chars.values())
        normalized[context] = {c: count / total for c, count in next_chars.items()}
    return normalized

def train_markov_model(text, existing_model=None):
    if existing_model is None:
        existing_model = make_markov()
    return add_sequence(text, existing_model)

def save_binary_model(prob_model, filepath="markov.bin"):
    """
    Save normalized model as a binary file:
    - 2 bytes: context
    - 1 byte: next char
    - 4 bytes: probability (float)
    """
    with open(filepath, "wb") as f:
        for context, next_chars in prob_model.items():
            for c, prob in next_chars.items():
                # pack 2 chars + 1 char + float = 2+1+4 = 7 bytes
                data = struct.pack('3sf', context.encode('utf-8') + c.encode('utf-8'), prob)
                f.write(data)

def sample_next(prob_model, context):
    if context not in prob_model:
        return None
    next_chars = prob_model[context]
    chars, probs = zip(*next_chars.items())
    return random.choices(chars, weights=probs, k=1)[0]

def generate_text(prob_model, length=100):
    context = "^^"
    output = []
    for _ in range(length):
        next_char = sample_next(prob_model, context)
        if next_char is None:
            break
        output.append(next_char)
        context = context[1] + next_char
    return "".join(output)

# Example usage
if __name__ == "__main__":
    text1 = (
        "Markov chains are mathematical systems that hop from one state to another. "
        "They are named after Andrey Markov, a Russian mathematician who studied these stochastic processes. "
        "In a Markov chain, the probability of moving to the next state depends only on the current state, "
        "not on the sequence of events that preceded it. This property is known as the Markov property. "
        "Markov models are widely used in various fields such as physics, chemistry, economics, and computer science. "
        "They are particularly useful for modeling random processes that evolve over time, such as stock prices or weather patterns."
    )

    text2 = (
        "Natural language processing often utilizes Markov models to predict the likelihood of a sequence of words. "
        "For example, a third-order Markov model considers the previous three words to predict the next word in a sentence. "
        "This approach helps in applications like text generation, speech recognition, and spelling correction. "
        "By analyzing large corpora of text, Markov models can learn the statistical properties of language. "
        "These models are foundational in building more complex language models and are a stepping stone to modern neural networks."
    )

    model = train_markov_model(text1)
    model = train_markov_model(text2, model)

    prob_model = normalize_markov(model)
    save_binary_model(prob_model)

    print("Generated text:", generate_text(prob_model, length=50))
