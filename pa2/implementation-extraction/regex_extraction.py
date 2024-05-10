import os
import re
import json
from html_reader import HTMLReader
from collections import OrderedDict


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
        # print(extracted_savings)
        extracted_contents = self.extract_content()

        json_items = []
        for title, price, list_price, saving, content in zip(extracted_titles, extracted_prices, extracted_list_prices,
                                                             extracted_savings, extracted_contents):
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
        return publish_times[0]

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


class BigBangRegularExpressionExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()

    def extract_product_type(self):
        pattern = r'<div .*?class="cp-category".*?>([^<]+)<\/a><\/div>'
        productType = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(productType[0])
        # print("================")
        return productType

    def extract_product_name(self):
        pattern = r'<h2 .*?class="cp-title".*?>([^<]+)<\/a><\/h2>'
        productName = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(productName[0])
        # print("================")
        return productName

    def extract_price(self):
        pattern = r'<div .*?class="cp-current-price".*?>([^<]+)<\/div>'
        price = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(price[0])
        # print("================")
        return price

    def extract_alternative_price(self):
        pattern = r'ali od <strong>(\d+,\d{2} €)'
        alternativePrice = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(alternativePrice[0])
        # print("================")
        return alternativePrice

    def extract_in_stock(self):
        # pattern = r'<div\s+[^>]*class="available-qty-btn"[^>]*>\s*<span[^>]*>(.*?)<\/span>'
        pattern = r'<div\s+[^>]*class="available-qty-btn"[^>]*>\s*<span[^>]*>(?:<strong>)?(.*?)(?:<\/strong>)?<\/span>'  # Eliminate <strong></strong>
        inStock = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(inStock)
        # print("================")
        return inStock

    def to_json(self, save=True):
        extracted_type = self.extract_product_type()
        extracted_name = self.extract_product_name()
        extracted_prices = self.extract_price()
        extracted_alternative_prices = self.extract_alternative_price()
        extracted_in_stock = self.extract_in_stock()

        json_items = []
        for type, name, price, alternative_price, in_stock in zip(extracted_type, extracted_name, extracted_prices,
                                                                  extracted_alternative_prices, extracted_in_stock):
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


class CraigsListRegularExpressionExtractor():
    def __init__(self, file_path, save_dir):
        self.file_path = file_path
        self.save_dir = save_dir
        self.html_reader = HTMLReader(file_path)
        self.html_content = self.html_reader.read_html_file()

    def extract_product_name(self):
        pattern = r'<a .*?class="cl-app-anchor text-only posting-title".*?>([^<]+)<\/span><\/a>'
        productName = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(productName[0])
        # print("================")
        # productName = list(OrderedDict.fromkeys(productName)) #Remove duplicate elements
        return productName

    def extract_price(self):

        # pattern = r'<li.*?title="Nintendo Switch Portable Gaming Console".*?><span class="priceinfo">(.*?)<\/span>'
        # pattern = r'<li.*?title="PS4 Slim (Playstation), Switch or Xbox One S Console".*?><span class="priceinfo">(.*?)<\/span>'
        # pattern = r'<li.*?title="PSVR2 \+ Globular Cluster Comfort Mod".*?><span class="priceinfo">(.*?)<\/span>'
        # pattern = r'<li.*?title="Empty boxes".*?><span class="priceinfo">(.*?)<\/span>'
        # price = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # print("================")
        # for i in range(0,len(price)):
        #    print("["+str(i)+"]: " + price[i])
        # print(price)
        # print("================")

        prices = []
        # Get all the products
        products = re.findall(r'<a .*?class="cl-app-anchor text-only posting-title".*?>([^<]+)<\/span><\/a>',
                              self.html_content, re.IGNORECASE | re.DOTALL)
        # products = list(OrderedDict.fromkeys(products)) #Remove duplicate elements
        for product in products:
            #    #print(product)
            price = re.findall(r'<li.*?title="' + re.escape(product) + '".*?><span class="priceinfo">(.*?)<\/span>',
                               self.html_content, re.IGNORECASE | re.DOTALL)
            if len(price) > 0:
                prices.append(price[0])
                # print(product + ' - ' + price[0])
            else:
                prices.append(None)
                # print(product + ' - ' + 'None')
        #    #print(product)
        return prices

    def extract_location(self):
        # pattern = r'<li.*?title="Nintendo Switch Portable Gaming Console".*?><div class="meta">(.*?)<\/div>'
        # pattern = r'<li.*?title="PS Vita".*?><div class="meta">(.*?)<\/div>'

        locations = []
        # Get all the products

        products = re.findall(r'<a .*?class="cl-app-anchor text-only posting-title".*?>([^<]+)<\/span><\/a>',
                              self.html_content, re.IGNORECASE | re.DOTALL)
        # products = list(OrderedDict.fromkeys(products)) #Remove duplicate elements
        for product in products:
            locationRAW = re.findall(r'<li.*?title="' + re.escape(product) + '".*?><div class="meta">(.*?)<\/div>',
                                     self.html_content, re.IGNORECASE | re.DOTALL)
            location = re.findall(r'<\/span>(.*)', locationRAW[0], re.IGNORECASE | re.DOTALL)
            #print(location[0])
            if location[0]:
               locations.append(location[0])
                #print(product + ' - ' + location[0])
            else:
                locations.append(None)
                #print(product + ' - ' + 'None')
        
        # locationRAW = re.findall(pattern, self.html_content, re.IGNORECASE | re.DOTALL)
        # location = re.findall(r'<\/span>(.*)', locationRAW[0], re.IGNORECASE | re.DOTALL)
        # print("================")
        # print(locationRAW[0])
        # print(location)
        # print("================")
        return locations


    def to_json(self, save=True):
        extracted_name = self.extract_product_name()
        extracted_prices = self.extract_price()
        extracted_location = self.extract_location()
    
        json_items = []
        for name, price, location in zip(extracted_name, extracted_prices, extracted_location):
            item = {
                "product_name": name,
                "product_price": price,
                "product_location": location
            }
            json_items.append(item)
    
        if save:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
            json_filename = os.path.join(self.save_dir, 'extracted_data.json')
            with open(json_filename, 'w') as json_file:
                json.dump(json_items, json_file, indent=4)
    
        return json_items