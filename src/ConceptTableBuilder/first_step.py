from .single_string_query import single_string_query

def get_cui(x, connection):
    x = x.replace('"', "")
    cursor = connection.cursor()
    query = single_string_query(x)
    cursor.execute(query)
    CUI = cursor.fetchall()
    cursor.close()
    if len(CUI) == 0:
        return None
    return CUI[0][0]

def run_first_step(df=None, connection=None):
    df["CUI"] = df["name"].apply(lambda x: get_cui(x, connection))
    return df