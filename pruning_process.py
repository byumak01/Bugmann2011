import eqs_and_variables as ev
import draw


def index_array():
    arr = []
    for i in range(ev.neuron_count):
        arr.append([])
    return arr


# find_synapse_with_the_lowest_weight function finds synapse with the lowest weight outgoing from a neuron, for every
# neuron in a layer.
def find_synapse_with_the_lowest_weight(syn_obj, layer_obj, enabled_neurons, layer_idx, input_neurons):
    layer_obj.is_recruited[:] = False

    indices_of_synapses_with_min_weight = index_array()

    if layer_idx >= 1:
        neurons_to_iterate = enabled_neurons[layer_idx - 1]
    else:
        neurons_to_iterate = input_neurons

    for syn_idx in range(len(syn_obj.w)):
        pre_idx = syn_obj.i[syn_idx]
        if pre_idx in neurons_to_iterate:

            if syn_obj.w[syn_idx] < indices_of_synapses_with_min_weight[pre_idx] or indices_of_synapses_with_min_weight[pre_idx] == []:
                # pre_idx deki norunu hangi synapse en iyi temsil ediyorsa o deger kaydediliyor.
                indices_of_synapses_with_min_weight[pre_idx] = syn_idx

    for idx in indices_of_synapses_with_min_weight:
        post_idx = syn_obj.j[idx]
        layer_obj.is_recruited[post_idx] = True

    return indices_of_synapses_with_min_weight


def give_weights_back_to_the_pool(layer_obj, syn_obj, indices_of_synapses_with_min_weight):
    for syn_idx in range(len(syn_obj.w)):
        if syn_idx not in indices_of_synapses_with_min_weight:
            post_idx = syn_obj.j[syn_idx]

            layer_obj.w_pool[post_idx] += syn_obj.w[syn_idx]
            syn_obj.w[syn_idx] = 0


def draw_after_pruning(layer_obj, layer_idx, folder_path):
    for neuron_idx in range(len(layer_obj.v)):
        if layer_obj.is_recruited[neuron_idx]:
            voltage = layer_obj.v[neuron_idx]
            draw.draw_neuron_activity(voltage, neuron_idx, layer_idx)
            draw.draw_if_recruited(neuron_idx, layer_idx + 1)
            draw.draw_outlines_layer_names_and_time(ev.run_time, folder_path)


def pruning(layers, synapse_objects, folder_path, enabled_neurons, input_neurons):
    len_syn_objects = len(synapse_objects)

    for obj_idx in range(0, len_syn_objects - 1):
        indices_of_synapses_with_min_weight = find_synapse_with_the_lowest_weight(synapse_objects[obj_idx],
                                                                                  layers[obj_idx], enabled_neurons, obj_idx, input_neurons)
        print("weights", synapse_objects[obj_idx].w)
        print("inside pruning", indices_of_synapses_with_min_weight)
        print("is_recruited", layers[obj_idx].is_recruited)
        give_weights_back_to_the_pool(layers[obj_idx], synapse_objects[obj_idx], indices_of_synapses_with_min_weight)
        draw_after_pruning(layers[obj_idx], obj_idx, folder_path)
