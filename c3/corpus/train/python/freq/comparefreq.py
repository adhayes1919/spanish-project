import json
import matplotlib.pyplot as plt
import numpy as np
from wordfreq import word_frequency, top_n_list

# Parameters
input_file = "../../json/frequency.json"
N = 10000  # Limit to the top N words
language = 'es'  # Language for wordfreq

# ==== Custom Frequency Data ====
# Load frequency data from your JSON file
with open(input_file, "r", encoding="utf-8") as infile:
    frequency_data = json.load(infile)

# Sort by frequency (descending order) and limit to top N words
sorted_frequencies = sorted(frequency_data.values(), reverse=True)[:N]

# Normalize frequencies (ensure they sum to 1 for proper percentage calculation)
total_word_count = sum(sorted_frequencies)
normalized_frequencies = [freq / total_word_count for freq in sorted_frequencies]

# Calculate cumulative coverage for custom data
custom_cumulative_coverage = np.cumsum(normalized_frequencies) * 100  # Convert to percentage

# ==== Wordfreq Data ====
# Get the top N words for Spanish
top_words = top_n_list(language, N, wordlist='best')

# Calculate cumulative frequency for wordfreq data
wordfreq_cumulative_coverage = []
total_coverage = 0

for word in top_words:
    freq = word_frequency(word, language, wordlist='best')
    total_coverage += freq
    wordfreq_cumulative_coverage.append(total_coverage * 100)  # Convert to percentage

# ==== Plotting Both Data Sets ====
plt.figure(figsize=(10, 6))

# Plot custom frequency data
plt.plot(range(1, len(custom_cumulative_coverage) + 1), custom_cumulative_coverage, label="Custom Data")

# Plot wordfreq data
plt.plot(range(1, len(wordfreq_cumulative_coverage) + 1), wordfreq_cumulative_coverage, label="Wordfreq Data", linestyle='--')

# Add title and labels
plt.title(f"Number of Words vs. Total Percent of Language Covered (Top {N} Words)")
plt.xlabel("Number of Words")
plt.ylabel("Cumulative Percentage of Language Covered")
plt.legend()
plt.grid()
plt.show()

