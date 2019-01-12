import pandas as pd

# Reading the collection of documents
file = open('/home/sanket/PycharmProjects/word2vec/CACM/cacm.all', 'r')
documents = file.read()

# Replacing the delimiters .I, .T, .A, .N, .X
delimiters = ['.I', '.T', '.A', '.N', '.X']

for delim in delimiters:
    documents = documents.replace(delim, '')

documents = documents.split('\n')

# Cleaning of queries
documents = [document.lstrip() for document in documents if document not in ['', ' ']]

int_indexes = []
doc_no = []
doc_title = []

num_ascii = list(range(48, 58))

for index in range(len(documents)):
    if documents[index].find('\t') == -1:
        if isinstance(documents[index], int):
            if (ord(documents[index][0]) in num_ascii):
                int_indexes.append(index)
        elif documents[index] == '.B':
            int_indexes.append(index)


print(len(int_indexes))
for index in range(0, len(int_indexes), 2):

    doc_no.append(int(documents[int_indexes[index]]))
    doc_title.append(' '.join(documents[int_indexes[index]+1:int_indexes[index+1]]))

# for i in int_indexes[190:200]:
#     print(documents[i])
# for i in int_indexes[::]:
#     print(documents[i])

# print(int_indexes[-5:])
# print(documents[95315])
