import pandas as pd
from src.RelRowStrategy import *

class RelationsTableBuilder:
    def __init__(self, data, strategy):
        # Data is a slice of the main data set
        # Expected columns = [name, raw_html, source_name, source_url, concept_type]
        # data must have at least one row
        self.table = pd.DataFrame()
        self.data = data
        self.strategy = strategy

    def build_table(self):
        # Grab first source name
        print("> Building table")
        print("> > Building unexploded table...")
        temp_table = pd.DataFrame()
        # We create a DataFrame of source -> list_of_destinations
        for index, row in self.data.iterrows():
            # Run the strategy algorithm
            new_row = self.strategy.build_row(row)
            # Convert row to pd.Series
            if (len(new_row) != 0):
                row_df = pd.DataFrame(new_row).T
                # Append
                temp_table = pd.concat([temp_table, row_df], axis=0)
        # Save to class table
        temp_table = temp_table.reset_index(drop=True)
        self.table = temp_table.copy()

        self.table.columns = ["from_string", "relations", "rel_type", "source_name", "source_url", "concept_type"]

        print("> > Building exploded table")
        # Clean up relations column
        self.table["relations"] = self.table["relations"].str.replace("[", "", regex=False)
        self.table["relations"] = self.table["relations"].str.replace(r"\s+", " ", regex=True) # removes white space
        self.table["relations"] = self.table["relations"].str.replace("]", "", regex=False)
        self.table["relations"] = self.table["relations"].str.replace("'", "", regex=False)

        print(f"> > > Before explosion length: {len(self.table)}")

        self.table = self.table.assign(relations=self.table["relations"].str.split(",")).explode("relations")
        self.table.rename(columns={"relations" : "to_string"}, inplace=True)
        self.table.reset_index(drop=True, inplace=True)

        self.table["to_string"] = self.table["to_string"].str.replace("@@@", ",", regex=False).str.strip()
        self.table["to_string"] = self.table["to_string"].str.replace(r"\\n \\n ", "\n", regex=True)

        print(f"> > > After explosion length: {len(self.table)}")
        print("> > Sneak peek at final table:")
        print(self.table.head(5))

        print(f"> > > resulted len: {len(self.table)}")
        print(f"> > > resulted columns: {self.table.columns}")

    def fix_sources(self):
        print("> Fixing sources (TEMP)")
        df = self.data.copy()
        df["match"] = df.apply(lambda x : x[2] in x[3], axis=1)
        df = df.loc[df["match"] == True]
        self.data = df.copy()
        self.data = self.data.drop(columns=["match"])

    def dump_table(self, path, name):
        if path[len(path) - 1] == "/":
            path = path[:-1]
        full_path = path + "/" + name + ".csv"
        print(f"> Dumping to {full_path}")
        self.table.to_csv(full_path, index=False)