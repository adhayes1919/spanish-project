import matplotlib.pyplot as plt
from wordfreq import word_frequency, top_n_list

# Parameters
language = 'es'  # Spanish
n = 10000  # Number of top words to consider

# Get the top N words for Spanish
top_words = top_n_list(language, n, wordlist='best')

# Calculate cumulative frequency
cumulative_coverage = []
total_coverage = 0

for word in top_words:
    freq = word_frequency(word, language, wordlist='best')
    total_coverage += freq
    cumulative_coverage.append(total_coverage * 100)  # Convert to percentage

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_coverage) + 1), cumulative_coverage)
plt.title("Number of Words vs. Total Percent of Language Covered (Spanish)")
plt.xlabel("Number of Words")
plt.ylabel("Cumulative Percentage of Language Covered")
plt.grid()
plt.show()

