import spacy
import re
import json
from nltk.corpus import words
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import psutil

nlp = spacy.load('es_core_news_sm')  # Load Spanish NLP model

# Load Spanish word list
def log_memory_usage():
    process = psutil.Process()
    print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")


with open("/home/ayden/nltk_data/corpora/words/es.txt", "r", encoding="utf-8") as file:
    spanish_words = set(word.strip().lower() for word in file.readlines())

def clean_and_tokenize_text(text, blacklisted_words=None):
    """
    Clean text, tokenize it, and filter out unwanted tokens in a single step.
    """
    # Clean the text using regex
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'r/\S+', '', text)
    text = re.sub(r'[^A-Za-záéíóúüñÁÉÍÓÚÜÑ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove blacklisted words
    if blacklisted_words:
        for word in blacklisted_words:
            text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)

    # Tokenize and filter in one step
    tokens = [
        token.text.lower()
        for token in nlp(text)
        if token.is_alpha and not token.is_stop and token.text.lower() in spanish_words
    ]

    return tokens
#of course going to be a rough metric given that reddit sentences aren't inherently formed properly
def count_sentences(text):
    return len(list(nlp(text).sents))

def preprocess_chunk(data_slice, total, start):
    """
    Process a chunk of data and return cleaned data.
    """
    log_memory_usage()
    chunk_data = []
    sentence_count = 0
    word_frequencies = Counter()

    for i, item in enumerate(data_slice, start=start):
        print(f"Processing {i + 1}/{total}")

        # Process post
        full_text = item['title'] + ' ' + item['selftext']
        sentence_count += count_sentences(full_text)
        filtered_post = clean_and_tokenize_text(full_text)
        word_frequencies.update(filtered_post)

        post_sentence = ' '.join(filtered_post)

        # Process comments
        filtered_comments = []
        for comment in item['comments']:
            sentence_count += count_sentences(comment)
            comment_tokens = clean_and_tokenize_text(comment)
            word_frequencies.update(comment_tokens)

            filtered_comments.append((' '.join(comment_tokens)))

        # Append cleaned post and comments
        chunk_data.append({
            'post': post_sentence,
            'comments': filtered_comments
        })

    return chunk_data, sentence_count, word_frequencies

def process_with_threads(data, chunk_size=100, max_threads=16):
    """
    Use threading to preprocess data in chunks.
    """
    total = len(data)
    results = []
    total_sentences = 0                                     
    total_word_frequencies = Counter()

    with ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for start in range(0, total, chunk_size):
            end = min(start + chunk_size, total)
            data_slice = data[start:end]
            futures.append(executor.submit(preprocess_chunk, data_slice, total, start))
        
        for future in as_completed(futures):
            try:
                chunk_data, sentence_count, word_frequencies = future.result()
                results.extend(chunk_data)
                total_sentences += sentence_count
                total_word_frequencies.update(word_frequencies)
                                     
            except Exception as e:
                print(f"Error in thread: {e}")
    return results, total_sentences, total_word_frequencies

if __name__ == "__main__":
    with open('./testjson/fullscrape2.json', 'r') as input_file:
        initial_data = json.load(input_file)

    print("Starting preprocessing with threading...")
    chunk_size = 100  # Set chunk size
    max_threads = 128  # Adjust the number of threads to fit your system's capabilities

    cleaned_data, total_sentences, total_word_frequencies = process_with_threads(initial_data, chunk_size=chunk_size, max_threads=max_threads)

    print("Saving results to file...")
    with open('./preprocessed/fullscrape2.json', 'w') as output_file:
        json.dump(cleaned_data, output_file, ensure_ascii=False, indent=4)

    with open('./wordfreq/fullscrape2', 'w') as output_file:
        json.dump(total_word_frequencies, output_file, ensure_ascii=False, indent=4)

    print(f"Found {total_sentences} sentences")
    print("Processing complete!")

