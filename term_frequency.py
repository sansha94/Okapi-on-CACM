from collections import Counter
import numpy as np


def tf(query_list, doc_splitted):
    # Counting words in document
    counter = Counter(doc_splitted)

    term_freq = {}

    # Calculating tf
    for q in query_list:
        if q in counter:
            term_freq[q] = round(1+np.log2(counter[q]), 3)

    return term_freq
