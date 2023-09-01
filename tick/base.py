import numpy as np
from jit_compiled_functions import base_count_tick_per_vertex_with_stages


class BaseTickFourPhases:
    """
    Base class for creating a tick population. This class assumes 4 phases in the tick life cycle: egg, larva, nymph
    and adult.

    attributes created:
        - graph: a single graph object on which ticks live.
        - stages_as_tuples: tuple of integer of length 4, such that
                                - stages_as_tuple[0] is the number of stages in the egg phase of a tick life
                                - stages_as_tuple[1] is the number of stages in the larva phase of a tick life
                                - stages_as_tuple[2] is the number of stages in the nymph phase of a tick life
                                - stages_as_tuple[3] is the number of stages in the adult phase of a tick life
        - pop_per_vertex_unfed: 2D integer array of shape (nb_vertex, sum(stages_as_tuples) containing the number of
                                unfed tick in a given vertex at a given stage. That is, we have that
                                pop_per_vertex_unfed[i, j] is the number of unfed ticks at stage j occupying the vertex
                                of index i.
        - pop_per_vertex_unfed_inf: same but for infected ticks.
        - pop_per_vertex_fed: 2D integer array of shape (nb_vertex, sum(stages_as_tuples) containing the number of
                              fed tick in a given vertex at a given stage. That is, we have that
                              pop_per_vertex_fed[i, j] is the number of fed ticks at stage j occupying the vertex of
                              index i.
        - pop_per_vertex_fed_inf: same but for infected ticks.

    mandatory kwargs:
        - graph: a single graph object on which ticks live.
        - hosts: placeholder, left at None for the moment todo: decide good input for the hosts
        - stages_as_tuple: tuple of integer of length 4, such that
                                - stages_as_tuple[0] is the number of stages in the egg phase of a tick life
                                - stages_as_tuple[1] is the number of stages in the larva phase of a tick life
                                - stages_as_tuple[2] is the number of stages in the nymph phase of a tick life
                                - stages_as_tuple[3] is the number of stages in the adult phase of a tick life
    """
    def __init__(self, graph=None, stages_as_tupple=None):
        if graph is None:
            raise ValueError("A graph object should be passed to the tick constructor, using the kwarg 'graph'.")
        self.graph = graph

        if stages_as_tupple is None:
            raise ValueError("Number of stages for each phase of a tick life should be provided using the kwarg"
                             "'stages_as_tuple'.")

        if len(stages_as_tupple) != 4:
            raise ValueError("This class represents ticks with 4 main stages of development, egg, larva, nymph and"
                             "adult. You did not provide the correct number of stages.")

        if 0 in stages_as_tupple:
            raise ValueError("One of the stage has a stage with 0 slot, which may cause undefined behaviour and is"
                             "therefore not authorized. If the tick species you are studying lacks one stage, "
                             "please consider using another class.")

        self.stages_as_tupple = tuple(stages_as_tupple)

        # ticks have massive population compared to the animals they feed on. Therefore, the population is agregated at
        # the vertex level of the graph. This info is stored in 2D arrays of integers.
        self.pop_per_vertex_unfed = np.full((self.graph.number_vertices, sum(stages_as_tupple)), 0, dtype=int)
        self.pop_per_vertex_fed = np.full((self.graph.number_vertices, sum(stages_as_tupple)), 0, dtype=int)
        self.pop_per_vertex_unfed_inf = np.full((self.graph.number_vertices, sum(stages_as_tupple)), 0, dtype=int)
        self.pop_per_vertex_fed_inf = np.full((self.graph.number_vertices, sum(stages_as_tupple)), 0, dtype=int)

        # we save the indexes
        self.indexes_egg_stage = (0, self.stages_as_tupple[0] - 1)
        self.indexes_larva_stage = (self.indexes_egg_stage[1] + 1,
                                    self.indexes_egg_stage[1] + self.stages_as_tupple[1])
        self.indexes_nymph_stage = (self.indexes_larva_stage[1] + 1,
                                    self.indexes_larva_stage[1] + self.stages_as_tupple[2])
        self.indexes_adult_stage = (self.indexes_nymph_stage[1] + 1,
                                    self.indexes_nymph_stage[1] + self.stages_as_tupple[3])

    def count_tick_per_vertex(self, stage=None, feeding_status='all', disease_status='all'):
        """
        Count the number of ticks on each vertex. A stage can be specified by the user.

        :param stage: optional, string, default None. If not None, should be either 'egg', 'larva', 'nymph' or 'adult'.
                      This method will then count only the ticks in the specified stage.
        :param feeding_status: optional, string, default 'all'. If 'all', all ticks are counted. If 'fed' only fed 
                               ticks are counted. If 'unfed' only unfed ones. Any other value raises an error.
        :param disease_status: optional, string, default 'all'. If 'all', all ticks are counted. If 'infected' only 
                               infected ticks are counted. If 'susceptible' only non-infected ones. Any other value 
                               raises an error.

        :return: 1D array of integers. r_arr[i] is the number of tick in the vertex of index i.
        """
        if feeding_status == 'all':
            if disease_status == 'all':
                pop_per_vertex = self.pop_per_vertex_fed + self.pop_per_vertex_unfed + \
                                 self.pop_per_vertex_fed_inf + self.pop_per_vertex_unfed_inf
            if disease_status == 'infected':
                pop_per_vertex = self.pop_per_vertex_fed_inf + self.pop_per_vertex_unfed_inf
            if disease_status == 'susceptible':
                pop_per_vertex = self.pop_per_vertex_fed + self.pop_per_vertex_unfed
            else:
                raise ValueError("Disease status can only be chosen among ['all', 'infected', 'susceptible'].")

        elif feeding_status == 'fed':
            if disease_status == 'all':
                pop_per_vertex = self.pop_per_vertex_fed + self.pop_per_vertex_fed_inf
            if disease_status == 'infected':
                pop_per_vertex = self.pop_per_vertex_fed_inf
            if disease_status == 'susceptible':
                pop_per_vertex = self.pop_per_vertex_fed
            else:
                raise ValueError("Disease status can only be chosen among ['all', 'infected', 'susceptible'].")

        elif feeding_status == 'unfed':
            if disease_status == 'all':
                pop_per_vertex = self.pop_per_vertex_unfed + self.pop_per_vertex_unfed_inf
            if disease_status == 'infected':
                pop_per_vertex = self.pop_per_vertex_unfed_inf
            if disease_status == 'susceptible':
                pop_per_vertex = self.pop_per_vertex_unfed
            else:
                raise ValueError("Disease status can only be chosen among ['all', 'infected', 'susceptible'].")
            
        else:
            raise ValueError("Feeding status can only be chosen among ['all', 'fed', 'unfed'].")

        if stage is None:
            return pop_per_vertex.sum(axis=1)
        if stage == 'egg':
            return base_count_tick_per_vertex_with_stages(pop_per_vertex,
                                                          self.indexes_egg_stage[0], self.indexes_egg_stage[1])
        if stage == 'larva':
            return base_count_tick_per_vertex_with_stages(pop_per_vertex,
                                                          self.indexes_larva_stage[0], self.indexes_larva_stage[1])
        if stage == 'nymph':
            return base_count_tick_per_vertex_with_stages(pop_per_vertex,
                                                          self.indexes_nymph_stage[0], self.indexes_nymph_stage[1])
        if stage == 'adult':
            return base_count_tick_per_vertex_with_stages(pop_per_vertex,
                                                          self.indexes_adult_stage[0], self.indexes_adult_stage[1])
        raise ValueError("If used, the kwarg stage should be either 'egg', 'larva', 'nymph' or 'adult'.")
