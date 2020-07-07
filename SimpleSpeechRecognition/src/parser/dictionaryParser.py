from typing import List, Tuple
from src.config import Config
from src.parser.parser import Parser


"""
Dictionary Parser
* parse 'dictionary.txt'
"""
class DictionaryParser(Parser):
    @classmethod
    def parse(cls, filename: str = Config.DictionaryPath) -> Tuple[List[str], List[List[str]]]:
        name_list = []
        phone_list_list = []
        with open(filename, 'r') as f:
            # Remove newline(\n) by map
            lines: List[str] = list(map(lambda s: (s[:-1] if s[-1] == '\n' else s).strip(), f.readlines()))
            for line in lines:
                parsed_line = cls._split(line)
                name_list.append(parsed_line[0])
                phone_list_list.append(parsed_line[1:])
        return name_list, phone_list_list
