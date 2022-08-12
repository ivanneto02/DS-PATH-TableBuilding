from .RelRowStrategy import RelRowStrategy
from bs4 import BeautifulSoup
import pandas as pd

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

        print(from_string, ",")

        row_lists = []
        # Find all relationships at once
        try:
            from_string = row["name"]
            text = row["raw_html"]
            soup = BeautifulSoup(text, "lxml")
            content = soup.find("p", attrs={"class" : "drug-subtitle"})
            titles = content.find_all("b")

            print(titles[2])

            curr_row = []
            for title in titles:
                title_text = title.text
                title_sibling = title.next_sibling

                # clean sibling
                title_sibling_text = title_sibling.text.replace("[", "").strip()
                print(f"title_sibling: {title_sibling_text}")

                if "generic" in title_text.lower():
                    curr_row = [from_string, cui1, title_sibling_text, relation_type1, source_name, source_url, concept_type, date_time_scraped]
                elif "brand" in title_text.lower():
                    curr_row = [from_string, cui1, title_sibling_text, relation_type2, source_name, source_url, concept_type, date_time_scraped]
                elif "dosage" in title_text.lower():
                    curr_row = [from_string, cui1, title_sibling_text, relation_type3, source_name, source_url, concept_type, date_time_scraped]
                elif "drug class" in title_text.lower():
                    title_sibling_text = title_sibling.next_sibling.text.replace("[", "").strip()
                    curr_row = [from_string, cui1, title_sibling_text, relation_type4, source_name, source_url, concept_type, date_time_scraped]
                row_lists.append(curr_row)

        except Exception as e:
            print("A relation processing step has failed", from_string)
            print(e)
            row1_list = None

        if len(row_lists) == 0:
            print("No relations found")
            return list()

        for row in row_lists:
            print(row)

        zipped = zip(row_lists)
        return pd.DataFrame(list(zipped))