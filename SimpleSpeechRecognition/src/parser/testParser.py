from typing import List
from nptyping import NDArray, Float64
import numpy as np
from src.config import Config
from src.parser.parser import Parser


"""
Test Parser
* parse tst/{sex}/{initial}/{text}.txt  (test files)
"""
class TestParser(Parser):
    @classmethod
    def parse(cls, filename: str) -> List[NDArray[Float64]]:
        test_list = []
        with open(filename, 'r') as f:
            lines: List[str] = list(map(lambda s: (s[:-1] if s[-1] == '\n' else s).strip(), f.readlines()))  # Remove newline(\n) by map
            num_line, vec_lines = lines[0], lines[1:]
            [vec_count, dim_count] = list(map(lambda value_str: int(value_str), cls._split(num_line)))
            
            assert vec_count == len(vec_lines)
            for vec_line in vec_lines:
                parsed_line = cls._split(vec_line)
                assert dim_count == len(parsed_line)
                x_vec = np.array(list(map(lambda value_str: float(value_str), parsed_line)))
                test_list.append(x_vec)
        return test_list

    @classmethod
    def createFileName(cls, sex: str, initial: str, text: str) -> str:
        return f'{Config.TestDirectoryPath}/{sex}/{initial}/{text}.txt'

    @classmethod
    def _split(cls, string: str) -> List[str]:
        # in test files, it has double blank - '  ' - and it cannot be parsed by re.split
        return string.split()
