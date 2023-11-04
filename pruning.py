from brian2 import *
import eqs_and_variables as ev
import draw
import random


def add_to_selected_synapses(layer_obj_idx, neuron_idx, selected_synapses, selected_synapse_idx):
    key = (layer_obj_idx, neuron_idx)
    if key not in selected_synapses:
        selected_synapses[key] = []
    # selected synapse idx is a tuple i,j
    selected_synapses[key].append(selected_synapse_idx)


# ROUND EDIP MINIMUMLAR ARASINDAN RASTGELE SECEN ALGORITMA
def select_synapses_with_min_w(syn_obj_idx, syn_obj, layer_obj, selected_neuron_idx):
    pre_idx = selected_neuron_idx

    post_indices = ev.rf_array[selected_neuron_idx]

    digit_count = 4

    p_idx = None
    min_w_idx = None

    weights = syn_obj.w[pre_idx, :]

    # We round after digit_count digit
    weights = [round(weight, digit_count) for weight in weights]

    # We take out zeros from weights
    non_zero_weights = [weight for weight in weights if weight != 0]

    non_zero_weights = set(non_zero_weights)

    non_zero_weights = list(non_zero_weights)

    non_zero_weights = sorted(non_zero_weights)

    # Get minimum weight
    if non_zero_weights:

        # a list for storing post indices with same min_w.
        indices_with_same_w = []

        loop_flag = False

        while not loop_flag and non_zero_weights:
            min_w = non_zero_weights.pop(0)
            find_synapses_with_min_w(pre_idx, post_indices, syn_obj, min_w, digit_count, indices_with_same_w)

            if indices_with_same_w:
                p_idx = random.choice(indices_with_same_w)
                min_w_idx = (pre_idx, p_idx)
                loop_flag = True

        prob = 1
        if p_idx is not None and rand() <= prob:
            syn_obj.is_selected[pre_idx, p_idx] = True
            layer_obj.selected_neuron[p_idx] = True
            add_to_selected_synapses(syn_obj_idx - 1, pre_idx, ev.selected_synapses, min_w_idx)

    return p_idx


def find_synapses_with_min_w(pre_idx, post_indices, syn_obj, min_w, digit_count, indices_with_same_w):
    for post_idx in post_indices:
        if syn_obj.is_enabled[pre_idx, post_idx] and not syn_obj.is_selected[pre_idx, post_idx]:
            if np.round(syn_obj.w[pre_idx, post_idx], digit_count) == min_w:
                indices_with_same_w.append(post_idx)


def give_weights_back_to_pool(syn_obj, layer_obj):
    synapse_count = len(syn_obj.w)

    for idx in range(synapse_count):
        if not syn_obj.is_selected[idx]:
            post_idx = syn_obj.j[idx]
            layer_obj.w_pool[post_idx] += syn_obj.w[idx]
            syn_obj.w[idx] = 0


def draw_after_pruning_state(selected_synapses):
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
