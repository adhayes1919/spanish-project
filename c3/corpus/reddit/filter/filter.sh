#!/bin/bash

input_file="../json/scrapejson/fullscrape2.json"
output_file="processed.json"
spanish_dict="es.txt"

# Clean text
sed -E 's/http[^ ]+//g; s/r\/[^ ]+//g; s/[^.!?A-Za-záéíóúüñÁÉÍÓÚÜÑ ]//g; s/ +/ /g' "$input_file" > cleaned.txt
#ISSUE: leaves "id: / title/ comments/ selftext" labels

# Count sentences
# 6507295
sentence_count=$(grep -o '[.!?]' cleaned.txt | wc -l)
echo "Total sentences: $sentence_count"

# Count words
word_count=$(wc -w cleaned.txt)
echo "Total words: $word_count"

# Frequency distribution
tr '[:upper:]' '[:lower:]' < cleaned.txt | tr -s ' ' '\n' | sort | uniq -c | sort -nr > word_frequencies.txt

# Filter Spanish words
grep -wFf "$spanish_dict" word_frequencies.txt > spanish_frequencies.txt

