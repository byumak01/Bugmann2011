import eqs_and_variables as ev
from brian2 import *


# check_if_delay_time is passed function checks if delay t is passed for any keys inside dictionary,
# these keys will be returned. Returned keys will later be used to call weight_update function.
def check_if_delay_time_passed(time, weight_delay):
    wd_keys = [key for key in weight_delay.keys() if key[0] <= time]
    return wd_keys


# call_weight_update function takes synapse object index from wd_key, also takes synapse indexes from dictionary,
# then will call weight_update function with proper arguments.
def call_weight_update(wd_keys, weight_delay, hidden_layers, synapse_objects):
    for key in wd_keys:
        obj_idx = key[1]
        w_index = weight_delay[key][0]
        weight_update(synapse_objects[obj_idx], hidden_layers[obj_idx], w_index)
        del weight_delay[key]


def take_weight_from_pool(synapse, ind_pre, ind_post, hidden_layer_obj):
    synapse.w[ind_pre, ind_post] += ev.fraction * hidden_layer_obj.w_pool[ind_post]


# update_pool_reserve function will update pool reserve.
def update_pool_reserve(hidden_layer_obj, ind_post):
    hidden_layer_obj.w_pool[ind_post] = (1 - ev.fraction) * hidden_layer_obj.w_pool[ind_post]


# take_weight_from_other_synapses function will execute rule 10.
def take_weight_from_other_synapses(synapse_obj, ind_pre, ind_post, updated_w):
    for i in ev.rf_array[ind_post]:
        if synapse_obj.w[i, ind_post] > updated_w and i != ind_pre:

            updater_w = synapse_obj.w[i, ind_post]  # Assigning to a dummy variable.

            # other synapse_obj releases some quantity.  Rule (11) at article
            synapse_obj.w[i, ind_post] -= (updater_w * (updater_w - updated_w)) / (8 + updater_w)

            # released quantity added to the synapse_obj that received a spike. Rule(12) at article.
            synapse_obj.w[ind_pre, ind_post] += (updater_w * (updater_w - updated_w)) / (8 + updater_w)



def weight_update(synapse_obj, hidden_layer_obj, w_index):
    for ind_pre, ind_post in zip(synapse_obj.i[w_index], synapse_obj.j[w_index]):
        #
        updated_w = synapse_obj.w[ind_pre, ind_post]

        # take_weight_from_other_synapses function will execute rule 10.
        take_weight_from_other_synapses(synapse_obj,ind_pre, ind_post, updated_w)

        # Taking synaptic weight from pool.
        take_weight_from_pool(synapse_obj, ind_pre, ind_post, hidden_layer_obj)

        # Updating pool reserve.
        update_pool_reserve(hidden_layer_obj, ind_post)
