import os
import re
import json
from html_reader import HTMLReader 

class OverstockRegularExpressionExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()

    def extract_titles(self):
        title_pattern = r'<b>([\d]{1,2}-kt\.?.*?(?:\s*\([^)]+\))?)</b>'
        titles = re.findall(title_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return titles

    def extract_list_prices(self):
        list_price_pattern = r'<b>List Price:</b></td><td align="left" nowrap="nowrap"><s>([^<]+)</s></td>'
        list_prices = re.findall(list_price_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return list_prices

    def extract_prices(self):
        price_pattern = r'<b>Price:</b></td><td align="left" nowrap="nowrap"><span class="bigred"><b>([^<]+)</b></span></td>'
        prices = re.findall(price_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return prices

    def extract_savings(self):
        savings_pattern = r'<b>You Save:</b></td><td align="left" nowrap="nowrap"><span class="littleorange">(\$[\d,.]+) \(([\d]+%)\)</span></td>'
        savings = re.findall(savings_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return savings

    def extract_content(self):
        content_pattern = r'</b></a><br>\s*<table>.*?<td valign="top"><span class="normal">([\s\S]*?<a href="[^"]+"><span class="tiny"><b>Click here to purchase\.</b></span></a>)'
        contents = re.findall(content_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return contents

    def to_json(self, save=True):
        if not self.html_content:
            print("No HTML content to process.")
            return []

        extracted_titles = self.extract_titles()
        extracted_prices = self.extract_prices()
        extracted_list_prices = self.extract_list_prices()
        extracted_savings = self.extract_savings()
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
    
class RtvsloRegularExpressionExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()
        
    def extract_author(self):
        author_pattern = r'<div class="author-name">(.*?)</div>'
        author = re.findall(author_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return author[0]
    
    def extract_published_time(self):
        publish_time_pattern = r'<div class="publish-meta">\s*([^<]+)'
        publish_times = re.findall(publish_time_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return publish_times [0]

    def extract_title(self):
        title_pattern = r'<h1[^>]*>(.*?)<\/h1>'
        titles = re.findall(title_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return titles[0]

    def extract_subtitle(self):
        subtitle_pattern = r'<div class="subtitle">(.*?)<\/div>'
        subtitles = re.findall(subtitle_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return subtitles[0] 

    def extract_lead(self):
        lead_pattern = r'<p class="lead">(.*?)<\/p>'
        leads = re.findall(lead_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return leads[0]

    def extract_content(self):
        content_pattern = r'<div class="article-body">.*?(<p.*?>.*?<\/p>)+.*?<\/div>'
        match = re.search(content_pattern, self.html_content, re.IGNORECASE | re.DOTALL)

        content_html = match.group(0)
        content_html = content_html.replace('"', '\\"')  

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

if __name__ == '__main__':
    # Overstock jewelry 1 page
    # jewelry_01_file = '../input-extraction/WebPages/overstock.com/jewelry01.html'
    # extractor = OverstockRegularExpressionExtractor(file_path=jewelry_01_file, save_dir='./results/jewelry1/')
    # json_data = extractor.to_json()
    # print(json.dumps(json_data, indent=4))

    # Overstock jewelry 2 page
    # jewelry_02_file = '../input-extraction/WebPages/overstock.com/jewelry02.html'
    # extractor2 = OverstockRegularExpressionExtractor(file_path=jewelry_02_file, save_dir='./results/jewelry2/')
    # json_data2 = extractor2.to_json()
    # print(json.dumps(json_data2, indent=4))

    # Rtvslo Audi page
    # audi_file = '../input-extraction/WebPages/rtvslo.si/audi.html'
    # extractor3 = RtvsloRegularExpressionExtractor(file_path=audi_file, save_dir='./results/audi/')
    # json_item = extractor3.to_json()
    # print(json_item)

    # Rtvslo Volvo
    volvo_file = '../input-extraction/WebPages/rtvslo.si/volvo.html'
    extractor4 = RtvsloRegularExpressionExtractor(file_path=volvo_file, save_dir='./results/volvo/')
    json_item2 = extractor4.to_json()
    print(json_item2)

