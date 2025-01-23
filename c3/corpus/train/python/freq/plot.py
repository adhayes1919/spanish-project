import json
import matplotlib.pyplot as plt
import numpy as np
from wordfreq import word_frequency, top_n_list

#TODO: clean up, make mine, understand, and potentially account for typos

# Parameters
input_file = "../../json/frequency.json"
N = 10000  # Limit to the top N words
language = 'es'  # Language for wordfreq
step = 500  # Interval for table rows

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

# ==== Create Table Data ====
table_data = []
for i in range(0, N, step):
    custom_percentage = custom_cumulative_coverage[i] if i < len(custom_cumulative_coverage) else 100
    wordfreq_percentage = wordfreq_cumulative_coverage[i] if i < len(wordfreq_cumulative_coverage) else 100
    difference = wordfreq_percentage - custom_percentage
    table_data.append([i + 1, f"{custom_percentage:.2f}", f"{wordfreq_percentage:.2f}", f"{difference:.2f}"])

# ==== Plotting Both Data Sets with Table ====
fig, ax = plt.subplots(figsize=(12, 10))

# Plot custom frequency data
ax.plot(range(1, len(custom_cumulative_coverage) + 1), custom_cumulative_coverage, label="Custom Data")

# Plot wordfreq data
ax.plot(range(1, len(wordfreq_cumulative_coverage) + 1), wordfreq_cumulative_coverage, label="Wordfreq Data", linestyle='--')

# Add title, labels, legend, and grid
ax.set_title(f"Number of Words vs. Total Percent of Language Covered (Top {N} Words)", fontsize=14)
ax.set_xlabel("Number of Words")
ax.set_ylabel("Cumulative Percentage of Language Covered")
ax.legend(loc="upper left")
ax.grid()

# Add a table below the plot
table = plt.table(
    cellText=table_data,
    colLabels=["Words", "Custom Data (%)", "Wordfreq Data (%)", "Difference (%)"],
    cellLoc="center",
    loc="bottom",
    bbox=[0.0, -0.7, 1, 0.6],  # Adjust placement (x, y, width, height)
)

# Style the table for readability
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(table_data[0]))))

# Highlight difference column with red/green coloring
for row_idx, row_data in enumerate(table_data, start=1):  # start=1 to skip header row
    difference = float(row_data[3])
    color = "red" if difference > 0 else "green"
    table[(row_idx, 3)].set_facecolor(color)  # Highlight Difference column (col=3)

# Adjust row heights for better spacing
for key, cell in table.get_celld().items():
    cell.set_height(0.05)  # Increase row height for better readability

# Adjust layout to fit everything
plt.subplots_adjust(left=0.1, bottom=0.4)

# Show the plot
plt.show()

# If needed, save the figure
# fig.savefig("language_coverage_with_table_highlighted.png", dpi=300)

