from brian2 import *
import receptive_field as rf


# create_key_for_enabled_neurons function creates a key with given hidden_layer index.
# Later enabled neuron indices at that layer_idx will be added to value side of this key.
def create_key_for_enabled_neurons(hidden_layer_idx, enabled_neurons):
    enabled_neurons[hidden_layer_idx] = set()


# add_neuron_indices_to_enabled_neurons function will add given neuron indices for enabled neurons to the given place
# inside enabled_neurons dictionary
def add_neuron_indices_to_enabled_neurons(layer_idx, enabled_neurons, neuron_indices):
    for element in neuron_indices:
        enabled_neurons[layer_idx].add(element)


def set_enable_flags_for_rest(layer, post_neuron_indices, ng_row_count, ng_column_count, rf_row_count,
                              rf_column_count, layer_idx, enabled_neurons):
    # Creating a key for given layer_idx
    create_key_for_enabled_neurons(layer_idx, enabled_neurons)
    for post_neuron_idx in post_neuron_indices:
        pre_synaptic_indices = rf.get_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count,
                                                            rf_row_count, rf_column_count)

        add_neuron_indices_to_enabled_neurons(layer_idx, enabled_neurons, pre_synaptic_indices)

        for pre_syn_idx in pre_synaptic_indices:
            layer[layer_idx].flag[pre_syn_idx] = True

    layer_idx -= 1

    if layer_idx >= 0:
        set_enable_flags_for_rest(layer, enabled_neurons[layer_idx + 1], ng_row_count, ng_column_count,
                                  rf_row_count, rf_column_count, layer_idx, enabled_neurons)


# set_target_neuron_flag function will set the flag value of given neuron in last hidden layer_idx to true.
def set_target_neuron_flag(layers, enabled_neurons):
    # getting index of target neuron.
    target_neuron_idx = [get_target_neuron_index()]

    # Creating a key for last hidden layer_idx in the enabled_neurons dict.
    # The reason I do len(layers) - 2   is I do subtract 1 since indexes start from 0,
    # I subtract another one since last layer_idx is response layer_idx, so I want to reach layer_idx before the last layer_idx.
    create_key_for_enabled_neurons(len(layers) - 2, enabled_neurons)
    # Adding the index of enabled neuron in last hidden layer_idx to the corresponding place in enabled_neurons dict.
    add_neuron_indices_to_enabled_neurons(len(layers) - 2, enabled_neurons, target_neuron_idx)

    # Setting flag value of target neuron in layer_idx 5 to true.
    layers[len(layers) - 2].flag[target_neuron_idx] = True

    return target_neuron_idx


# get_target_neuron_index will determine which neuron in the last hidden layer_idx will be the head of the cone and
# then return its index value.
def get_target_neuron_index():
    return 46
