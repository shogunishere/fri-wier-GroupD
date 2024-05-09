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
		
class BigBangXPathExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()
        self.tree = html.fromstring(self.html_content)
     
    def extract_product_type(self):
        productType = self.tree.xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[1]/div[2]/a/text()")
        #print(productType[0])
        return productType
		
    def extract_product_name(self):
        productName = self.tree.xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[1]/h2/a/text()")
        #print(productName[0])
        return productName
	
    def extract_price(self):
        price = self.tree.xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[2]/div[1]/text()")
        #print(price[0])
        return price
		
    def extract_alternative_price(self):
        alternativePrice = self.tree.xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[2]/div[2]/p/strong/text()")
        #print(alternativePrice[0])
        return alternativePrice
		
    def extract_in_stock(self):
        inStock = self.tree.xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[3]/div[1]/span/text() | /html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[3]/div[1]/span/strong/text()")
        #print(inStock[0])
        return inStock

    def to_json(self, save=True):
        extracted_type = self.extract_product_type()
        extracted_name = self.extract_product_name()
        extracted_prices = self.extract_price()
        extracted_alternative_prices = self.extract_alternative_price()
        extracted_in_stock = self.extract_in_stock()
        
        json_items = []
        for type, name, price, alternative_price, in_stock in zip(extracted_type, extracted_name, extracted_prices, extracted_alternative_prices, extracted_in_stock):
            item = {
                "product_type": type,
                "product_name": name,
                "product_price": price,
                "product_alternative_price": alternative_price,
                "product_in_stock": in_stock            
            }
            json_items.append(item)

        if save:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)  
            json_filename = os.path.join(self.save_dir, 'extracted_data.json')
            with open(json_filename, 'w') as json_file:
                json.dump(json_items, json_file, indent=4)
        
        return json_items
		
class CraigsListXPathExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()
        self.tree = html.fromstring(self.html_content)
     
    def extract_product_name(self):
        productName = self.tree.xpath("/html/body/div[1]/main/div[1]/div[5]/ol/li/div/a/span/text()")
        #print(productName[1])
        return productName
	
    def extract_price(self):
        prices = []
        number_of_items = len(self.tree.xpath("/html/body/div[1]/main/div[1]/div[5]/ol/li[@class='cl-search-result cl-search-view-mode-gallery']"))-2
        #print("Number of items:", number_of_items)
        
        for i in range(1,number_of_items):
            price_element = self.tree.xpath("/html/body/div[1]/main/div[1]/div[5]/ol/li["+str(i)+"]/div/span/text()")
            if len(price_element) == 1:
               prices.append(price_element[0])
               #print("["+str(i)+"]: "+price_element[0])
            else:
               prices.append(None)
               #print("["+str(i)+"]: None")
        		
        #print(prices)
        return prices
		
    def extract_location(self):
        locations = []
        number_of_items = len(self.tree.xpath("/html/body/div[1]/main/div[1]/div[5]/ol/li[@class='cl-search-result cl-search-view-mode-gallery']"))-2
        for i in range(1,number_of_items):
            location_element = self.tree.xpath("/html/body/div[1]/main/div[1]/div[5]/ol/li["+str(i)+"]/div/div[2]/text()")
            if len(location_element) == 2:
                locations.append(location_element[1])
                #print("["+str(i)+"]: "+location_element[1])
            else:
               locations.append(None)
               #print("["+str(i)+"]: None")
        location = self.tree.xpath("/html/body/div[1]/main/div[1]/div[5]/ol/li/div/div[2]/text()")
        print(locations)
        return locations
		
    #def extract_post_date(self):
    #    postDate = self.tree.xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[3]/div[1]/span/text() | /html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[3]/div[1]/article/div[2]/div[3]/div[1]/span/strong/text()")
    #    #print(postDate[0])
    #    return postDate

    def to_json(self, save=True):
        extracted_name = self.extract_product_name()
        extracted_prices = self.extract_price()
        extracted_location = self.extract_location()
        #extracted_post_date = self.extract_post_date()
        
        json_items = []
        #for type, name, price, location, post_date in zip(extracted_name, extracted_prices, extracted_location, extracted_post_date):
        for name, price, location, in zip(extracted_name, extracted_prices, extracted_location):
            item = {
                "product_name": name,
                "product_price": price,
                "product_location": location,
                #"product_post_date": post_date           
            }
            json_items.append(item)

        if save:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)  
            json_filename = os.path.join(self.save_dir, 'extracted_data.json')
            with open(json_filename, 'w') as json_file:
                json.dump(json_items, json_file, indent=4)
        
        return json_items