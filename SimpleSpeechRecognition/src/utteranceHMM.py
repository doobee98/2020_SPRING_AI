from typing import Dict, List, Tuple
from nptyping import NDArray, Float64
import numpy as np
from src.types.dictionary import DictionaryItem, Dictionary
from src.types.hmm import HMM
from src.gaussian import SingleGaussian, MultiGaussian


"""
UtteranceHMM
* composition matrix of word HMMs
"""
class UtteranceHMM:
    def __init__(self, hmmDict: Dict[str, HMM], wordDictionary: Dictionary):
        # initialize variables
        Dummy = 2
        total_size = Dummy - 1
        for wordItem in wordDictionary.wordInfoList():
            for phone in wordItem.phone_list:
                total_size += len(hmmDict[phone].states)
        exit_vector_list: List[NDArray[Float64]] = []

        # initialize instance variables
        self.__matrix_size = 1                              # Entry Dummy State
        self.matrix: NDArray[Float64] = np.zeros((total_size, total_size))
        self.gaussianList: List[MultiGaussian] = [None]     # Entry Dummy State
        self.startIndexList: List[int] = [None for _ in range(wordDictionary.count())]

        # register word HMM
        for index, wordItem in enumerate(wordDictionary.wordInfoList()):
            gaussian_list, word_matrix = UtteranceHMM.wordHMM(hmmDict, wordItem)

            # initialize
            w_size, _ = word_matrix.shape
            w_inner_size = w_size - Dummy

            # check predicates
            assert w_size == _
            assert word_matrix[0][1] == 1.0
            assert word_matrix[0][-1] == 0.0

            # register inner matrix
            new_inner_start = self.__matrix_size
            new_inner_end = new_inner_start + w_inner_size
            new_inner_mat = word_matrix[1:1+w_inner_size, 1:1+w_inner_size]
            self.matrix[new_inner_start:new_inner_end, new_inner_start:new_inner_end] = new_inner_mat

            # save exit vector
            exit_vector_list.append(word_matrix[1:1+w_inner_size, [-1]])

            # update
            self.__matrix_size += w_inner_size
            self.gaussianList += gaussian_list
            self.startIndexList[index] = new_inner_start

        # entry unigram
        unigram = wordDictionary.unigramList()
        for word_index, start_index in enumerate(self.startIndexList):
            self.matrix[0][start_index] = unigram[word_index]

        # exit (unigram or bigram)
        for exit_word_index, exit_start in enumerate(self.startIndexList):
            gram = wordDictionary.unigramList()
            # gram = wordDictionary.bigramList(exit_word_index)
            exit_vector = exit_vector_list[exit_word_index]
            (exit_vector_size, c) = exit_vector.shape
            assert c == 1

            # distiribute exit vector to each word entry state
            for next_word_index, next_start in enumerate(self.startIndexList):
                value = gram[next_word_index]
                self.matrix[exit_start:exit_start+exit_vector_size, [next_start]] += value * exit_vector

    def matrixSize(self) -> int:
        return self.__matrix_size

    @classmethod
    def wordHMM(cls, hmmDict: Dict[str, HMM], dictItem: DictionaryItem) -> Tuple[List[MultiGaussian], NDArray[Float64]]:
        # organize a word HMM(state pdf list and word matrix) with parsed hmmDict
        Dummy = 2

        total_size = Dummy + sum([len(hmmDict[phone].states) for phone in dictItem.phone_list])
        cur_matrix: NDArray[Float64] = np.zeros((total_size, total_size))
        cur_size = 0
        state_mgd_list: List[MultiGaussian] = []

        # append word HMM with phone states and phone tp
        for phone_iter in dictItem.phone_list:
            phone_hmm = hmmDict[phone_iter]
            new_matrix = phone_hmm.tp
            state_mgd_list += [MultiGaussian([pdf.weight for pdf in state.pdf_list],
                                             [SingleGaussian(pdf.median, pdf.variance) for pdf in state.pdf_list])
                               for state in phone_hmm.states]

            (new_size, _) = new_matrix.shape
            assert new_size == _

            if cur_size == 0:
                cur_matrix[:new_size, :new_size] = new_matrix
                cur_size = new_size
            else:
                # index naming
                cur_inner_start, cur_inner_size = 1, cur_size - Dummy
                cur_inner_end = cur_inner_start + cur_inner_size
                new_inner_start, new_inner_size = cur_size - 1, new_size - Dummy
                new_inner_end = new_inner_start + new_inner_size

                # set inter (in and out) matrix (right top)
                cur_out = cur_matrix[cur_inner_start-1:cur_inner_end, [new_inner_start]]
                new_in = new_matrix[0, 1:]
                inter_matrix = cur_out * new_in         # numpy broadcasting
                cur_matrix[cur_inner_start-1:cur_inner_end, new_inner_start:new_inner_end+1] = inter_matrix

                # set next inner matrix (right down)
                cur_matrix[new_inner_start:new_inner_end, new_inner_start:new_inner_end+1] = new_matrix[1:-1, 1:]

                # next cur_size
                cur_size += new_size - Dummy

        return (state_mgd_list, cur_matrix)
