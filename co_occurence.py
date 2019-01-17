import xml.etree.ElementTree as et
import json
from nltk.tokenize import regexp_tokenize


def xml_to_dict(file_name: str, stop_words, pattern):
    docs = {}

    tree = et.parse(file_name)
    root = tree.getroot()

    for index, child in enumerate(root, start=1):
        doc = regexp_tokenize(child[0].text, pattern)
        doc = [d.lower() for d in doc]

        # Removing stopwords from document
        doc = [w for w in doc if w not in stop_words]
        doc = set(doc)
        docs['Doc ' + str(index)] = ' '.join(doc)

    return docs


def json_to_dict(file_name: str):
    scores = {}

    with open(file_name, 'r') as fp:
        scores = json.load(fp)

    return scores


def term_pool(scores_dict: dict, documents: dict):
    terms = {}

    for query in scores_dict:
        terms[query] = {}

        for doc in scores_dict[query]:
            terms[query][doc] = documents[doc]

    return terms
