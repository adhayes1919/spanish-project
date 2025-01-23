# Ayden Hayes
# 12/12/24
# preprocessing.py
# To provide basic regex preprocessing for Spanish learning app
import spacy
import re
import json
from nltk.corpus import words

nlp = spacy.load('es_core_news_sm')  # Load Spanish NLP model
spanish_vocab = nlp.vocab

def clean_text(text, blacklisted_words=None):
    """Clean text by removing URLs, special characters, and optional blacklisted words."""
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'r/\S+', '', text)
    text = re.sub(r'[^A-Za-záéíóúüñÁÉÍÓÚÜÑ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if blacklisted_words:
        for word in blacklisted_words:
            text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)

    tokens = text.split()
    tokens = [token.lower() for token in tokens if is_spanish_word(token)]

    return ' '.join(tokens)

#spanish_words = set(word.lower() for word in words.words('es.txt'))
with open("/home/ayden/nltk_data/corpora/words/es.txt", "r", encoding="utf-8") as file:
    spanish_words = set(word.strip().lower() for word in file.readlines())

def is_spanish_word(word):
    """Check if a word exists in the Spanish vocabulary."""
    return word in spanish_words

def preprocess_chunk(data_slice, total, start):
    """Process a chunk of data and return cleaned data."""
    chunk_data = []
    for i, item in enumerate(data_slice, start=start):
        print(f"Processing {i + 1}/{total}")
        # Process post
        post_text = clean_text(item['title'] + ' ' + item['selftext'])
        filtered_post = [
            token.text.lower() for token in nlp(post_text)
            if token.is_alpha and not token.is_stop and is_spanish_word(token.text.lower())
        ]
        post_sentence = ' '.join(filtered_post)

        # Process comments
        filtered_comments = []
        for comment in item['comments']:
            comment_text = clean_text(comment)
            filtered_comment = [
                token.text.lower() for token in nlp(comment_text)
                if token.is_alpha and not token.is_stop and is_spanish_word(token.text.lower())
            ]
            comment_sentence = ' '.join(filtered_comment)
            filtered_comments.append(comment_sentence)

        # Append cleaned post and comments
        chunk_data.append({
            'post': post_sentence,
            'comments': filtered_comments
        })
    return chunk_data

if __name__ == "__main__":
    with open('./testjson/fullscrape.json', 'r') as input_file:
        initial_data = json.load(input_file)

    total = len(initial_data)  # Calculate total items
    chunk_size = 100  # Set chunk size

    with open('./preprocessed/fullscrape2.json', 'w') as output_file:
        output_file.write("[")  # Start JSON array
        for start in range(0, total, chunk_size):
            end = min(start + chunk_size, total)
            data_slice = initial_data[start:end]
            chunk = preprocess_chunk(data_slice, total, start)
            json.dump(chunk, output_file, ensure_ascii=False, indent=4)
            if end < total:
                output_file.write(",")  # Add a comma between chunks
        output_file.write("]")  # End JSON array

