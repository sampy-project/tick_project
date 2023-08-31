import numpy as np
from jit_compiled_functions import mortality_proportion_based_mortality_all_graph


class ProportionBasedTickMortality:
    """
    Building block that provides simple "proportion-based" ways to modelize ticks' mortality.
    That is, the user provides for each stage a proportion of ticks that will be eliminated.
    """
    def __init__(self, **kwargs):
        pass

    def proportion_based_mortality_all_graph(self, feeding_status, disease_status, array_proportion, 
                                             geographic_condition=None):
        """
        Kill a user defined proportion of ticks per stage. This proportion is the same on every
        vertices of the graph. The user may include or exclude vertices using the kwarg
        'geographic_condition'.

        :param feeding_status: string, either 'fed' or 'unfed'.
        :param disease_status: string, either 'infected' of 'susceptible'. 
        :param array_proportion: 1D array of float, each between 0 and 1
        :param geographic_condition: optional, 1D array of bool, default None.
        """
        if geographic_condition is None:
            geographic_condition = np.full(self.pop_per_vertex_fed.shape[0], True)

        if feeding_status == 'fed' and disease_status == 'susceptible':
            mortality_proportion_based_mortality_all_graph(array_proportion, 
                                                           self.pop_per_vertex_fed,
                                                           geographic_condition)
        elif feeding_status == 'unfed' and disease_status == 'susceptible':
            mortality_proportion_based_mortality_all_graph(array_proportion, 
                                                           self.pop_per_vertex_unfed,
                                                           geographic_condition)
        elif feeding_status == 'fed' and disease_status == 'infected':
            mortality_proportion_based_mortality_all_graph(array_proportion, 
                                                           self.pop_per_vertex_fed_inf,
                                                           geographic_condition)
        elif feeding_status == 'unfed' and disease_status == 'infected':
            mortality_proportion_based_mortality_all_graph(array_proportion, 
                                                           self.pop_per_vertex_unfed_inf,
                                                           geographic_condition)
        else:
            raise ValueError("Not valid choice of feeding status and disease status.")

    def vertex_specific_proportion_based_mortality(self, feeding_status, disease_status, array_proportion):
        """
        Kill a user defined proportion of ticks per stage per vertex.

        :param feeding_status: string, either 'fed' or 'unfed'.
        :param disease_status: string, either 'infected' of 'susceptible'. 
        :param array_proportion: 2D array of float, each between 0 and 1.
        """
        if feeding_status == 'fed' and disease_status == 'susceptible':
            self.pop_per_vertex_fed -= np.floor(self.pop_per_vertex_fed * array_proportion)
        elif feeding_status == 'unfed' and disease_status == 'susceptible':
            self.pop_per_vertex_unfed -= np.floor(self.pop_per_vertex_unfed * array_proportion)
        elif feeding_status == 'fed' and disease_status == 'infected':
            self.pop_per_vertex_fed_inf -= np.floor(self.pop_per_vertex_fed_inf * array_proportion)
        elif feeding_status == 'unfed' and disease_status == 'infected':
            self.pop_per_vertex_unfed_inf -= np.floor(self.pop_per_vertex_unfed_inf * array_proportion)
