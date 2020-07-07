from typing import Dict, List
from src.parser.parser import Parser
from src.config import Config


"""
Bigram Parser
* parse 'bigram.txt'
"""
class BigramParser(Parser):
    @classmethod
    def parse(cls, filename: str = Config.BigramPath) -> Dict[str, Dict[str, float]]:
        parsed_dict = {}
        with open(filename, 'r') as f:
            # Remove newline(\n) by map
            lines: List[str] = list(map(lambda s: (s[:-1] if s[-1] == '\n' else s).strip(), f.readlines()))
            for line in lines:
                parsed_line = cls._split(line)
                assert len(parsed_line) == 3
                [name_from, name_to, value_str] = parsed_line
                if parsed_dict.get(name_from) is None:
                    parsed_dict[name_from] = {}
                parsed_dict[name_from][name_to] = float(value_str)
        return parsed_dict
