import numpy as np
from .jit_compiled_functions import feeding_release_fed_ticks
from numba.typed import List as NumbaList


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
                    
                host.df_attributes['tick_stage_' + str(stage) + '_timestep_0'] = 0
                host.df_attributes['tick_stage_' + str(stage) + '_timestep_0_inf'] = 0
                    
    def _sampy_debug_attach_to_host_to_feed(self, list_host_stage_prob):
        pass

    def attach_to_host_to_feed(self, rng_seed, list_stage_hosts_prob, position_attribute='position'):
        """
        Attach ticks to their hosts, using the followin methodology:
            1) the user gives to each pair of host and stage a probability.
            2) this probability is the probability for a tick in this stage to attach to an host of
               the corresponding population.
            3) for each given cell, the number of tick that attach to a given agent is obtained using
               a multinomial distribution using the probabilities given by the user. 

        IMPORTANT: this method used numba random number generation, which we try to avoid as much
                   as possible. However, in this case it would require a lot of work, and probably
                   the development of a function converting uniform number into a multinomial
                   distrib. This will be changed in the future.

        :param rng_seed: seed used inside the numba compiled function
        :param list_stage_hosts_prob: list of lists of the form [stage, (host_string_1, p1), ..., 
                                                                 (host_string_k, pk)].
        """
        for item in list_stage_hosts_prob:
            stage = item[0]

            # we first create the DataStructures that will be needed by the Numba Compiled function below
            list_counts = NumbaList()
            list_positions_argsort = NumbaList() # this is needed for technical reasons in the Numba func,
                                                 # it is the argsort of positions of each host
            list_proba = []
            list_col_tick = NumbaList()
            list_col_tick_inf = NumbaList()

            # now we fill those data structure
            for host, proba in item[1:]:
                list_counts.append(self.dict_hosts[host].count_pop_per_vertex(position_attribute=position_attribute))
                list_positions_argsort.append(np.argsort(self.dict_hosts[host].df_attributes[position_attribute]))
                list_proba.append(proba)
                list_col_tick.append(self.dict_hosts[host].df_attributes['tick_stage_' + str(stage) + '_timestep_0'])
                list_col_tick_inf.append(self.dict_hosts[host].df_attributes['tick_stage_' + str(stage) + '_timestep_0_inf'])
            arr_proba = np.array(list_proba)
            

                
