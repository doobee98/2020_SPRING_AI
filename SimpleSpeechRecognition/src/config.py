
"""
Config
* Path Information Class
"""
class Config:
    Data = "./prevData"
    Src = "./src"

    DictionaryPath = f"{Data}/dictionary.txt"
    HMMPath = f"{Data}/hmm.txt"
    UnigramPath = f"{Data}/unigram.txt"
    BigramPath = f"{Data}/bigram.txt"
    VocabularyPath = f"{Data}/vocabulary.txt"
    TestDirectoryPath = f"{Data}/tst"

    LanguageModelWeight = 0.2
