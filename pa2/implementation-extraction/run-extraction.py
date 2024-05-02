import re
import json
from html_reader import HTMLReader 

class RegularExpressionExtractor:
    def __init__(self, file_path):
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()

    def extract_titles(self):
        if not self.html_content:
            print("No HTML content to process.")
            return []

        title_pattern = r'<b>([\d]{1,2}-kt\.?.*?(?:\s*\([^)]+\))?)</b>'
        titles = re.findall(title_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return titles
    
    def extract_list_prices(self):
        if not self.html_content:
            print("No HTML content to process.")
            return []

        list_price_pattern = r'<b>List Price:</b></td><td align="left" nowrap="nowrap"><s>([^<]+)</s></td>'
        list_prices = re.findall(list_price_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return list_prices
    
    def extract_prices(self):
        if not self.html_content:
            print("No HTML content to process.")
            return []

        price_pattern = r'<b>Price:</b></td><td align="left" nowrap="nowrap"><span class="bigred"><b>([^<]+)</b></span></td>'
        prices = re.findall(price_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return prices

    def extract_savings(self):
        if not self.html_content:
            print("No HTML content to process.")
            return []

        savings_pattern = r'<b>You Save:</b></td><td align="left" nowrap="nowrap"><span class="littleorange">(\$[\d,.]+) \(([\d]+%)\)</span></td>'
        savings = re.findall(savings_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        return savings
    
    def extract_content(self):
            if not self.html_content:
                print("No HTML content to process.")
                return []

            content_pattern = r'</b></a><br>\s*<table>.*?<td valign="top"><span class="normal">([\s\S]*?<a href="[^"]+"><span class="tiny"><b>Click here to purchase\.</b></span></a>)'
            contents = re.findall(content_pattern, self.html_content, re.IGNORECASE | re.DOTALL)
            return contents
    
    def to_json(self):
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

        return json_items
    
if __name__ == '__main__':
    
    # Overstock.com
    jewelry_01_file = '../input-extraction/WebPages/overstock.com/jewelry01.html'
    jewelry_02_file = '../input-extraction/WebPages/overstock.com/jewelry02.html'

    # Rtvslo.si (not supported yet)
    audi_file = '../input-extraction/WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
    volvo_file = '../input-extraction/WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljsĚŚe v razredu - RTVSLO.si.html'

    extractor = RegularExpressionExtractor(jewelry_01_file)

    json_data = extractor.to_json()
    print(json.dumps(json_data, indent=4))