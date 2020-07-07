from typing import List
import re


"""
Abstract Parser
"""
class Parser:
    @classmethod
    def parse(cls, filename: str):
        raise NotImplementedError

    @classmethod
    def _split(cls, string: str) -> List[str]:
        return re.split('[\t ]', string)
