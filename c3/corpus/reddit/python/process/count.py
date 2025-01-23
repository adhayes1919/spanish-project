from collections import Counter
import spacy
import json
from preprocessing import is_spanish_word

nlp = spacy.load('es_core_news_sm')




def analyze_word_frequencies(data):
    """
    Analyze word frequencies from a dataset of posts and comments.
    Args:
        data: List of dictionaries with 'post' and 'comments' keys.
    Returns:
        Counter object with word frequencies.
    """
    word_counts = Counter()
    total_groups = len(data)  # Total number of groups
    total_items = sum(len(group) for group in data)  # Limit total items to 100
    processed_items = 0

    #limit = 100

    for group_idx, group in enumerate(data):  # Iterate through the outer list
        print(f"Processing group {group_idx + 1}/{total_groups}")

        for item_idx, item in enumerate(group):  # Each item is a dictionary with 'post' and 'comments'
            """
            if processed_items >= limit:  # Stop after processing 100 items
                break
            """

            processed_items += 1
            print(f"  Processing item {processed_items}/{total_items} ({processed_items/total_items:.2%})")

            # Process the 'post' text
            tokens_post = [token.text.lower() for token in nlp(item['post']) 
                           if token.is_alpha and is_spanish_word(token.text.lower())]  # Tokenize and filter valid words
            word_counts.update(tokens_post)  # Update word frequencies

            # Process the 'comments' text
            for comment in item['comments']:
                tokens_comment = [token.text.lower() for token in nlp(comment) 
                                  if token.is_alpha and is_spanish_word(token.text.lower())]  # Tokenize and filter valid words
                word_counts.update(tokens_comment)  # Update word frequencies
        """  
        if processed_items >= limit:  # Ensure outer loop exits if 100 items are processed
            break
        """

    print("Processing complete!")
    return word_counts


def count_sentences(text):
    return len(list(nlp(text).sents))

def analyze_sentence_counts(data):
    sentence_counts = {"post_sentences": 0, "comment_sentences": 0}  
    n = len(data)
    print(f"preparing to count to : {n}")
    for i, item in enumerate(data):
        print(f"data: {i}")
        sentence_counts["post_sentences"] += count_sentences(item["post"])
        for comment in item["comments"]:
            sentence_counts["comment_sentences"] += count_sentences(comment)
    return sentence_counts

#frequencies = analyze_word_frequencies(preprocessed_data)
#print(frequencies[:20])  # Top 20 most common words

if __name__ == "__main__":
    with open('./preprocessed/fullscrape.json', 'r') as data_file:
        data_json = json.load(data_file)
        freq = analyze_word_frequencies(data_json)

        with open('word_counts.json', 'w', encoding='utf-8') as file:
            json.dump(freq, file, ensure_ascii=False, indent=4)
        print(freq)

        #sentence counts include english too for right now
        #sentence_counts = analyze_sentence_counts(data_json)
        #print(sentence_counts)
