import json
import random

path = "../json/data/"
input_file = "../json/encoded_sentences.json"

train_file = path + "train_data.jsonl"
val_file = path + "val_data.jsonl"
test_file = path + "test_data.jsonl"


train_ratio, val_ratio, test_ratio = 0.8, 0.1, 0.1

print("Starting split")
with open(input_file, "r", errors="replace") as infile, \
    open(train_file, "w") as train_out, \
    open(val_file, "w") as val_out, \
    open(test_file, "w") as test_out:

        for line in infile:
            rand = random.random()
            if rand < train_ratio:
                train_out.write(line)
            elif rand < train_ratio + val_ratio:
                val_out.write(line)
            else:
                test_out.write(line)
print("Randomized split complete")

