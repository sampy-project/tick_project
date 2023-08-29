import numpy as np


class ProportionBasedTickMortality:
    """
    Building block that provides simple "proportion-based" ways to modelize ticks' mortality.
    That is, the user provides for each stage a proportion of ticks that will be eliminated.
    """
    def __init__(self, **kwargs):
        pass

    def proportion_based_mortality_all_graph(self, array_population, array_proportion, geographic_condition=None):
        """

        :param array_population:
        :param array_proportion:
        :param geographic_condition: optional, 1D array of bool, default None.
        """
        pass

    def vertex_specific_proportion_based_mortality(self, array_population, array_proportion):
        """

        :param array_population:
        :param array_proportion:
        """
        pass
