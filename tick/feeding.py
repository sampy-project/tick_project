import numpy as np
from .jit_compiled_functions import feeding_release_fed_ticks


class FeedingSingleGraph:
    """
    This building-blocks provides tool to link the population of ticks to a single or several hosts, 
    on which they will feed. This building block assumes that the various hosts and the ticks share 
    the same graph.

    add new columns to the hosts df_population

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
        self.nb_timesteps_feeding = nb_timesteps_feeding

        for _, values in self.dict_hosts.items():
            host, list_stages = values
            for stage in list_stages:
                for i in range(self.nb_timesteps_feeding):
                    host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + str(i)] = 0
                    host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + str(i) + '_inf'] = 0

    def increment_feeding_stage(self, position_attribute='position'):
        """
        todo
        """
        for host, list_stages in self.dict_hosts.values():
            for stage in list_stages:
                feeding_release_fed_ticks(self.pop_per_vertex_fed, 
                                          host.df_attribute[position_attribute],
                                          host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + \
                                                              str(stage + 1)],
                                          stage)
                feeding_release_fed_ticks(self.pop_per_vertex_fed_inf, 
                                          host.df_attribute[position_attribute],
                                          host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + \
                                                              str(stage + 1) + '_inf'],
                                          stage)

                for i in range(self.nb_timesteps_feeding - 1):
                    index_sup = self.nb_timesteps_feeding - 1 - i

                    host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + str(index_sup)] = \
                        host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + str(index_sup - 1)]
                    host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + str(index_sup) + '_inf'] = \
                        host.df_attributes['tick_stage_' + str(stage) + '_timestep_' + str(index_sup - 1) + '_inf']
                    
    def attach_to_host_to_feed(self):
        """
        todo
        """
        pass
                
