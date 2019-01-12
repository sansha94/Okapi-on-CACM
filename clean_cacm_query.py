import pandas as pd

# Reading the file query.text
file = open('CACM/query.text', 'r')
queries = file.read()

# Replacing the delimiters .I, .W, .N
delimiters = ['.I', '.W', '.N']

for delim in delimiters:
    queries = queries.replace(delim, '')

queries = queries.split('\n')

# Cleaning of queries
queries = [query.lstrip() for query in queries if query not in ['', ' ']]

# Handling the none type
queries = queries[:103] + queries[104:]

int_indexes = []
query_no = []
query = []

num_ascii = list(range(48, 58))

for index in range(len(queries)):
    if ord(queries[index][0]) in num_ascii:
        int_indexes.append(index)

int_indexes = int_indexes[::2] + [324]

for index in range(len(int_indexes)-1):
    query_no.append(int(queries[int_indexes[index]]))
    query.append(' '.join(queries[int_indexes[index]+1:int_indexes[index+1]-1]))

# Converting to Dataframe
queries = pd.DataFrame({'Query_No': query_no, 'Query': query})

# Converting to csv for future use
queries.to_csv('queries_with_stopwords.csv', index=False)

file.close()
