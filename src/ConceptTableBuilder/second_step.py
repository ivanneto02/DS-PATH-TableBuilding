from .single_string_query import single_string_query
import re
from .filter_words import filter_words

def clean_string(x):
    x = x.lower()
    x = x.replace("and", "")
    x = x.strip()
    return x

def get_cui(x, connection):
    x = x.replace('"', "")
    queries = []
    if "— see" in x:
        left, right = ( x.strip() for x in x.split("— see") )
        queries.append(single_string_query(left)) # left concept query
        queries.append(single_string_query(right)) # right concept query
    elif ("(" in x) or (")" in x):
        regex_exp = r"\(.+?\)"
        insi_par = [ i.strip().replace("(", "").replace(")", "") for i in re.findall(regex_exp, x) ]
        outs_par = [ i.strip() for i in re.split(regex_exp, x) ]
        strings = insi_par + outs_par
        queries += [ single_string_query(i) for i in strings ]
    elif "," in x:
        x = x.replace("(", ",")
        x = x.replace(")", ",")
        x = x.replace("[", ",")
        x = x.replace("]", ",")
        strings = x.split(",")
        strings = [ clean_string(i) for i in strings ]
        queries += [ single_string_query(i) for i in strings ]
    elif ("[" in x) or ("]" in x):
        regex_exp = r"\[.+?\]"
        insi_par = [ i.strip().replace("[", "").replace("]", "") for i in re.findall(regex_exp, x) ]
        outs_par = [ i.strip() for i in re.split(regex_exp, x) ]
        strings = insi_par + outs_par
        queries += [ single_string_query(i) for i in strings ]
    else:
        x = x.split(" ")
        x = list(filter(lambda i: i not in filter_words, x))
        x = " ".join(x)
        queries.append( single_string_query(x) )
    CUIs = []
    for query in queries:
        cursor = connection.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        cursor.close()
        if len(response) == 0:
            continue
        else:
            CUIs.append(response[0][0])

    # Always return the first CUI
    if len(CUIs) == 0:
        return None
    return CUIs[0]

def run_second_step(df=None, connection=None):
    df["CUI"] = df["name"].apply(lambda x: get_cui(x, connection))
    return df