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


@nb.njit
def mortality_proportion_based_mortality_all_graph(array_proportion, array_pop, array_vertices):
    for i in range(array_pop.shape[0]):
        if array_vertices[i]:
            for j in range(array_pop.shape[1]):
                array_pop[i, j] -= np.floor(array_pop[i, j] * array_proportion[j])


@nb.njit
def feeding_release_fed_ticks(array_pop, array_pos, array_nb_tick_fed, stage):
    for i in range(array_nb_tick_fed.shape[0]):
        array_pop[array_pos[i], stage] += array_nb_tick_fed[i]


@nb.njit
def feeding_attach_to_host_to_feed(rng_seed, list_counts, arr_ticks, stage, arr_proba,
                                   list_pos_argsort, list_col_tick):
    np.random.seed(rng_seed)
    nb_host_pop = len(list_counts)
    arr_counter_host = np.full(nb_host_pop, 0, dtype=int) # used when 

    for pos in range(list_counts[0].shape[0]):

        nb_agents = 0
        for i in range(nb_host_pop):
            nb_agents += list_counts[i][pos]

        # this following section is, by itself, a good enough reason to recode a multinomial
        # generator given that it is just made to satisfy numpy.random.multinomial
        # construction. This will be done later.
        arr_prob_extended = np.full(nb_agents + 1, 0., dtype=float)
        tot_sum_prob_extended = 0.
        counter = 0
        for i in range(nb_host_pop):
            tot_sum_prob_extended =+ arr_proba[i] * list_counts[i][pos]
            for _ in range(list_counts[i][pos]):
                arr_prob_extended[counter] = arr_proba[i]
                counter += 1
        
        if tot_sum_prob_extended > 1.:
            arr_prob_extended /= tot_sum_prob_extended
        else:
            arr_prob_extended[-1] = 1. - tot_sum_prob_extended
        
        multinom_sample = np.random.multinomial(arr_ticks[pos, stage], arr_prob_extended)

        counter = 0
        for i in range(nb_host_pop):
            for j in range(list_counts[i][pos]):
                list_col_tick[i][list_pos_argsort[i][arr_counter_host[i]]] += multinom_sample[counter]
                arr_ticks[pos, stage] -= multinom_sample[counter]
                counter += 1
                arr_counter_host[i] += 1

