from typing import List
from src.types.pdf import PDF


"""
STATE
* state model class (parsed from hmmParser)
"""
class STATE:
    def __init__(self, pdfList: List[PDF]):
        self.pdf_list = pdfList
