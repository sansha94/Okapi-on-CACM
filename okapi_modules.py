import numpy as np

k1 = 1.2
b = 0.75
k3 = 7

def term_frequency(query, documents):
    for q in query:
        for child in documents:
            temp = child[1].text.split()
            if q in temp:
                index = temp.index()


def idf(N:int, n:int):
    '''
    Calculation of idf for term q-i in Query Q

     N: No. of documents in the collection
     query_term: i-th query term in the query Q
     n: No. of documents containing q-i

     return: idf value
    '''
    return np.log10((N - n + 0.5) / (n + 0.5))

def document_length(root):
    '''
    Calculating the document length
    :return: document length
    '''
    doc_length = []
    for child in root:
        doc_length.append(len(child[1].text))

    return doc_length


def average_document_length():
    doc_length =