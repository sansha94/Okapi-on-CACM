from glob import glob
import co_occurence as co_occur

# JSON files
files = sorted(glob('data/*.json'))

# Documents
documents = co_occur.xml_to_dict('data/doc.xml')

top10_docs = co_occur.json_to_dict(files[0])
top15_docs = co_occur.json_to_dict(files[1])
top25_docs = co_occur.json_to_dict(files[2])
top5_docs = co_occur.json_to_dict(files[3])
