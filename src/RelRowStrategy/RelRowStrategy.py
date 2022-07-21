class RelRowStrategy:
    def __init__(self):
        # We will return one or multiple rows:
        # from_string, to_string, relation_type, source_name, source_url
        pass

    def build_row(self, row):
        '''Override this function for each strategy'''
        pass