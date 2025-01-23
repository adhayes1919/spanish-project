from collections import Counter
import json

input_file = "../json/tokenized_lines.json"
output_file = "../json/encoded_sentences.json"

VERBOSE = False

with open(input_file, "r", encoding="utf-8", errors="replace") as infile:
    total_counter = Counter()
    
    line_count = 2682125 #wc -l tokenized_lines.json
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

min_freq = 5
# word to id
vocab = {word: idx + 2 for idx, (word, count) in enumerate(total_counter.items()) if count >= min_freq}

vocab["<PAD>"] = 0
vocab["<UNK>"] = 1

with open("../json/vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f, ensure_ascii=False)
                
with open(input_file, "r", errors="replace") as infile, open(output_file, "w") as outfile:
    for i, line in enumerate(infile):
        try:
            if i % 1000 == 0:
                print(f"encoded {i} out of {line_count}")
            sentence = json.loads(line.strip())
            encoded_sentence = [vocab.get(word, vocab["<UNK>"]) for word in sentence]
            outfile.write(json.dumps(encoded_sentence) + "\n")
        except json.JSONDecodeError as e:
            if VERBOSE:
                print(f"Skipping invalid line: {i:num_digits}. \n Line content: {line} \n)")
            else:
                print(f"Skipping invalid line: {i:num_digits}")
