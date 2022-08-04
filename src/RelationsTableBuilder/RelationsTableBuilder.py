import pandas as pd
from src.RelRowStrategy import *
from src.ConceptTableBuilder import run_third_step
from config import *
import src.UMLSConnector as connector

class RelationsTableBuilder:
    def __init__(self, data, strategy):
        # Data is a slice of the main data set
        # Expected columns = [name, raw_html, source_name, source_url, concept_type]
        # data must have at least one row
        self.table = pd.DataFrame()
        self.data = data
        self.strategy = strategy

    def build_table(self):
        print(f"> > > Dropping duplicates and resetting index")
        self.data.drop_duplicates(inplace=True, subset=["name", "source_name", "source_url", "concept_type"])
        self.data.reset_index(inplace=True, drop=True)

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

        print("> > Renaming columns")
        print(self.table.head(10))
        print(self.table.columns)
        self.table.columns = ["from_string", "CUI1", "relations", "rel_type", "source_name", "source_url", "concept_type", "date_time_scraped"]

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
        df["match"] = df.apply(lambda x : x[3] in x[4], axis=1)
        df = df.loc[df["match"] == True]
        print(df.loc[df["match"] != True].head(20))
        self.data = df.copy()
        self.data = self.data.drop(columns=["match"])

    def map_relation_cuis(self):
        print("> Mapping relation cuis")
        df = self.table.copy()

        print("    > Establishing MySql connection")
        connection = connector.connect(
            host = MYSQL_HOST,
            database = MYSQL_DATABASE,
            user = MYSQL_USERNAME,
            password = MYSQL_PASSWORD)

        print("    > Copying resulting table")
        df = run_third_step(df=df, name="to_string", connection=connection)
        self.table = df.copy()

    def dump_table(self, path, name):
        if path[len(path) - 1] == "/":
            path = path[:-1]
        full_path = path + "/" + name + ".csv"
        print(f"> Dumping to {full_path}")
        self.table.to_csv(full_path, index=False)