import json
import matplotlib.pyplot as plt
import numpy as np

# Parameters
input_file = "../../json/frequency.json"
N = 10000  # Limit to the top N words

# Load frequency data from your JSON file
with open(input_file, "r", encoding="utf-8") as infile:
    frequency_data = json.load(infile)

# Sort by frequency (descending order) and limit to top N words
sorted_frequencies = sorted(frequency_data.values(), reverse=True)[:N]

# Normalize frequencies (ensure they sum to 1 for proper percentage calculation)
total_word_count = sum(sorted_frequencies)
normalized_frequencies = [freq / total_word_count for freq in sorted_frequencies]

# Calculate cumulative coverage
cumulative_coverage = np.cumsum(normalized_frequencies) * 100  # Convert to percentage

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_coverage) + 1), cumulative_coverage)
plt.title(f"Number of Words vs. Total Percent of Language Covered (Top {N} Words)")
plt.xlabel("Number of Words")
plt.ylabel("Cumulative Percentage of Language Covered")
plt.grid()
plt.show()

