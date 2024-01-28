from utils import *

FILE_PATH ='data/shakespeare.txt'

with open(FILE_PATH, 'r') as f:
    data = f.read()

vocab = prepare_corpus(data=data)
counts = get_word_counts(vocab)
probs = get_word_probs(counts)

print(get_suggestions('al', vocab=vocab, probs=probs))