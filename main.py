from utils import *

FILE_PATH = 'data/shakespeare.txt'
INSERT_COST = 1
DELETE_COST = 1
REPLACE_COST = 2
N_SUGGESTIONS = 5


with open(FILE_PATH, 'r') as f:
    data = f.read()

vocab = prepare_corpus(data=data)
counts = get_word_counts(vocab)
probs = get_word_probs(counts)

def autocorrect(wrong_word):
    suggestions = get_suggestions(word=wrong_word, vocab=vocab, probs=probs, n_suggestions=N_SUGGESTIONS)

    if not suggestions:
        print(f"No suggestions found for '{wrong_word}'.")
    else:
        costs = []
        print(f"\nInstead of {wrong_word}, did you mean:")
        for word, prob in suggestions:
            print(f"{word}, with a probability of: {prob}")

        for word, _ in dict(suggestions).items():
            cost, _, steps = min_edit_distance(
                source=wrong_word, target=word, insert_cost=INSERT_COST,
                delete_cost=DELETE_COST, replace_cost=REPLACE_COST
            )
            costs.append((word, cost, steps))

        print("\nLeast costly operations in ascending order:\n")
        for cost in sorted(costs, key=lambda x: x[1]):
            print(f"{cost[0]}\nCost: {cost[1]}")
            print(f"Steps taken: {', '.join(cost[2])}\n")


def gene_sequence(sequence1, sequence2):
    min_distance, _,_ = min_edit_distance(
    source=sequence1, target=sequence2, insert_cost=INSERT_COST, 
    delete_cost=DELETE_COST, replace_cost=REPLACE_COST)

    print(f'sequence 1: {sequence1}')
    print(f'sequence 2: {sequence2}')
    print(f"Minimum edit distance between {sequence1} and {sequence2}:", min_distance)



if __name__=='__main__':
    print('1: autocorrect\n2:gene sequencing\nany: quit.')
    item = int(input('select menu item: '))
    if item == 1:
        wrong_word = input('Enter a wrong word for suggestions: \n')
        autocorrect(wrong_word=wrong_word)
        exit()
    elif item ==2:
        sq1 = str(input('input gene sequence 1:\n> '))
        sq2 = str(input('input gene sequence 2:\n> '))
        gene_sequence(sequence1=sq1, sequence2=sq2)
        exit()
    else:
        exit(1)

# example sequences
# sequence1 = "ACGTACGTACGT"
# sequence2 = "ACGTAAGTACGG"