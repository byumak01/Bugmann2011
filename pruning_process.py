import eqs_and_variables as ev
import draw


def index_array():
    arr = []
    for i in range(ev.neuron_count):
        arr.append(ev.pool_capacity + 1)
    return arr


# find_synapse_with_the_lowest_weight function finds synapse with the lowest weight outgoing from a neuron, for every
# neuron in a layer.
def find_synapse_with_the_lowest_weight(syn_obj):
    indices_of_synapses_with_min_weight = index_array()
    for idx in range(len(syn_obj.w)):
        pre_idx = syn_obj.i[idx]

        if syn_obj.w[idx] < indices_of_synapses_with_min_weight[pre_idx]:
            indices_of_synapses_with_min_weight[pre_idx] = syn_obj.w[idx]

    return indices_of_synapses_with_min_weight


def give_weights_back_to_the_pool(layer_obj, syn_obj, indices_of_synapses_with_min_weight):
    for syn_idx in range(len(syn_obj.w)):
        if syn_idx not in indices_of_synapses_with_min_weight:
            post_idx = syn_obj.j[syn_idx]

            layer_obj.w_pool[post_idx] += syn_obj.w[syn_idx]
            syn_obj.w[syn_idx] = 0


def pruning(layers, synapse_objects, folder_path):
    len_syn_objects = len(synapse_objects)

    for idx in range(0, len_syn_objects - 1):
        indices_of_synapses_with_min_weight = find_synapse_with_the_lowest_weight(synapse_objects[idx])
        give_weights_back_to_the_pool(layers[idx], synapse_objects[idx], indices_of_synapses_with_min_weight)
