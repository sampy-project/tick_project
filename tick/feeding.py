import numpy as np


class FeedingSingleGraph:
    """
    This building-blocks provides tool to link the population of ticks to a single or several hosts, 
    on which they will feed. This building block assumes that the various hosts and the ticks share 
    the same graph.

    add new columns to the hosts dataframe

    Mandatory kwargs:
        - dict_hosts: dictionnary whose keyes are hashable identifiers that the user chose to use
                      to identify the hosts (usually a string), and values are lists of the form
                      [population_object, [i1, i2, ..., ik]] where the ik are distinct integers
                      corresponding to stages of the ticks.
        - nb_timesteps_feeding: int, number of timesteps that the tick spend on the host. Assumed 
                                to be the same accross all hosts and tick stages.
    """
    def __init__(self, dict_hosts=None, nb_timesteps_feeding=None, **kwargs):
        if dict_hosts is None:
            raise ValueError("No 'dict_hosts' provided for tick's feeding behavior.")
        if nb_timesteps_feeding is None:
            raise ValueError("No 'nb_timesteps_feeding' provided for tick's feeding behavior.")

        self.dict_hosts = dict_hosts

        for name_host, values in self.dict_hosts.itmes():
            host, list_stages = values
            for stages in list_stages:
                for i in range(nb_timesteps_feeding):
                    host.df_attributes['tick_stage_' + str(stages) + '_timestep_' + str(i)] = 0
