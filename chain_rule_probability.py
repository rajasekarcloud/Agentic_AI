# The chain rule says the probability of a sequence of events (or words) can be decomposed into conditional probabilities
# Unconditional probability: Start with 𝑝(the)
# Conditional probabilities: Multiply by 𝑝(cat∣the),
# then 𝑝(chase∣the,cat), etc.
# Final result: The product gives the probability of the whole sentence.
from collections import defaultdict

# The chain rule says the probability of a sequence of events (or words) can be decomposed into conditional probabilities
#Unconditional probability: Start with 𝑝(the)
#Conditional probabilities: Multiply by 𝑝(cat∣the),
#then 𝑝(chase∣the,cat), etc.
#Final result: The product gives the probability of the whole sentence.
from collections import defaultdict
from collections import defaultdict

corpus = [
    "the cat chase the mouse",
    "the mouse chase the cat",
    "the cat sleeps",
    "the dog chase the cat"
]

# Conditional frequency dictionary
conditional_freq = defaultdict(lambda: defaultdict(int))

for sentence in corpus:
    words = sentence.split()
    for i in range(len(words) - 1):
        prev, next_word = words[i], words[i+1]
        # We will add a key for prev word and count occurrence of it
        conditional_freq[prev][next_word] += 1

# Example queries
print("Conditional frequency of 'cat' given 'the':", conditional_freq["the"]["cat"])
print("Conditional frequency of 'mouse' given 'the':", conditional_freq["the"]["mouse"])
print("Conditional frequency of 'chase' given 'cat':", conditional_freq["cat"]["chase"])

# Output

Conditional frequency of 'cat' given 'the': 4
Conditional frequency of 'mouse' given 'the': 2
Conditional frequency of 'chase' given 'cat': 1
