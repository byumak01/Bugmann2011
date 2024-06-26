from brian2 import *
import eqs_and_variables as ev
import draw
import math


# spike_k represents the k. spike t.
# spike_k_minus_1 represents the k-1. spike t.
# t represents current simulation t.

# Creating a hashmap for alpha function values.
def create_hash_map_for_alpha_function():
    h_map = {}
    for x in range(0, 151, 1):
        x_value = x / 10.0
        result = (math.exp(1) / (ev.t_max / ms)) * x_value * math.exp(-(x_value / (ev.t_max / ms)))
        h_map[x_value] = result
    return h_map


# Alpha function
def alpha_function(t, spike_k, hash_map):
    key = round((t - spike_k - ev.dirac) / ms, 1)
    return hash_map[key] if key in hash_map else 0


# Synaptic Depression
def synaptic_depression(spike_k, spike_k_minus_1, synaptic_w):
    if spike_k_minus_1 == 0:
        # If prev_prev_spike condition is met that means we are calculating synaptic depression for first spike.
        # Since there is no spike before first spike we return weight of the synapse_obj directly without multiplying it
        # with (1 - exp(-(prev_spike - prev_prev_spike) / ev.tau)) term.
        return synaptic_w
    else:
        return synaptic_w * (1 - exp(-(spike_k - spike_k_minus_1) / ev.tau))


# Calculating Total Current
def calculate_synaptic_current(t, spike_k, spike_k_minus_1, synaptic_w, hash_map):
    return alpha_function(t, spike_k, hash_map) * synaptic_depression(spike_k, spike_k_minus_1, synaptic_w)


def create_key_for_results(results, synapse_obj_idx, post_neuron_idx):
    results[(synapse_obj_idx, post_neuron_idx)] = [0]


def total_synaptic_current(t, spike_times_dict, layers, synapse_objects, folder_path, hash_map, termination_condition):
    # I first create a dictionary to store calculated values inside it.
    # The key side of this dictionary will be very similar to the spike_times dictionary.
    # Key is a tuple with 2 elements. First element represents which layer_idx object index does
    # the post synaptic neuron belongs.
    # Second element will represent index of post-synaptic neuron.
    # Value side holds total_current value.
    results = {}
    # For loop below will iterate over all keys in the spike_times dictionary.
    for key in spike_times_dict:
        # Synapse object index for selected key
        synapse_obj_idx = key[0]

        # synapse_obj index for selected key
        synapse_idx = key[1]

        # length of the spike times array for selected key
        length = len(spike_times_dict[key])

        # Index for post synaptic neuron.
        post_neuron_idx = synapse_objects[synapse_obj_idx].j[synapse_idx]

        # Path for weight value of selected synapse_obj.
        synapse_weight = synapse_objects[synapse_obj_idx].w[synapse_idx]

        # If a key does not exist for selected post-synaptic neuron a new key is created.
        if not (synapse_obj_idx, post_neuron_idx) in results:
            create_key_for_results(results, synapse_obj_idx, post_neuron_idx)

        # current for selected synapse_obj is calculated (for last 20 spikes) then added to its place
        # in results dictionary.
        for idx in range(length - 1):
            results[(synapse_obj_idx, post_neuron_idx)] += calculate_synaptic_current(t, spike_times_dict[key][idx + 1],
                                                                                      spike_times_dict[key][idx],
                                                                                      synapse_weight, hash_map)

    # We will add values inside results dictionary to correct places in neuron group objects.
    # I also draw state_of_neuron value of selected neuron.
    for key2 in results:
        layer_idx = key2[0]
        neuron_idx = key2[1]
        layers[layer_idx].total_current[neuron_idx] = results[key2]
        voltage = layers[layer_idx].v[neuron_idx]

        if (t / ms % ev.screenshot_per == 0 or termination_condition) and (
        layers[layer_idx].fire_count[neuron_idx] > 0 if layer_idx != ev.layer_count - 1 else True):
            draw.draw_neuron_activity(voltage, neuron_idx, layer_idx)
            draw.draw_if_recruited(neuron_idx, layer_idx)
            draw.draw_outlines_layer_names_and_time(t, folder_path, False, ev.run_counter)
