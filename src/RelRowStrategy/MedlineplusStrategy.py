from .RelRowStrategy import RelRowStrategy
from bs4 import BeautifulSoup
import pandas as pd

class MedlineplusStrategy(RelRowStrategy):
    def build_row(self, row):
        # Create brand name relations
        # Expected columns = [name, raw_html, source_name, source_url, concept_type]
        date_time_scraped = row["date_time_scraped"]
        from_string = row["name"] # Name column
        relation_type1 = "has_tradename"
        relation_type2 = "part_of"
        source_name = row["source_name"] # source_name column
        source_url = row["source_url"] # source_url column
        concept_type = row["concept_type"]

        row1_list = []
        row2_list = []

        # Find brand name relationship
        try:
            from_string = row["name"]
            text = row["raw_html"]
            soup = BeautifulSoup(text, "lxml")
            content = soup.find("div", attrs={"id" : "section-brandname-1"})
            li = content.find_all("li")

            brand_relations = []
            for item in li:
                try:
                    item.find("sup").decompose()
                except:
                    pass
                try:
                    item.find("a").decompose()
                except:
                    pass
                brand_relations.append(item.text.strip().replace(",", "@@@"))

            row1_list = [from_string, str(brand_relations), relation_type1, source_name, source_url, concept_type, date_time_scraped]
        except Exception as e:
            print("No brand relation found", from_string)
            print(e)
            row1_list = None
        
        try:
            content = soup.find("div", attrs={"id" : "section-brand-name-2"})
            li = content.find_all("li")

            comp_relations = []
            for item in li:
                try:
                    item.find("sup").decompose()
                except:
                    pass
                try:
                    item.find("a").decompose()
                except:
                    pass
                comp_relations.append(item.text.strip().replace(",", "@@@"))
            row2_list = [from_string, str(comp_relations), relation_type2, source_name, source_url, concept_type, date_time_scraped]
        except Exception as e:
            print("No comp relation found", from_string)
            print(e)
            row2_list = None

        # Return depending on which list is there
        if row1_list and row2_list:
            return pd.DataFrame(list(zip(row1_list, row2_list)))
        elif row1_list:
            return pd.DataFrame(row1_list)
        elif row2_list:
            return pd.DataFrame(row2_list)
        else:
            print("No relation found:", from_string)
            return list()