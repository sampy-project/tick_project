from .jit_compiled_functions import stage_transition_proportion_based_transition_from_matrix
import numpy as np


class ProportionBasedStageTransition:
    """
    Building block that provides simple "proportion-based" ways to modelize ticks' stage transitions.
    That is, the user provides a proportion for each pair (a, b) of stages such that there should be some ticks
    transitionning from stage a to stage b. The definition of a stage depends on the method used.

    Important: the methods provided here do not make assumptions on the various class of population
    """
    def __init__(self, **kwargs):
        pass

    def _sampy_debug_proportion_based_transitions(self, feeding_status, disease_status, dict_transitions):
        if feeding_status not in ['unfed', 'fed']:
            raise ValueError("feeding_status should either be 'fed' or 'unfed'.")
        if disease_status not in ['infected', 'susceptible']:
            raise ValueError("disease_status should either be 'infected' or 'susceptible'.")
        for key, val in dict_transitions.items():
            if not (0. <= val <= 1.):
                raise ValueError("Values in the dictionnary should be floats between 0 and 1.")
            start_phase, start_stage, end_phase, end_stage = key
            if start_phase not in ['egg', 'larva', 'nymph', 'adult']:
                raise ValueError("Keyes of the dict should be tuples of the form (start_phase," + 
                                 " start_stage, end_phase, end_stage), with phases being in" + 
                                 " [egg, larva, nymph, adult].")
            if (start_phase == 'egg') and not (0 <= start_stage < self.stages_as_tupple[0]):
                raise ValueError("The starting phase is invalid.")
            if (start_phase == 'larva') and not (0 <= start_stage < self.stages_as_tupple[1]):
                raise ValueError("The starting phase is invalid.")
            if (start_phase == 'nymph') and not (0 <= start_stage < self.stages_as_tupple[2]):
                raise ValueError("The starting phase is invalid.")
            if (start_phase == 'adult') and not (0 <= start_stage < self.stages_as_tupple[3]):
                raise ValueError("The starting phase is invalid.")

            if end_phase not in ['egg', 'larva', 'nymph', 'adult']:
                raise ValueError("Keyes of the dict should be tuples of the form (start_phase," + 
                                 " start_stage, end_phase, end_stage), with phases being in" + 
                                 " [egg, larva, nymph, adult].")
            if (end_phase == 'egg') and not (0 <= end_stage < self.stages_as_tupple[0]):
                raise ValueError("The ending phase is invalid.")
            if (end_phase == 'larva') and not (0 <= end_stage < self.stages_as_tupple[1]):
                raise ValueError("The ending phase is invalid.")
            if (end_phase == 'nymph') and not (0 <= end_stage < self.stages_as_tupple[2]):
                raise ValueError("The ending phase is invalid.")
            if (end_phase == 'adult') and not (0 <= end_stage < self.stages_as_tupple[3]):
                raise ValueError("The ending phase is invalid.")
            

    def proportion_based_transitions(self, feeding_status, disease_status, dict_transitions):
        """
        Performs the transitions encoded in the dictionary 'dict_transitions'. Its keyes are tuples of the form
        (start_phase, start_stage, end_phase, end_stage), where start_phase and end_phase are string in the list
        ['egg', 'larva', 'nymph', 'adult'] and start_stage and end_stage are integers giving a valid stage
        for each corresponding phase. The values are non-neg floats giving the proportion of the population that 
        transitions.

        IMPORTANT: There cannot be any "loop" in the transitions.

        :param feeding_status: string, either 'fed' or 'unfed'.
        :param disease_status: string, either 'infected' of 'susceptible'.
        :param matrix_transitions: 2D array of floats. matrix_transitions[i, j] is the proportion of ticks that should
                                   go from status i to status j. Note that the method will be more efficient if there
                                   are only transitions such that j > i.
        """
        matrix_transitions = np.full((self.pop_per_vertex_fed.shape[1],
                                      self.pop_per_vertex_fed.shape[1]), 0.)
        for key, val in dict_transitions.items():
            start_phase, start_stage, end_phase, end_stage = key

            index_start_stage = getattr(self, 'indexes_' + start_phase + '_stage')[start_stage]
            index_end_stage = getattr(self, 'indexes_' + end_phase + '_stage')[end_stage]

            matrix_transitions[index_start_stage, index_end_stage] = val

        self.proportion_based_transition_from_matrix(feeding_status, disease_status, matrix_transitions)

    def _sampy_debug_proportion_based_transition_from_matrix(self, feeding_status, disease_status, matrix_transitions):
        if feeding_status not in ['unfed', 'fed']:
            raise ValueError("feeding_status should either be 'fed' or 'unfed'.")
        if disease_status not in ['infected', 'susceptible']:
            raise ValueError("disease_status should either be 'infected' or 'susceptible'.")
        if len(matrix_transitions.shape) != 2:
            raise ValueError("The transition matrix has wrong shape.")
        if matrix_transitions.shape[0] != matrix_transitions.shape[1]:
            raise ValueError("The transition matrix should be square.")
        if (matrix_transitions < 0.).any() or (matrix_transitions > 1.).any():
            raise ValueError("The transition matrix has values that are not between 0 and 1.")
        
    def proportion_based_transition_from_matrix(self, feeding_status, disease_status, matrix_transitions):
        """
        Performs the transitions encoded in the matrix 'matrix_transitions'. This matrix is a 2D array of 
        non-negative floats, such that matrix_transitions[i, j] is the proportion of the population
        that will transition from state i to state j. 

        IMPORTANT: There cannot be any "loop" in the transitions. That is, there cannot be a sequence of
                   indexes i_0, ..., i_k such that (i_0, i_1), ..., (i_{k-1}, i_k), (i_k, i_0) all have
                   positive values in the matrix.

        :param feeding_status: string, either 'fed' or 'unfed'.
        :param disease_status: string, either 'infected' of 'susceptible'.
        :param matrix_transitions: 2D array of floats. matrix_transitions[i, j] is the proportion of ticks that should
                                   go from status i to status j. Note that the method will be more efficient if there
                                   are only transitions such that j > i.
        """
        if feeding_status == 'fed' and disease_status == 'susceptible':
            stage_transition_proportion_based_transition_from_matrix(matrix_transitions, 
                                                                     self.pop_per_vertex_fed)
        elif feeding_status == 'unfed' and disease_status == 'susceptible':
            stage_transition_proportion_based_transition_from_matrix(matrix_transitions, 
                                                                     self.pop_per_vertex_unfed)
        elif feeding_status == 'fed' and disease_status == 'infected':
            stage_transition_proportion_based_transition_from_matrix(matrix_transitions, 
                                                                     self.pop_per_vertex_fed_inf)
        elif feeding_status == 'unfed' and disease_status == 'infected':
            stage_transition_proportion_based_transition_from_matrix(matrix_transitions, 
                                                                     self.pop_per_vertex_unfed_inf)
        else:
            raise ValueError("Not valid choice of feeding status and disease status.")
        
