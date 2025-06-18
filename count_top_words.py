from collections import Counter
import re

def count_top_words(file_path, exclude_list=None, top_n=20):
    """
    Counts the most frequent words in a text file, excluding specified words.

    Parameters:
        file_path (str): Path to the text file.
        exclude_list (list): List of words to exclude from the count.
        top_n (int): Number of top frequent words to return (default is 20).

    Returns:
        list: List of tuples containing the top N frequent words and their counts.
    """
    
    def load_text(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def clean_and_split(text):
        # Convert to lowercase and extract words using regex
        return re.findall(r'\b\w+\b', text.lower())

    def filter_words(words, exclusions):
        if exclusions:
            exclusions_set = set(word.lower() for word in exclusions)
            return [word for word in words if word not in exclusions_set]
        return words

    text = load_text(file_path)
    words = clean_and_split(text)
    filtered_words = filter_words(words, exclude_list)

    word_counts = Counter(filtered_words)
    return word_counts.most_common(top_n)


####################################################################################################
# INPUT ############################################################################################
####################################################################################################
result = count_top_words(
    'WORDS_INPUT.txt',
    exclude_list=[
'de',
'para',
'na',
'em',
'com',
'o',
'a',
],
    top_n=10)

for r in result:
    print(r)
