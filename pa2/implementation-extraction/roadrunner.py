from tokenizer import Tokenizer
from bs4 import Tag, NavigableString

class RoadRunner():
    def __init__(self, pages_to_compare):
        self.pages = [self._tokenize_html(page) for page in pages_to_compare]

    def _open_html(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                return html_content
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")

    def _tokenize_html(self, page):
        content = self._open_html(page)

        print('content')
        print(content)

        tokenizer = Tokenizer()
        tokenizer.feed(content)

        tokens = tokenizer.content
        
        print('tokens')
        print(tokens)

        return tokens

    def generate_wrapper(self):
        page1 = self.pages[0]
        page2 = self.pages[1]

        pointer1 = 0
        pointer2 = 0

        wrapper = ""

        while pointer1 < len(page1) and pointer2 < len(page2):
            token1 = page1[pointer1]
            token2 = page2[pointer2]
            
            if token1 == token2:
                # match
                wrapper += page1[pointer1]
            else:
                if Tokenizer.is_tag(page1[pointer1]) and Tokenizer.is_tag(page2[pointer2]):
                    # tag mismatch
                    print(f'Tag mistmatch!  {page1[pointer1]} vs {page2[pointer2]}')

                    # search for possible iterator

                    # search failed, mismatch is an optional

                elif Tokenizer.is_tag(page1[pointer1]) ^ Tokenizer.is_tag(page2[pointer2]):
                    # mixed mismatch
                    print(f'Mixed mistmatch!  {page1[pointer1]} vs {page2[pointer2]}')
                else:
                    # string mistmatch 
                    print(f'String mistmatch!  {page1[pointer1]} vs {page2[pointer2]}')
                    wrapper += '#PCDATA'
            pointer1 += 1
            pointer2 += 1


        return wrapper

if __name__ == '__main__':
    books1 = '../input-extraction/CustomPages/books1.html'
    books2 = '../input-extraction/CustomPages/books2.html'

    road_runner = RoadRunner(pages_to_compare=[books1, books2])
    wrapper = road_runner.generate_wrapper()
    
    print('Wrapper: ')
    print(wrapper)
