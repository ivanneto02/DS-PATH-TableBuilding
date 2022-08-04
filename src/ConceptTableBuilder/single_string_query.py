def single_string_query(string=""):
    QUERY = f"SELECT CUI, STR FROM MRCONSO WHERE STR LIKE \"{string}\" LIMIT 1;"
    return QUERY