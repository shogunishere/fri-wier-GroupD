from tokenizer import Tokenizer
from bs4 import Tag, NavigableString
from typing import List, Tuple

class RoadRunner():
    def __init__(self, pages_to_compare):
        self.pages: List[str] = [self._tokenize_html(page) for page in pages_to_compare]

    def _open_html(self, file_path):
        try:
            # Try opening with utf-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            # Fallback to iso-8859-1 if utf-8 fails
            with open(file_path, 'r', encoding='iso-8859-1') as file:
                html_content = file.read()
        return html_content


    def _tokenize_html(self, page) -> List[str]: 
        content = self._open_html(page)

        tokenizer = Tokenizer()
        tokenizer.feed(content)

        tokens = tokenizer.content

        return tokens
    

    def _tokenize_str(self, str) -> List[str]: 
        tokenizer = Tokenizer()
        
        str = f'<body>{str}</body>' # Tokenizer() tokenizes only body, so we 

        tokenizer.feed(str)

        tokens = tokenizer.content  

        tokens = tokens[1:-1] # drop body tags, dont need them  
    
        return tokens
    
    '''
    Performs search to find square regex
    '''
    def _find_square(self, square_start: int, square_length: int, page: List[str]) -> Tuple[bool, str]:
        square_regex = ""

        idx_backwards = square_start - square_length
        
        print(f'page: {page}')
        print(f'length: {square_length}')

        idx = square_start

        checks = 0

        while checks < square_length:
            
            print(f'page[idx]: {page[idx]}, idx: {idx}')
            
            print(f'page[idx_backwards]: {page[idx_backwards]}, idx_backwards: {idx_backwards}')

            if page[idx] == page[idx_backwards] and Tokenizer.is_tag(page[idx]): # equal tags
                square_regex += page[idx] 
            elif page[idx] == page[idx_backwards] and not Tokenizer.is_tag(page[idx]): # equal strings
                square_regex += page[idx]
            elif page[idx] != page[idx_backwards] and Tokenizer.is_tag(page[idx]) and Tokenizer.is_tag(page[idx_backwards]): # non-equal tags
                return (False, None)
            elif page[idx] != page[idx_backwards] and not Tokenizer.is_tag(page[idx]) and not Tokenizer.is_tag(page[idx_backwards]): # non-equal string
                square_regex += "#PCDATA"

            idx += 1
            idx_backwards += 1
            checks += 1

        return (True, square_regex)

    '''
    Searches if page has square from position start
    '''
    def _square_match(self, start: int, page: List[str]) -> Tuple[bool, str, int]:

        square = page[start]

        opening_tag = page[start]

        idx = start + 1 
        while idx < len(page):
            potential_close_tag = page[idx]

            if Tokenizer.tags_match(tag1=opening_tag, tag2=potential_close_tag):
                square += page[idx]  
                square_length = len(self._tokenize_str(square))
                print(f'square: {square}')
                print(f'square_length: {square_length}')

                return (True, square, square_length)
            
            square += page[idx]
        
            idx += 1
        
        return (False, None)
    
    def _optional_candidate_search(self, page, pointer):
        idx = pointer

        optional_candidate = page[pointer]

        # construct optional candidate
        while not Tokenizer.tags_match(page[idx], page[pointer]):
            idx += 1
            optional_candidate += page[idx]

        return optional_candidate

    def generate_wrapper(self):
        wrapper = self.pages[0]
        sample = self.pages[1]

        wrapper_pointer = 0
        sample_pointer = 0

        wrapper_ = ""

        skip_by = 1
        
        while wrapper_pointer < len(wrapper) and sample_pointer < len(sample):
            cur_wrapper_token: str = wrapper[wrapper_pointer]
            cur_sample_token: str = sample[sample_pointer]
            
            print(f'cur_wrapper_token: {cur_wrapper_token}')
            print(f'cur_sample_token: {cur_sample_token}')

            if cur_wrapper_token == cur_sample_token:
                # match
                wrapper_ += wrapper[wrapper_pointer]
            else:
                if Tokenizer.is_tag(wrapper[wrapper_pointer]) and Tokenizer.is_tag(sample[sample_pointer]):
                    # tag mismatch
                    print(f'Tag mismatch!  {wrapper[wrapper_pointer]} vs {sample[sample_pointer]}')

                    # search for possible iterator
                    
                    # terminal tag: last token of square has to be 1 before mismatch
                    iterator_terminal_tag = sample[wrapper_pointer-1]
                    print(f'iterator terminal tag: {iterator_terminal_tag}')

                    # one of the tokens has to be initial tag
                    if Tokenizer.tags_match(iterator_terminal_tag, cur_wrapper_token):
                        # option 1: higher cardinality is in wrapper
                        print(f'Square is on the wrapper!: {cur_wrapper_token} ... {iterator_terminal_tag}')

                        # square matching
                        (matched, square, length) = self._square_match(page=wrapper, start=wrapper_pointer)
                        
                        print(f"matched: {matched}")

                        if matched:
                            # find square regex
                            _, square_iterator_regex = self._find_square(square_length=length,square_start=wrapper_pointer, page=wrapper)
                            
                            print(f'square_iterator_regex: {square_iterator_regex}')

                            wrapper_ += f'({square_iterator_regex})+'
                        else:
                            # add fake square element as optional  
                            wrapper_ += f'?({square})'
                            raise Exception("Too complex!")


                    elif Tokenizer.tags_match(iterator_terminal_tag, cur_sample_token):
                        # option 2: higher cardinality is in sample
                        print(f'Square is on the sample!: {cur_sample_token} ... {iterator_terminal_tag}')
                        
                        # square matching
                        (matched, square, length) = self._square_match(page=sample, start=sample_pointer)
                        
                        print(f"matched: {matched}")

                        if matched:
                            # find square regex
                            square_iterator_regex = self._find_square(length=length,square_end=sample_pointer, page=sample)
                            
                            print('square_iterator_regex')
                            print(square_iterator_regex)

                            wrapper_ += f'?({square})'
                        else:
                            # add fake square element as optional  
                            wrapper_ += f'?({square})'
                            raise Exception("Too complex!")

                    # else:
                    #     # search failed, treat mismatch as an optional

                    #     wrapper_optional_candidate = self._optional_candidate_search(page=wrapper, pointer=wrapper_pointer)
                    #     wrapper_optional_candidate = self._tokenize_str(wrapper_optional_candidate)
                    #     print(f'wrapper_optional_candidate: {wrapper_optional_candidate}')


                    #     sample_optional_candidate = self._optional_candidate_search(page=sample, pointer=sample_pointer)
                    #     sample_optional_candidate = self._tokenize_str(sample_optional_candidate)
                    #     print(f'sample_optional_candidate: {sample_optional_candidate}')

                    #     if sample[sample_pointer + len(sample_optional_candidate)] == wrapper[wrapper_pointer]:
                    #         print(f'Optional in sample: {sample_optional_candidate}, After skipping optional tags match: {sample[sample_pointer + len(sample_optional_candidate)]} vs {wrapper[wrapper_pointer]}')
                    #         wrapper_ += f'({sample_optional_candidate})?'

                    #         # Skip optional
                    #         sample_pointer += len(sample_optional_candidate)
                    #     elif  wrapper[wrapper_pointer + len(wrapper_optional_candidate)] == sample[sample_pointer]:
                    #         print(f'Optional in wrapper: {wrapper_optional_candidate}, After skipping wrapper tags match: {wrapper[wrapper_pointer + len(wrapper_optional_candidate)]} vs {sample[sample_pointer]}')
                    #         wrapper_ += f'({wrapper_optional_candidate})?'

                    #         # Skip optional
                    #         wrapper_pointer += len(wrapper_optional_candidate)

                    #     continue

                elif Tokenizer.is_tag(wrapper[wrapper_pointer]) ^ Tokenizer.is_tag(sample[sample_pointer]):
                    # mixed mismatch
                    print(f'Mixed mismatch!  {wrapper[wrapper_pointer]} vs {sample[sample_pointer]}')
                else:
                    # string mistmatch 
                    print(f'String mismatch!  {wrapper[wrapper_pointer]} vs {sample[sample_pointer]}')
                    wrapper_ += '#PCDATA'

            print('Current wrapper: ')
            print(wrapper_)

            wrapper_pointer += 1
            sample_pointer += 1


        return wrapper_

if __name__ == '__main__':
    page1 = '../input-extraction/CustomPages/bigbang1_preprocessed.html'
    page2 = '../input-extraction/CustomPages/bigbang2_preprocessed.html'

    road_runner = RoadRunner(pages_to_compare=[page1, page2])
    wrapper = road_runner.generate_wrapper()
    
    print('Wrapper: ')
    print(wrapper)
