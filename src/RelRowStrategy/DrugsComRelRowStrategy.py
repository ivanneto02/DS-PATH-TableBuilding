from .RelRowStrategy import RelRowStrategy
from bs4 import BeautifulSoup
import pandas as pd
import re

class DrugsComRelRowStrategy(RelRowStrategy):
    def build_row(self, row):
        # Create brand name relations
        # Expected columns = [name, raw_html, source_name, source_url, concept_type]
        date_time_scraped = row["date_time_scraped"]
        cui1 = row["CUI"]
        from_string = row["name"] # Name column
        
        relation_type1 = "has_genericname"
        relation_type2 = "has_tradename"
        relation_type3 = "has_dosageform"
        relation_type4 = "has_drugclass"

        source_name = row["source_name"] # source_name column
        source_url = row["source_url"] # source_url column
        concept_type = row["concept_type"]

        row_lists = []
        # Find all relationships at once
        try:
            from_string = row["name"]
            text = row["raw_html"]
            soup = BeautifulSoup(text, "lxml")
            content = soup.find("p", attrs={"class" : "drug-subtitle"})
            titles = content.find_all("b")

            for title in titles:
                title_text = title.text
                iterator = title.next_sibling

                items = []
                while iterator:
                    if iterator.name == "br":
                        break
                    if ("show all" in iterator.text) or (len(iterator.text) < 3):
                        iterator = iterator.next_sibling
                        continue
                    items.append(re.sub('\[[^>]+\]', '', iterator.text).replace("[", "").strip())
                    iterator = iterator.next_sibling

                curr_row = []
                if "generic" in title_text.lower():
                    curr_row = [from_string, cui1, items[0], relation_type1, source_name, source_url, concept_type, date_time_scraped]
                elif "brand" in title_text.lower():
                    curr_row = [from_string, cui1, items, relation_type2, source_name, source_url, concept_type, date_time_scraped]
                elif "dosage" in title_text.lower():
                    curr_row = [from_string, cui1, items[0], relation_type3, source_name, source_url, concept_type, date_time_scraped]
                elif "drug class" in title_text.lower():
                    curr_row = [from_string, cui1, items[0], relation_type4, source_name, source_url, concept_type, date_time_scraped]

                row_lists.append(curr_row)
        except:
            pass

        if len(row_lists) == 0:
            return list()

        zipped = zip(*[l for l in row_lists])
        return pd.DataFrame(list(zipped))