from glob import glob
import co_occurence as co_occur
from nltk.corpus import stopwords

# JSON files
files = sorted(glob('data/*.json'))

# Stopwords
stop_words = set(stopwords.words('english'))

# Pattern keeping only digits and strings
pattern = r'(\d+|\w+)'

# Documents
documents = co_occur.xml_to_dict('data/doc.xml', stop_words, pattern)

top10_docs = co_occur.json_to_dict(files[0])
top15_docs = co_occur.json_to_dict(files[1])
top25_docs = co_occur.json_to_dict(files[2])
top5_docs = co_occur.json_to_dict(files[3])

term_pool_top5 = co_occur.term_pool(top5_docs, documents)
term_pool_top10 = co_occur.term_pool(top10_docs, documents)
term_pool_top15 = co_occur.term_pool(top15_docs, documents)
term_pool_top25 = co_occur.term_pool(top25_docs, documents)
