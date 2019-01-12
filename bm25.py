import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import term_frequency as tf
import inverse_doc_frequency as idf
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Total documents in the collection
N = 1575

# Pattern keeping only digits and strings
pattern = r'(\d+|\w+)'

# Queries with stopwords
queries = pd.read_csv('data/queries_with_stopwords.csv')

# Stopwords
stop_words = set(stopwords.words('english'))

# Documents
tree = ET.parse('data/doc.xml')
root = tree.getroot()

# Query term frequency
query_tf = {}

# Query inverse document frequency
query_idf = {}

# Document length
doc_length = {}

# Average document length
avg_doc_length = 0

# Okapi scores
scores = {}

# Okapi Constants
k1 = 0.2
b = 0.75
k3 = 7.0
qtf = 1

# Calculating document length
for doc_no, child in enumerate(root, start=1):
    doc = regexp_tokenize(child[0].text, pattern)
    doc = [d.lower() for d in doc]

    # Removing stopwords from document
    doc = [w for w in doc if not w in stop_words]
    doc_length['Doc ' + str(doc_no)] = len(doc)

avg_doc_length = round(sum(doc_length.values()) / N, 3)

# Calculating term frequency
for q_no, query in enumerate(queries['Query'], start=1):
    query = regexp_tokenize(query, pattern)
    query = [q.lower() for q in query]

    # Removing stopwords from query
    query = [w for w in query if w not in stop_words]
    query = set(query)
    term_freq = []

    for child in root:
        doc = regexp_tokenize(child[0].text, pattern)
        doc = [d.lower() for d in doc]

        # Removing stopwords from document
        doc = [w for w in doc if w not in stop_words]
        term_freq.append(tf.tf(query, doc))

    query_tf['Query ' + str(q_no)] = term_freq

# Calculating inverse document frequency
for query in queries['Query']:
    query = regexp_tokenize(query, pattern)
    query = [q.lower() for q in query]
    query = set(query)

    for q in query:
        if q not in query_idf:
            query_idf[q] = 0
            for child in root:
                doc = regexp_tokenize(child[0].text, pattern)
                doc = [d.lower() for d in doc]
                doc = set(doc)

                if q in doc:
                    query_idf[q] += 1

            if query_idf[q] > 0:
                query_idf[q] = round(np.log2((N - query_idf[q] + 0.5)/ (query_idf[q] + 0.5)), 3)

q_no = 0

# Pseudo relevance feedback based selection Okapi-BM25
for query in queries['Query']:
    query = regexp_tokenize(query, pattern)
    query = [q.lower() for q in query]
    # Removing stopwords from query
    query = [w for w in query if w not in stop_words]
    query = set(query)

    q_no += 1

    doc_score = {}

    for tf in query_tf:
        score = 0
        for i in range(N):

            if len(query_tf[tf][i]) > 0:
                for term in query_tf[tf][i]:
                    K = k1 * ((1 - b) + (b * (doc_length['Doc '+str(i+1)] / avg_doc_length)))
                    temp = query_idf[term] * ((k1+1) * query_tf[tf][i][term]) * (k3 + 1)
                    score += round(temp / ((K + query_tf[tf][i][term]) *(k3+1)), 3)

                doc_score['Doc ' + str(i+1)] = score
            else:
                doc_score['Doc ' + str(i+1)] = 0.0

    scores['Query 1'] = doc_score

print(query_tf['Query 1'])
print(scores['Query 1'])
