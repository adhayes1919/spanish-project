#!/bin/bash

input_file="./cleaned/cleaned.txt"
output_file="tokenized.json"
spanish_dict="es.txt"

# Ensure UTF-8 locale
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

gawk -v dict="$spanish_dict" '
# Function to fix corrupted UTF-8 sequences
function clean_utf8(str) {
    gsub(/Ã¡/, "á", str);
    gsub(/Ã©/, "é", str);
    gsub(/Ã­/, "í", str);
    gsub(/Ã³/, "ó", str);
    gsub(/Ãº/, "ú", str);
    gsub(/Ã±/, "ñ", str);
    gsub(/Ã¼/, "ü", str);
    return str;
}

# Function to handle lowercase conversion and cleaning
function to_lowercase(str) {
    gsub(/[ÁÉÍÓÚÜÑ]/, "áéíóúüñ", str);  # Replace uppercase accents
    return clean_utf8(tolower(str));    # Convert to lowercase and clean corrupted UTF-8
}

BEGIN { 
    RS="[\n]"; ORS=""; print "[";      # Set record and output separators
    sentence_count = 0; 
    retained_count = 0; 
    print "Loading Spanish dictionary..." > "/dev/stderr";

    # Load Spanish dictionary into an array
    while ((getline word < dict) > 0) {
        spanish_words[word] = 1;
    }
    print "Dictionary loaded. Starting tokenization process..." > "/dev/stderr";
}

{
    sentence_count++;
    gsub(/[^A-Za-záéíóúüñÁÉÍÓÚÜÑ ]/, "", $0);  # Remove non-alphabetic characters
    gsub(/ +/, " ", $0);                        # Normalize spaces
    num_words = split($0, words, " ");          # Split sentence into words

    # Count how many words are in the Spanish dictionary
    spanish_count = 0;
    for (i = 1; i <= num_words; i++) {
        word = to_lowercase(words[i]);
        if (word in spanish_words) {
            spanish_count++;
        }
    }

    # Calculate the percentage of Spanish words
    if (num_words > 0) {
        spanish_percentage = (spanish_count / num_words) * 100;
    } else {
        spanish_percentage = 0;
    }

    # Retain sentence if it meets the threshold (e.g., 70%)
    if (spanish_percentage >= 70) {
        retained_count++;
        printf "["
        for (i = 1; i <= num_words; i++) {
            if (words[i] != "") {
                printf "\"" to_lowercase(words[i]) "\""  # Convert word to lowercase
                if (i < num_words) printf ","          # Add a comma if not the last word
            }
        }
        printf "],"
    }

    # Log progress to stderr every 100 sentences
    if (sentence_count % 100 == 0) {
        print "Processed " sentence_count " sentences so far." > "/dev/stderr";
    }
}

END { 
    if (NR > 1) printf "\b";  # Remove trailing comma
    print "]";
    print "Processing complete. Total sentences: " sentence_count > "/dev/stderr";
    print "Retained sentences: " retained_count > "/dev/stderr";
}
' "$input_file" > "$output_file"

echo "Tokenized sentences exported to $output_file"

