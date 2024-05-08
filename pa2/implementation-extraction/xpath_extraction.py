import os
from lxml import html
import json
from html_reader import HTMLReader 

class OverstockXPathExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()
        self.tree = html.fromstring(self.html_content)

    def extract_titles(self):
        titles = self.tree.xpath("/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/b/text()")
        return titles
    
    def extract_list_prices(self):
        list_prices = self.tree.xpath("/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()")
        return list_prices
    
    def extract_prices(self):
        prices = self.tree.xpath("/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()")
        return prices
    
    def extract_savings(self):
        savings_raw = self.tree.xpath("/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()")
        
        savings = []
        for raw in savings_raw:
            modified = str(raw)
            # Split the string by space
            parts = modified.split()
        
            # Remove parentheses and their contents from the second part
            cleaned_second_part = ''.join(filter(lambda x: x not in '()', parts[1]))
        
            # Join the parts back together
            saving = (parts[0], cleaned_second_part)
            savings.append(saving)
		
        #print('===========')
        #print(savings[0])
        #print('===========')
        return savings
    
    def extract_content(self):
        contents = self.tree.xpath("/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()")
        return contents

    def to_json(self, save=True):
        if not self.html_content:
            print("No HTML content to process.")
            return []

        extracted_titles = self.extract_titles()
        extracted_prices = self.extract_prices()
        extracted_list_prices = self.extract_list_prices()
        extracted_savings = self.extract_savings()
        #print(extracted_savings)
        extracted_contents = self.extract_content()

        json_items = []
        for title, price, list_price, saving, content in zip(extracted_titles, extracted_prices, extracted_list_prices, extracted_savings, extracted_contents):
            saving_amount, saving_percent = saving 
            item = {
                "Title": title,
                "Price": price,
                "ListPrice": list_price,
                "Saving": saving_amount,
                "SavingPercent": saving_percent,
                "Content": content.strip()
            }
            json_items.append(item)

        if save:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)  
            json_filename = os.path.join(self.save_dir, 'extracted_data.json')
            with open(json_filename, 'w') as json_file:
                json.dump(json_items, json_file, indent=4)
        
        return json_items
		
class RtvsloXPathExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()
        self.tree = html.fromstring(self.html_content)
        
    def extract_author(self):
        authors = self.tree.xpath("//div[@class='article-meta']/div[@class='author']/div[@class='author-name']/text()")
        return authors[0]
    
    def extract_published_time(self):
        publish_times = self.tree.xpath("//div[@class='article-meta']/div[@class='publish-meta']/text()")
        return publish_times[0].strip()

    def extract_title(self):
        titles = self.tree.xpath("//header[@class='article-header']/h1/text()")
        return titles[0]

    def extract_subtitle(self):
        subtitles = self.tree.xpath("//header[@class='article-header']/div[@class='subtitle']/text()")
        return subtitles[0] 

    def extract_lead(self):
        leads = self.tree.xpath("//header[@class='article-header']/p[@class='lead']/text()")
        return leads[0]

    def extract_content(self):
        content_lines = self.tree.xpath("//div[@class='article-body']/article[@class='article']/p/text() | //div[@class='article-body']/article[@class='article']/p/strong/text()")
        content_html = "\n".join(content_lines)
        return content_html  

    def to_json(self, save=True):
        author = self.extract_author()
        published_time = self.extract_published_time()
        title = self.extract_title()
        subtitle = self.extract_subtitle()
        lead = self.extract_lead()
        content = self.extract_content()

        json_item = {
            "author": author,
            "published_time": published_time,
            "title": title,
            "subtitle": subtitle,
            "lead": lead,
            "content": content
        }

        if save:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)  
            json_filename = os.path.join(self.save_dir, 'extracted_data.json')
            with open(json_filename, 'w') as json_file:
                json.dump(json_item, json_file, indent=4)
        
        return json_item