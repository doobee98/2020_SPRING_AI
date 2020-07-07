from typing import Dict, List
import numpy as np
from src.config import Config
from src.parser.parser import Parser
from src.types.pdf import PDF
from src.types.state import STATE
from src.types.hmm import HMM


"""
HMM Parser
* parse 'hmm.txt'
"""
class HMMParser(Parser):
    # define delimiter string
    Name = "~h"
    BeginHMM = "<BEGINHMM>"
    NumStates = "<NUMSTATES>"
    State = "<STATE>"
    NumMixes = "<NUMMIXES>"
    Mixture = "<MIXTURE>"
    Mean = "<MEAN>"
    Variance = "<VARIANCE>"
    Transp = "<TRANSP>"
    EndHMM = "<ENDHMM>"

    @classmethod
    def parse(cls, filename: str = Config.HMMPath) -> Dict[str, HMM]:
        DummyStateNum = 2
        hmm_dict: Dict[str, HMM] = {}

        with open(filename, 'r') as f:
            lines: List[str] = list(map(lambda s: (s[:-1] if s[-1] == '\n' else s).strip(), f.readlines()))  # Remove newline(\n) by map

            idx = 0
            while idx < len(lines):
                # initialize variables
                name = ""
                num_state = 0
                num_mixture = 0
                num_transp = 0
                tp = np.array([])       # []?
                state_list: List[STATE] = []

                # Parse Name: ~h "{name}"
                parsed_line = cls._split(lines[idx])
                cls.__assertParsedLine(parsed_line, cls.Name)
                name = parsed_line[1][1:-1]
                hmm_dict[name] = {}
                idx += 1

                # Parse BEGINHMM
                cls.__assertParsedLine(cls._split(lines[idx]), cls.BeginHMM)
                idx += 1

                # Parse NUMSTATES
                parsed_line = cls._split(lines[idx])
                cls.__assertParsedLine(parsed_line, cls.NumStates)
                num_state = int(parsed_line[1]) - DummyStateNum
                idx += 1

                # Parse State
                for i in range(num_state):
                    pdf_list: List[PDF] = []

                    # Parse STATE
                    cls.__assertParsedLine(cls._split(lines[idx]), cls.State)
                    idx += 1

                    # Parse NUMMIXES
                    parsed_line = cls._split(lines[idx])
                    cls.__assertParsedLine(parsed_line, cls.NumMixes)
                    num_mixture = int(parsed_line[1])
                    idx += 1

                    # Parse PDF
                    for i in range(num_mixture):
                        size_vec = 0
                        weight = 0.0
                        mean_vec = np.array([])     # []?
                        var_vec = np.array([])      # []?

                        # Parse MIXTURE
                        parsed_line = cls._split(lines[idx])
                        cls.__assertParsedLine(parsed_line, cls.Mixture)
                        weight = float(parsed_line[2])
                        idx += 1

                        # Parse MEAN
                        parsed_line = cls._split(lines[idx])
                        cls.__assertParsedLine(parsed_line, cls.Mean)
                        size_vec = int(parsed_line[1])
                        idx += 1

                        parsed_line = cls._split(lines[idx])
                        assert size_vec == len(parsed_line)     # check vector size
                        mean_vec = np.array(list(map(lambda value_str: float(value_str), parsed_line)))
                        idx += 1

                        # Parse VARIANCE
                        parsed_line = cls._split(lines[idx])
                        cls.__assertParsedLine(parsed_line, cls.Variance)
                        size_vec = int(parsed_line[1])
                        idx += 1

                        parsed_line = cls._split(lines[idx])
                        assert size_vec == len(parsed_line)     # check vector size
                        var_vec = np.array(list(map(lambda value_str: float(value_str), parsed_line)))
                        idx += 1

                        # Create Pdf Object
                        pdf_list.append(PDF(weight, mean_vec, var_vec))

                    # Create State Object
                    state_list.append(STATE(pdf_list))

                # Parse TRANSP
                parsed_line = cls._split(lines[idx])
                cls.__assertParsedLine(parsed_line, cls.Transp)
                num_transp = int(parsed_line[1])
                idx += 1

                # Create tp Matrix Object
                temp_matrix: List[List[float]] = []
                for i in range(num_transp):
                    parsed_line = cls._split(lines[idx])
                    assert num_transp == len(parsed_line)  # check vector size
                    temp_matrix.append(list(map(lambda value_str: float(value_str), parsed_line)))
                    idx += 1
                tp = np.array(temp_matrix)

                # Parse ENDHMM
                cls.__assertParsedLine(cls._split(lines[idx]), cls.EndHMM)
                idx += 1

                # Create Hmm Object
                hmm_dict[name] = HMM(name, tp, state_list)

        return hmm_dict

    @classmethod
    def __assertParsedLine(cls, parsed_line: List[str], line_type: str) -> None:
        # assert parsing delimiter
        assert parsed_line[0] == line_type


