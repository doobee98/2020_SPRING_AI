from src.parser.hmmParser import HMMParser
from src.parser.dictionaryParser import DictionaryParser
from src.parser.unigramParser import UnigramParser
from src.parser.bigramParser import BigramParser
from src.utteranceHMM import UtteranceHMM
from src.types.dictionary import Dictionary
from src.recognizer import test

"""

Speech Recognizer - 2doo  
* numpy, nptyping 설치 필요 (numpy=1.18.4, nptyping=1.1.0)

"""

# Parse Model Files
hmm_dict = HMMParser.parse()
uni_dict = UnigramParser.parse()
bi_dict = BigramParser.parse()
word_list, phone_list_list = DictionaryParser.parse()

# Initialize Word Dictionary
word_dictionary = Dictionary(word_list, phone_list_list, uni_dict, bi_dict)

# Create Word HMM and Organize Utterance HMM
utter = UtteranceHMM(hmm_dict, word_dictionary)

# Test Datum
test(utter, word_dictionary)
