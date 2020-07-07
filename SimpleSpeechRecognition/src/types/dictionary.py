from typing import List, Dict


"""
DictionaryItem
* Item for one word
* name, unigram, bigram(to other words), phone list organizing it
"""
class DictionaryItem:
    def __init__(self, name: str, unigram: float, bigram: List[float], phone_list: List[str]):
        self.name = name
        self.unigram = unigram
        self.bigram = bigram
        self.phone_list = phone_list


"""
Dictionary
* word info dictionary by word index (not its name, because of duplicate word)
"""
class Dictionary:
    Silence = '<s>'
    def __init__(self,
                 word_list: List[str],
                 phone_list_list: List[List[str]],
                 uni_dict: Dict[str, float],
                 bi_dict: Dict[str, Dict[str, float]]):

        # change name gram to index gram (dict to list) - because of same word
        same_word_weight_list = [1 / word_list.count(name) for name in word_list]       # weight: uniform distribution
        uni_list = [uni_dict[name] * same_word_weight_list[index] for index, name in enumerate(word_list)]
        bi_list = [[
            bi_dict[name_from][name_to] * same_word_weight_list[index_to]
            if bi_dict[name_from].get(name_to) is not None
            else 0
            for index_to, name_to in enumerate(word_list)
        ] for index_from, name_from in enumerate(word_list)]

        # create word info(name, unigram, bigram, phoneList) list
        self.__word_info_list: List[DictionaryItem] = []
        for index, name in enumerate(word_list):
            item = DictionaryItem(name, uni_list[index], bi_list[index], phone_list_list[index])
            self.__word_info_list.append(item)

    def count(self) -> int:
        return len(self.__word_info_list)

    def wordName(self, index: int) -> str:
        return self.wordInfo(index).name

    def wordNameList(self) -> List[str]:
        return [info.name for info in self.__word_info_list]

    def wordInfo(self, index: int) -> DictionaryItem:
        return self.__word_info_list[index]

    def wordInfoList(self) -> List[DictionaryItem]:
        return self.__word_info_list

    def unigramList(self) -> List[float]:
        return [info.unigram for info in self.__word_info_list]

    def bigramList(self, index: int) -> List[float]:
        return self.wordInfo(index).bigram
