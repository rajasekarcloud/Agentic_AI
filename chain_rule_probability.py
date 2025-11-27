# The chain rule says the probability of a sequence of events (or words) can be decomposed into conditional probabilities
# Unconditional probability: Start with 𝑝(the)
# Conditional probabilities: Multiply by 𝑝(cat∣the),
# then 𝑝(chase∣the,cat), etc.
# Final result: The product gives the probability of the whole sentence.
from collections import defaultdict
