# import matplotlib.pyplot as plt
import os
import re
import numpy as np
import random as rm

CURRENT_FOLDER = os.path.join('blog', 'static', 'blog', 'writing_with_BEC')
NPY_FOLDER = os.path.join(CURRENT_FOLDER, 'BECtff')
MATRICES_FOLDER = os.path.join(CURRENT_FOLDER, 'str_matrices')


def word2matrix(word):
    L = len(word)
    # kerning_filling = np.load('str_matrices/{}.npy'.format(ord(' ')))
    kerning_filling_path = os.path.join(MATRICES_FOLDER, f"{ord(' ')}.npy")
    kerning_filling = np.load(kerning_filling_path)
    matrices_list = [kerning_filling]
    for index in range(L):
        string = word[index]
        # matrix = np.load('str_matrices/{}.npy'.format(ord(string)))
        matrix_path = os.path.join(MATRICES_FOLDER, f"{ord(string)}.npy")
        matrix = np.load(matrix_path)
        matrices_list.append(matrix)
        matrices_list.append(kerning_filling)
    return np.hstack(matrices_list)


def word2od(word, randomize=True, alignement='center'):
    Lines = re.split('\n', word)
    matrices = []
    for Line in Lines:
        matrix = word2matrix(Line)
        OD = []
        for column in matrix.T:
            name = ''.join(column.astype(int).astype(str))
            # files_name = sorted(os.listdir('BECttf/' + name + '/'))
            name_path = os.path.join(NPY_FOLDER, name)
            files_name = sorted(os.listdir(name_path))
            rand_index = -1
            if randomize:
                rand_index = rm.randint(0, len(files_name)-1)
            # od = np.load('BECttf/{}/'.format(name) + files_name[rand_index]).T
            od_path = os.path.join(NPY_FOLDER, name,
                                   files_name[rand_index])
            od = np.load(od_path).T
            if name != 7 * '0':
                OD.append(od / (np.max(od)))
            else:
                OD.append(od / 1.5)
        matrices.append(np.hstack(OD))

    return np.vstack(justification(matrices, alignement=alignement))


def justification(arrays, alignement='center'):
    new_arrays = []
    max_w = np.max([x.shape[1] for x in arrays])
    for x in arrays:
        if x.shape[1] < max_w:
            new_x = np.zeros((arrays[0].shape[0], max_w))
            missing = max_w - x.shape[1]
            if alignement == 'center':
                left_fill = int(missing/2)
            elif alignement == 'left':
                left_fill = 0
            elif alignement == 'right':
                left_fill = max_w - x.shape[1]
            new_x[:, left_fill:left_fill+x.shape[1]] = x
            new_arrays.append(new_x)
        else:
            new_arrays.append(x)
    return new_arrays
