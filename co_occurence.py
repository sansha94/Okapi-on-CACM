import xml.etree.ElementTree as et
import json


def xml_to_dict(file_name: str):
    docs = {}

    tree = et.parse(file_name)
    root = tree.getroot()

    for index, child in enumerate(root, start=1):
        description = child[0].text.replace('\n', '')
        description = description.replace('\t', '')
        description = description.lstrip().rstrip()
        docs['Doc ' + str(index)] = description

    return docs


def json_to_dict(file_name: str):
    scores = {}

    with open(file_name, 'r') as fp:
        scores = json.load(fp)

    return scores
