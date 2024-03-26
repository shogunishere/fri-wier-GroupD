from enum import Enum

class PageType(Enum):
    HTML = 1
    BINARY = 2
    DUPLICATE = 3
    FRONTIER = 4

class BinaryType(Enum):
    DOC = 1
    DOCX = 2
    PDF = 3
    PPT = 4
    PPTX = 5