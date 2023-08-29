import numba as nb
import numpy as np


@nb.njit
def base_count_tick_per_vertex_with_stages(array_pop, index_start, index_end):
    """
    Simple nested loop counting the number of tick at a given stage.

    :param array_pop: 2d array of int
    :param index_start: index on axis 2 corresponding to beginning of the stage
    :param index_end: index on axis 2 corresponding to the end of the stage.

    :return: 1D array of int
    """
    rv = np.full((array_pop.shape[0],), 0, dtype=int)
    for i in range(array_pop.shape[0]):
        for j in range(index_start, index_end + 1):
            rv[i] += array_pop[j]
    return rv


@nb.njit
def stage_transition_proportion_based_transition_from_matrix(trans_matrix, 
                                                             population_array):
    set_output_transition = set()
    for _ in range(trans_matrix.shape[0]):
        for i in range(trans_matrix.shape[0]):
            curr_index = trans_matrix.shape[0] - i - 1

            # if this index has been seen already, we skip.
            if curr_index in set_output_transition:
                break

            # now we check if this index is 'valid'. That is there is no population supposed to 
            # "leave" curr_index status
            is_valid = True
            for j in range(trans_matrix.shape[0]):
                if trans_matrix[curr_index, j] > 0. and (j not in set_output_transition):
                    is_valid = False
                    break

            # if the index is valid, we make the transitions toward curr_index
            if is_valid:
                set_output_transition.add(curr_index)

                for k in range(trans_matrix.shape[0]):
                    if trans_matrix[k, curr_index] > 0.:
                        for u in range(population_array.shape[0]):
                            pop_moved = np.floor(population_array[u, k] * trans_matrix[k, curr_index])
                            population_array[u, k] -= pop_moved
                            population_array[u, curr_index] += pop_moved

                break
