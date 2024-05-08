'''
This is used for Roadrunnner algorithm
'''
from html.parser import HTMLParser

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