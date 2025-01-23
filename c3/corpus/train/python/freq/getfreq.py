from collections import Counter
import json

input_file = "../../json/tokenized_lines.json"
output_file = "../../json/frequency.json"

VERBOSE = False

with open(input_file, "r", encoding="utf-8", errors="replace") as infile:
    total_counter = Counter()
    
    line_count = 2721717 #wc -l tokenized_lines.json
    num_digits = len(str(line_count))
    for i, line in enumerate(infile):
        try:
            if i % 1000 == 0:
                print(f"processed {i} out of {line_count}")
            sentence = json.loads(line.strip())
            sentence_counter = Counter(sentence)
            total_counter.update(sentence_counter)

        except json.JSONDecodeError as e:
            if VERBOSE:
                print(f"Skipping invalid line: {i:num_digits}. \n Line content: {line} \n)")
            else:
                print(f"Skipping invalid line: {i:num_digits}")

total_word_count = sum(total_counter.values())
frequency = {word : count/total_word_count for word, count in total_counter.items()}

sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(sorted_frequency, outfile, ensure_ascii=False) 
