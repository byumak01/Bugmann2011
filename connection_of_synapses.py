# The function which is used for making synaptic connections is defined here
# Also the function which sets initial values for synapse objects is defined here.

import receptive_field as rf


def set_initial_variables(synapse_objects, initial_weights, probability):
    for synapse_obj in synapse_objects:
        synapse_obj.w = initial_weights
        synapse_obj.p = probability


def make_synaptic_connections(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count, rf_column_count,
                              synapse_objects):
    # by using get_indices_of_rf neurons function we get indexes of neurons which are in the receptive field of given
    # post-synaptic neuron.
    pre_synaptic_indices = rf.get_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count,
                                                        rf_column_count)

    for idx, synapse_obj in enumerate(synapse_objects):
        # In the last index of synapse_objects array connection between last hidden layer and response layer is defined.
        # Normally a neuron takes its receptive field from previous layers. That means a neuron in layer N represents
        # multiple neurons from layer N-1.
        # But between last hidden layer and response layer the situation is different. One neuron in last hidden layer
        # represents multiple neurons in response layer.
        # This if condition defines the case between last hidden layer and response layer.
        if idx == len(synapse_objects) - 1:
            synapse_obj.connect(j=pre_synaptic_indices, i=post_neuron_idx)
        else:
            # else condition makes connection for the rest of the synapse objects.
            synapse_obj.connect(i=pre_synaptic_indices, j=post_neuron_idx)

