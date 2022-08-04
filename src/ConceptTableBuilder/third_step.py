from .single_string_query import single_string_query

from nltk.util import everygrams
import re
import Levenshtein as leven

import pandas as pd

def preprocess_string(x):
    regex = r"[^a-zA-Z0-9]"
    # Replaces all non-alphanumeric characters with ''
    x = re.sub(regex, " ", x)
    return x

def get_ngrams(x):
    split = x.split()
    return list(everygrams(split))

def get_cui(x, connection):
    x = preprocess_string(x)
    ngram_list = get_ngrams(x)

    # Execute queries, append distances
    # We also determine the minimum distance
    distances = []
    responses = []
    # print(x)
    for ngram in ngram_list:
        string = " ".join([x for x in ngram])
        query = single_string_query(string)
        cursor = connection.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        cursor.close()
        if len(response) == 0:
            continue

        distance = leven.distance(x, response[0][1])
        responses.append(response)
        distances.append(distance)

    if len(distances) == 0:
        return None
    
    min_d = distances[0]
    min_c = responses[0][0][0]
    for response, distance in zip(responses, distances):
        if distance < min_d:
            min_d = distance
            min_c = response[0][0]

    return min_c

def run_third_step(df=None, connection=None, name="name"):
    df["CUI2"] = df[name].apply(lambda x: get_cui(x, connection))
    return df