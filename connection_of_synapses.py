# The function which is used for making synaptic connections is defined here
# Also the function which sets initial values for synapse objects is defined here.

import receptive_field as rf


def set_initial_variables(synapse_objects, initial_weights, probability):
    for synapse_obj in synapse_objects:
        synapse_obj.w = initial_weights
        synapse_obj.p = probability


def make_synaptic_connections(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count, rf_column_count,
                              synapse_objects, syn_connection_prob):
    # by using get_indices_of_rf neurons function we get indexes of neurons which are in the receptive field of given
    # post-synaptic neuron.
    pre_synaptic_indices = rf.get_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count,
                                                        rf_column_count)

    for idx, synapse_obj in enumerate(synapse_objects):
        synapse_obj.connect(i=pre_synaptic_indices, j=post_neuron_idx, p=syn_connection_prob)

