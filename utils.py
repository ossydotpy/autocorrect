import re
from collections import Counter
from string import ascii_lowercase


def split_word(word):
    """
    Splits a word into all possible combinations of left and right substrings.

    Args:
    word (str): The word to be split.

    Returns:
    list: A list of tuples containing all possible splits of the word.
    """

    splits = []
    for i in range(len(word) + 1):
        splits.append((word[0:i], word[i:]))
    return splits

def delete_one_letter(word):
    """
    Generates a list of words by deleting one letter from the input word.

    Args:
    word (str): The input word.

    Returns:
    list: A list of words obtained by deleting one letter from the input word.
    """

    new_words = []
    splits = split_word(word)
    for split in splits:
        L, R = split
        if len(R) > 0:
            new_words.append(L + R[1:])
    return new_words

def insert_one_letter(word):
    """
    Generates a list of words by inserting one letter into the input word.

    Args:
    word (str): The input word.

    Returns:
    list: A list of words obtained by inserting one letter into the input word.
    """

    new_words = []
    splits = split_word(word)
    for split in splits:
        L, R = split
        for letter in ascii_lowercase:
            new_word = L + letter + R
            new_words.append(new_word)

    return new_words

def switch_one_letter(word):
    """
    Generates a list of words by switching adjacent letters in the input word.

    Args:
    word (str): The input word.

    Returns:
    list: A list of words obtained by switching adjacent letters in the input word.
    """

    new_words = []
    splits = split_word(word)
    for split in splits:
        L, R = split
        if len(R) > 1:
            new_words.append(L + R[1] + R[0] + R[2:])

    return new_words

def replace_one_letter(word):
    """
    Generates a list of words by replacing each letter of the input word with every letter of the alphabet.

    Args:
    word (str): The input word.

    Returns:
    list: A list of words obtained by replacing each letter of the input word with every letter of the alphabet.
    """

    new_words = []
    splits = split_word(word)
    for split in splits:
        L, R = split
        if len(R) > 0:
            for letter in ascii_lowercase:
                new_word = L + letter + R[1:]
                new_words.append(new_word)
    new_words_set = set(new_words)
    new_words_set.discard(word)
    new_words = sorted(list(new_words_set))
    return new_words

def edit_one_letter(word, allow_switches=False):
    """
    Generates a set of words that are one edit away from the input word.

    Args:
    word (str): The input word.
    allow_switches (bool): Whether to allow switching adjacent letters. Default is False.

    Returns:
    set: A set of words that are one edit away from the input word.
    """

    edits = set()
    edits.update(insert_one_letter(word))
    edits.update(delete_one_letter(word))
    edits.update(replace_one_letter(word))
    if allow_switches:
        edits.update(switch_one_letter(word))

    return edits

def edit_two_letters(word, allow_switches=False):
    """
    Generates a set of words that are two edits away from the input word.

    Args:
    word (str): The input word.
    allow_switches (bool): Whether to allow switching adjacent letters. Default is False.

    Returns:
    set: A set of words that are two edits away from the input word.
    """

    edits = set()
    for edit in edit_one_letter(word, allow_switches=allow_switches):
        two_edits = edit_one_letter(edit, allow_switches=allow_switches)
        edits.update(two_edits)
    return edits

def prepare_corpus(data):
    """
    Preprocesses the input data by extracting words and converting them to lowercase.

    Args:
    data (str): The input text data.

    Returns:
    list: A list of preprocessed words extracted from the input data.
    """

    words = re.findall(r'\w+', data.lower())
    return words

def get_word_counts(data):
    """
    Computes the frequency of each word in the input data.

    Args:
    data (list): A list of words.

    Returns:
    Counter: A Counter object containing the frequency of each word.
    """

    return Counter(data)

def get_word_probs(word_counts: dict):
    """
    Computes the probability of each word based on its frequency.

    Args:
    word_counts (dict): A dictionary containing word counts.

    Returns:
    dict: A dictionary containing the probability of each word.
    """

    prob_dict = {}
    for word, count in word_counts.items():
        prob_dict[word] = count / len(word_counts)
    return prob_dict

def get_suggestions(word, vocab, probs, n_suggestions=5):
    """
    Generates spelling suggestions for a given word based on the vocabulary and word probabilities.

    Args:
    word (str): The input word.
    vocab (set): A set of valid words in the vocabulary.
    probs (dict): A dictionary containing the probability of each word.
    n_suggestions (int): The number of suggestions to generate. Default is 5.

    Returns:
    list: A list of spelling suggestions for the input word.
    """

    suggestions = []
    best_words = {}
    if word in vocab:
        suggestions.append(word)

    for suggestion in edit_one_letter(word).intersection(edit_two_letters(word)):
        if suggestion in vocab:
            suggestions.append(suggestion)
    for word in suggestions:
        best_words[word] = probs.get(word, 0)

    top_n = Counter(best_words).most_common(n_suggestions)
    return top_n
