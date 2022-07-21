from .RelRowStrategy import RelRowStrategy

from bs4 import BeautifulSoup

import pandas as pd

class MayoclinicRelRowStrategy(RelRowStrategy):
    def build_row(self, row):
        # Find brand name relationship
        try:
            text = row["raw_html"]
            soup = BeautifulSoup(text, "lxml")
            content = soup.find("div", attrs={"id" : "main-content"})
            ol = content.find("ol", attrs={"class" : "content"})
            items = ol.find_all("li")

            # Create brand name relations
            # Expected columns = [name, raw_html, source_name, source_url, concept_type]
            relations = [ item.text.strip() for item in items ]
            from_string = row["name"] # Name column
            relation_type = "has_tradename"
            source_name = row["source_name"] # source_name column
            source_url = row["source_url"] # source_url column
            concept_type = row["concept_type"]
            row_list = [from_string, str(relations), relation_type, source_name, source_url, concept_type]
            return pd.DataFrame(row_list)

        except:
            return list()