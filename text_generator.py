import random
from collections import Counter
from collections import defaultdict
from typing import List

from nltk.tokenize import WhitespaceTokenizer
from nltk.util import trigrams

SENTENCE_ENDINGS = ('.', '!', '?')
SENTENCE_COUNT = 11
SENTENCE_MIN_WORDS = 3


def read_input_data(filename: str) -> str:
    """Reads an input file and returns it's text"""

    with open(filename, 'r') as f:
        data = f.read()

    return data


def create_tokens(text: str) -> list:
    """Returns a list of tokens split by the whitespace using nltk module"""

    tbw = WhitespaceTokenizer()
    tokens_list = tbw.tokenize(text)

    return tokens_list


def create_data_set(token_lst: List[str]) -> dict:
    """Returns a dict {head1_head2: [(tail, frequency)] ... }
     (a Markov model"""

    temp_dict = defaultdict(list)  # a dict to place temp data there
    data_dict = {}  # a dict for results
    trigram = list(trigrams(token_lst))  # a trigram from the corpus

    for i in trigram:
        temp_dict[i[0] + ' ' + i[1]].append(i[2])

    for k, v in temp_dict.items():
        data_dict[k] = Counter(v).most_common()

    return data_dict


def get_first_word(data: dict) -> str:
    """Returns a random word from the data
     to start a sentence in the future"""

    seq = list(data.keys())
    first_word = random.choice(seq)

    while (first_word.split()[0][-1] in SENTENCE_ENDINGS
           or not first_word[0].isupper()):
        first_word = random.choice(seq)

    return first_word


def print_results(data_dict: dict, first_word: str) -> None:
    """Prints (SENTENCE_COUNT - 1) sentences with
    minimum (SENTENCE_MIN_WORDS+ 2) words in each"""

    counter = 0
    while (counter < SENTENCE_MIN_WORDS
           or first_word[-1] not in SENTENCE_ENDINGS):

        splitted_word = first_word.split()

        next_word = data_dict[first_word]
        candidates = [i[0] for i in next_word]
        probables = list(map(int, [i[1] for i in next_word]))

        print(splitted_word[0], end=' ')
        first_word = (splitted_word[1] + ' '
                      + random.choices(candidates, probables)[0])

        counter += 1
    else:
        print(first_word, end=' ')


def main() -> None:
    """A Controller function"""

    corpus = read_input_data(input())
    tokens_list = create_tokens(corpus)
    data_dict = create_data_set(tokens_list)

    for i in range(1, SENTENCE_COUNT):
        first_word = get_first_word(data_dict)
        print_results(data_dict, first_word)
        print()  # for a new line


if __name__ == '__main__':
    main()
