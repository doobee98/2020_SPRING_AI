from typing import List
from nptyping import NDArray, Float64
import numpy as np
import time, os
from src.parser.testParser import TestParser
from src.config import Config
from src.utteranceHMM import UtteranceHMM
from src.types.dictionary import Dictionary


"""
optimized viterbi function (original viterbi: below page)
"""
def optimizedViterbi(utter: UtteranceHMM, evidence_list: List[NDArray[Float64]]):
    # HyperParameter: Language Model Weight
    language_model_weight = Config.LanguageModelWeight

    # preload optimizing
    log = np.log
    neginf, negmax = -np.inf, -np.finfo(float).max
    logmatrix, gaussianList = log(utter.matrix), utter.gaussianList

    # probability function
    plog_initial = lambda index: logmatrix[0][index]
    plog_trans = lambda index_from, index_to: logmatrix[index_from][index_to]
    def plog_evidence(index, vec):
        g_value = log(gaussianList[index].probability(vec))
        if g_value == neginf:
            return negmax
        else:
            return language_model_weight * g_value

    # define variables
    evidence_count = len(evidence_list)     # ROW
    state_count = utter.matrixSize() - 1    # COL, ignore start state 0
    m_p = [[neginf for col in range(state_count + 1)] for row in range(evidence_count)]    # probability
    m_q = [[0 for col in range(state_count + 1)] for row in range(evidence_count)]          # before index

    # force silence start and end
    sil_start_index, sil_end_index = 1, 3   # assumption

    # save initial state probability
    m_p[0][sil_start_index] = log(1)    # force silence start, ignore probability

    # loop for all evidence vector
    for k in range(1, evidence_count):
        kth_evidence = evidence_list[k]
        for j in range(1, state_count + 1):
            j_state_evidence_prob = plog_evidence(j, kth_evidence)
            for i in range(1, state_count + 1):
                max_prob, max_state = m_p[k][j], m_q[k][j]
                ith_prob, ij_trans_prob = m_p[k-1][i], plog_trans(i, j)
                if ith_prob != neginf and ij_trans_prob != neginf:
                    prob = ith_prob + ij_trans_prob + j_state_evidence_prob
                    if prob > max_prob:
                        max_prob = prob
                        max_state = i
                if max_state != 0:
                    m_p[k][j] = max_prob
                    m_q[k][j] = max_state

    # find best state sequence with silence end
    q = [0 for _ in range(evidence_count)]
    t = evidence_count - 1
    q[t] = sil_end_index           # silence end
    for k in range(t-1, -1, -1):
        q[k] = m_q[k][q[k+1]]
    del m_p, m_q

    # remove duplicated states and return
    for i in range(len(q)-1, 0, -1):
        if q[i] == q[i-1]:
            del q[i]
    return q[1:]        # ignore start state 0


"""
test function
"""
def test(utter: UtteranceHMM, word_dictionary: Dictionary):
    print('START Recognize!')
    start_time = time.time()

    # Read Test File Names
    file_list = []
    for (path, dir, files) in os.walk(Config.TestDirectoryPath):
        path = path.replace('\\', '/')
        if not dir:
            for filename in files:
                file_list.append(f'{path}/{filename}')
    total_file_num = len(file_list)

    # Initialize Output File
    output_filepath = f'{Config.Data}/recognized.txt'
    with open(output_filepath, 'w') as f:
        f.write('#!MLF!#\n')

    # Recognize each test file and Append Output File
    for index, file in enumerate(file_list):
        print(f'\t({index+1:>4}/{total_file_num}) [{int(time.time() -  start_time):>8}s] Start: {file}')
        testvec_list = TestParser.parse(file)
        v = optimizedViterbi(utter, testvec_list)

        # parse state list to word list
        result_list = []
        for state_index in v:
            try:
                word_name = word_dictionary.wordName(utter.startIndexList.index(state_index))
                if word_name != Dictionary.Silence:
                    result_list.append(word_name)
            except ValueError:
                pass

        # append output file
        recognized_file_name = file[file.index('tst'):].replace('txt', 'rec')
        with open(output_filepath, 'a') as f:
            f.write(f'"{recognized_file_name}"\n')
            for word_name in result_list:
                f.write(f'{word_name}\n')
            f.write('.\n')
        del testvec_list

    # finish!
    print(f'FINISH Recognize! - [{int(time.time() - start_time):>8}s]')




"""
additional: original viterbi function
"""
def viterbi(utter: UtteranceHMM, evidence_list: List[NDArray[Float64]]):
    # HyperParameter: Language Model Weight
    language_model_weight = Config.LanguageModelWeight

    # probability function
    plog_initial = lambda index: np.log(utter.matrix[0][index])
    plog_trans = lambda index_from, index_to: np.log(utter.matrix[index_from][index_to])

    def plog_evidence(index, vec):
        g_value = np.log(utter.gaussianList[index].probability(vec))
        if g_value == -np.inf:
            return -np.finfo(float).max
        else:
            return language_model_weight * g_value

    # define variables
    evidence_count = len(evidence_list)     # ROW
    state_count = utter.matrixSize() - 1    # COL, ignore start state 0
    m_p = [[-np.inf for col in range(state_count + 1)] for row in range(evidence_count)]    # probability
    m_q = [[0 for col in range(state_count + 1)] for row in range(evidence_count)]          # before index

    # force silence start and end
    sil_start_index, sil_end_index = 1, 3   # assumption

    # save initial state probability
    m_p[0][sil_start_index] = np.log(1)    # force silence start, ignore probability

    # loop for all evidence vector
    for k in range(1, evidence_count):
        current_evidence = evidence_list[k]
        for j in range(1, state_count + 1):
            for i in range(1, state_count + 1):
                if m_p[k-1][i] != -np.inf and plog_trans(i, j) != -np.inf:    # filter for speed
                    value = m_p[k-1][i] + plog_trans(i, j) + plog_evidence(j, current_evidence)
                    if value > m_p[k][j]:
                        m_p[k][j] = value
                        m_q[k][j] = i

    # find best state sequence with silence end
    q = [0 for _ in range(evidence_count)]
    t = evidence_count - 1
    q[t] = sil_end_index           # silence end
    for k in range(t-1, -1, -1):
        q[k] = m_q[k][q[k+1]]

    # remove duplicated states and return
    for i in range(len(q)-1, 0, -1):
        if q[i] == q[i-1]:
            del q[i]
    return q[1:]        # ignore start state 0
