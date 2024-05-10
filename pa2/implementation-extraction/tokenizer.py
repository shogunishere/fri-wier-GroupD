'''
This is used for Roadrunnner algorithm
'''
from html.parser import HTMLParser
from typing import List

class Tokenizer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.content = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.capture = True 
        if self.capture:
            self.content.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if self.capture:
            self.content.append(f"</{tag}>")
        if tag == "body":
            self.capture = False  
    
    def handle_data(self, data):
        if self.capture:
            trimmed_data = data.strip()
            if trimmed_data:  
                self.content.append(trimmed_data)

    @staticmethod
    def is_tag(token):
            return token.startswith('<') and token.endswith('>')
    
    @staticmethod
    def get_tag_name(token):
        if Tokenizer.is_tag(token):
            return token.strip('<>/ ').split()[0]  
        return None

    @staticmethod
    def tags_match(tag1, tag2):
        tag_name1 = Tokenizer.get_tag_name(tag1)
        tag_name2 = Tokenizer.get_tag_name(tag2)
        is_closing_pair = (tag1.startswith('</') and tag2.startswith('<') and not tag2.startswith('</')) or \
                          (tag2.startswith('</') and tag1.startswith('<') and not tag1.startswith('</'))
        return tag_name1 == tag_name2 and is_closing_pair
    

    @staticmethod
    def generate_closing_tag(opening_tag):
        if not opening_tag.startswith('<') or '>' not in opening_tag:
            raise ValueError("Invalid opening tag format")

        tag_name = opening_tag.strip('<>').split()[0]  
        return f"</{tag_name}>"

