from nltk.tokenize import regexp_tokenize
import json


def document_length(root, pattern, stop_words: set):
    doc_length = {}
    for doc_no, child in enumerate(root, start=1):
        doc = regexp_tokenize(child[0].text, pattern)
        doc = [d.lower() for d in doc]

        # Removing stopwords from document
        doc = [w for w in doc if not w in stop_words]
        doc_length['Doc ' + str(doc_no)] = len(doc)

    return doc_length


def average_document_length(doc_length, N):
    return round(sum(doc_length.values()) / N, 3)


def to_dict(sorted_list):
    d = {}

    for l in sorted_list:
        d[l[0]] = l[1]

    return d


def write_json(scores_dict, file_name: str):

    with open('data/'+file_name+'.json', 'w') as fp:
        json.dump(scores_dict, fp, indent=4)
