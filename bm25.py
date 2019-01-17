import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import term_frequency as tf
import okapi_modules as okapi
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

# Top documents
query_top5_docs = {}
query_top10_docs = {}
query_top15_docs = {}
query_top25_docs = {}

# Getting document length
doc_length = okapi.document_length(root, pattern, stop_words)

# Getting average document length
avg_doc_length = okapi.average_document_length(doc_length, N)

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

# Pseudo relevance feedback based selection Okapi-BM25
for q_no in range(1, 65):
    doc_score = {}
    query = 'Query ' + str(q_no)
    for i in range(N):
        score = 0
        if len(query_tf[query][i]) > 0:
            for term in query_tf[query][i]:
                K = k1 * ((1 - b) + (b * (doc_length['Doc ' + str(i + 1)] / avg_doc_length)))
                temp = query_idf[term] * ((k1 + 1) * query_tf[query][i][term]) * (k3 + 1)
                score += round(temp / ((K + query_tf[query][i][term]) * (k3 + 1)), 3)
        doc_score["Doc " + str(i + 1)] = score

    scores["Query " + str(q_no)] = doc_score

for score in scores:
    query_top5_docs[score] = okapi.to_dict(sorted(scores[score].items(), key=lambda x:x[1], reverse=True)[:5])
    query_top10_docs[score] = okapi.to_dict(sorted(scores[score].items(), key=lambda x:x[1], reverse=True)[:10])
    query_top15_docs[score] = okapi.to_dict(sorted(scores[score].items(), key=lambda x: x[1], reverse=True)[:15])
    query_top25_docs[score] = okapi.to_dict(sorted(scores[score].items(), key=lambda x: x[1], reverse=True)[:25])

t = ['query_top5_docs', 'query_top10_docs', 'query_top15_docs', 'query_top25_docs']

for i in t:
    okapi.write_json(eval(i), i[:-5])
