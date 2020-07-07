from typing import Dict, List
from src.config import Config
from src.parser.parser import Parser


"""
Unigram Parser
* parse 'unigram.txt'
"""
class UnigramParser(Parser):
    @classmethod
    def parse(cls, filename: str = Config.UnigramPath) -> Dict[str, float]:
        parsed_dict = {}
        with open(filename, 'r') as f:
            # Remove newline(\n) by map
            lines: List[str] = list(map(lambda s: (s[:-1] if s[-1] == '\n' else s).strip(), f.readlines()))
            for line in lines:
                parsed_line = cls._split(line)
                assert len(parsed_line) == 2
                [name, value_str] = parsed_line
                parsed_dict[name] = float(value_str)
        return parsed_dict
