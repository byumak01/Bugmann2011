from brian2 import *
import eqs_and_variables as ev
import draw


def add_to_selected_synapses(layer_obj_idx, neuron_idx, selected_synapses, selected_synapse_idx):
    key = (layer_obj_idx, neuron_idx)
    if key not in selected_synapses:
        selected_synapses[key] = []
    # selected synapse idx is a tuple i,j
    selected_synapses[key].append(selected_synapse_idx)


# spesifik bir norondan cikan butun agirliklari yazdir yaptigi secimi kontrol et
#
# find_synapse_with_the_lowest_weight function finds synapse with the lowest weight outgoing from a neuron, for every
# neuron in a layer.
def select_synapses_with_min_w(syn_obj_idx, syn_obj, layer_obj, selected_neuron_idx):

    pre_idx = selected_neuron_idx
    sorted_weights = sorted(syn_obj.w[pre_idx, :])
    i = 0
    min_w = sorted_weights[i]
    min_w_idx = None
    p_idx = None
    exit_loop = False

    while not exit_loop:
        # alttaki for looptan degistirerek kurtulabiliriz.
        # birbirine cok yakin agirliklar oldugu durumda random atcak virgulden sonra 4 basamaga gore roundlicaz.
        # sort etmeye gerek olmayabilir belki ??
        for post_idx in ev.rf_array[selected_neuron_idx]:
            if syn_obj.w[pre_idx, post_idx] == min_w:
                # after and should not be necessary
                if layer_obj.is_enabled[post_idx] and not syn_obj.is_selected[pre_idx, post_idx] and min_w > 0:
                    min_w_idx = (pre_idx, post_idx)
                    p_idx = post_idx
                    exit_loop = True
                else:
                    if i + 1 < len(sorted_weights):
                        i += 1
                        min_w = sorted_weights[i]
                    else:
                        exit_loop = True

    if p_idx is not None:
        syn_obj.is_selected[pre_idx, p_idx] = True
        layer_obj.selected_neuron[p_idx] = True
        add_to_selected_synapses(syn_obj_idx - 1, pre_idx, ev.selected_synapses, min_w_idx)

    return p_idx


def give_weights_back_to_pool(syn_obj, layer_obj):
    synapse_count = len(syn_obj.w)

    for idx in range(synapse_count):
        if not syn_obj.is_selected[idx]:
            post_idx = syn_obj.j[idx]
            layer_obj.w_pool[post_idx] += syn_obj.w[idx]
            syn_obj.w[idx] = 0


def draw_after_pruning_state(selected_synapses):
    # key -1 var unutma
    print(selected_synapses)
    for ky in selected_synapses:
        for idx_pair in selected_synapses[ky]:
            obj_idx = ky[0] + 1
            neuron_idx = idx_pair[1]
            draw.draw_neuron_activity(ev.threshold, neuron_idx, obj_idx)


def pruning(layers, synapse_objects, folder_path, is_pruning, run_count):
    len_syn_objects = len(synapse_objects)
    selected_neuron_indices = set(ev.inputs[ev.input_shape])
    for idx in range(0, len_syn_objects - 1):
        hold_indices = []
        for selected_neuron_idx in selected_neuron_indices:
            if selected_neuron_idx is not None:
                selected_neuron_idx = select_synapses_with_min_w(idx, synapse_objects[idx], layers[idx],
                                                                  selected_neuron_idx)

                hold_indices.append(selected_neuron_idx)
        give_weights_back_to_pool(synapse_objects[idx], layers[idx])
        selected_neuron_indices = set(hold_indices)

    draw.reset_board()
    draw.draw_active_neurons_in_stimulus_layer(ev.inputs[ev.input_shape])
    draw_after_pruning_state(ev.selected_synapses)
    draw.draw_outlines_layer_names_and_time(ev.run_time + 1 * ms, folder_path, is_pruning, run_count)
