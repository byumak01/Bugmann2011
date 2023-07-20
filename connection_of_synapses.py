# The function which is used for making synaptic connections is defined here
# Also the function which sets initial values for synapse objects is defined here.

import receptive_field as rf
import eqs_and_variables as ev


def set_initial_variables(synapse_objects, initial_weights, transmission_p):
    for synapse_obj in synapse_objects:
        synapse_obj.w = initial_weights
        synapse_obj.transmission_p = transmission_p


def make_synaptic_connections(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count, rf_column_count,
                              synapse_objects, syn_connection_prob):
    # by using get_indices_of_rf neurons function we get indexes of neurons which are in the receptive field of given
    # post-synaptic neuron.
    pre_synaptic_indices = rf.get_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count,
                                                        rf_column_count)

    ev.rf_array.append(pre_synaptic_indices)

    for idx, synapse_obj in enumerate(synapse_objects):
        synapse_obj.connect(i=pre_synaptic_indices, j=post_neuron_idx, p=syn_connection_prob)



