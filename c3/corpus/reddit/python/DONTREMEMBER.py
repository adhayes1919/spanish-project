#Ayden Hayes
#12/12/24
#preprocessing.py
#to provide basic regex preprocessing for spanish learning app
import spacy
import re
import json
from concurrent.futures import ThreadPoolExecutor
from threading import local

# Thread-local storage for spacy model
thread_local = local()

def get_nlp():
    """
    Ensure each thread has its own nlp instance.
    """
    if not hasattr(thread_local, "nlp"):
        thread_local.nlp = spacy.load('es_core_news_sm')
    return thread_local.nlp


def clean_text(text, blacklisted_words=None):
    """
    Cleans the input text using regex.
    """
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'r/\S+', '', text)
    text = re.sub(r'[^A-Za-záéíóúüñÁÉÍÓÚÜÑ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if blacklisted_words:
        for word in blacklisted_words:
            text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)

    return text


def is_spanish_word(word, nlp):
    """
    Checks if a word exists in the Spanish vocabulary.
    """
    return word in nlp.vocab


def process_item(item):
    """
    Processes a single JSON item (post and comments).
    """
    nlp = get_nlp()
    post_text = clean_text(item['title'] + ' ' + item['selftext'])
    filtered_post = [
        token.text.lower() for token in nlp(post_text)
        if token.is_alpha and not token.is_stop and is_spanish_word(token.text.lower(), nlp)
    ]
    post_sentence = ' '.join(filtered_post)

    filtered_comments = []
    for comment in item['comments']:
        comment_text = clean_text(comment)
        filtered_comment = [
            token.text.lower() for token in nlp(comment_text)
            if token.is_alpha and not token.is_stop and is_spanish_word(token.text.lower(), nlp)
        ]
        comment_sentence = ' '.join(filtered_comment)
        filtered_comments.append(comment_sentence)

    return {
        'post': post_sentence,
        'comments': filtered_comments
    }


def preprocess_data(data, max_threads=8):
    """
    Preprocess the data using multithreading.
    """
    cleaned_data = []
    total = len(data)
    print(f"Starting preprocessing with {max_threads} threads...")

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(process_item, item): idx for idx, item in enumerate(data)}

        for future in futures:
            idx = futures[future]
            try:
                cleaned_data.append(future.result())
                print(f"Processed item: {idx + 1}/{total}")
            except Exception as e:
                print(f"Error processing item {idx + 1}/{total}: {e}")

    return cleaned_data


if __name__ == "__main__":
    with open('./testjson/fullscrape.json', 'r') as input_file:
        initial_data = json.load(input_file)

    cleaned_data = preprocess_data(initial_data, max_threads=8)

    with open('./preprocessed/fullscrape.json', 'w') as output_file:
        json.dump(cleaned_data, output_file, ensure_ascii=False, indent=4)

