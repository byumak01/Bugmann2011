import eqs_and_variables as ev
from brian2 import *
import draw


# When a spike is received a new key in the weight_delay dictionary is created. For more information about weight_delay
# dictionary please check where weight_delay dictionary is defined (main.py).
def create_key_for_weight_delay(time, syn_obj_idx, weight_delay_dict):
    weight_delay_dict[(time / ms + ev.delay / ms, syn_obj_idx)] = []


# Indexes of synapses which received the spike will be appended to appropriate places in weight_delay dictionary.
def add_indexes_to_weight_delay(time, syn_obj_idx, weight_delay_dict, syn_indices):
    weight_delay_dict[(time / ms + ev.delay / ms, syn_obj_idx)].append(syn_indices)


# If key value for a synapse_obj does not exist in spike times dictionary this function creates the key.
def create_key_for_spike_times(syn_obj_idx, syn_idx, spike_times):
    # I am appending first value saved inside key as 0. Reason for that is explained below:
    # Synaptic Depression function takes k. spike and k-1. spike as its arguments, But there is no spike came before the
    # first spike. So this is a special case and by adding 0 to the beginning I am kinda assuming spike came before the
    # first spike came at 0. second. Please check synaptic_depression() function inside synaptic_current.py to see how
    # synaptic depression is calculated for this special case.
    spike_times[(syn_obj_idx, syn_idx)] = [0]


# Function below will remove the first element of given array from spike times dictionary.
def remove_spike_time(syn_obj_idx, syn_idx, spike_times):
    spike_times[(syn_obj_idx, syn_idx)].pop(0)


# add_spike_time function will add the spike t to the correct place in spike times dictionary.
def add_spike_time(synapse_obj, syn_obj_idx, syn_idx, spike_times):
    spike_times[(syn_obj_idx, syn_idx)].append(synapse_obj.spike_time[syn_idx])
    # Since we are interested in only last 20 spike we will remove more than that.
    # But since we also need k-1. spike t for synaptic depression we will remove first element array when length
    # becomes greater than 21.
    if len(spike_times[(syn_obj_idx, syn_idx)]) > 21:
        remove_spike_time(syn_obj_idx, syn_idx, spike_times)


# check_synapses function will iterate over all synapses for given Synapse object and return the indexes of synapses
# which received a spike.
def check_synapses(synapse_obj):
    arr = []
    for idx in range(len(synapse_obj.spike_fired)):
        if synapse_obj.spike_fired[idx]:
            # We first make spike_fired variable False again for all synapses so that when we receive a new spike
            # we can understand it.
            synapse_obj.spike_fired[idx] = False
            # Adding transmission probability:
            if rand() < ev.transmission_p:
                arr.append(idx)
    return arr


# This function will check if any spikes fired.
def check_any_spikes(t, synapse_objects, weight_delay, spike_times, layers):
    # The for loop will let us iterate over all synapse_obj objects.
    for synapse_obj in synapse_objects:
        # I store the index of Synapse object inside a variable.
        syn_obj_idx = synapse_objects.index(synapse_obj)
        # If any spike came from selected Synapse object the spike_fired value of the synapse which received the
        # spike will be True.
        # If any spikes are received, I store the index value of synapses which transmitted spike inside a variable
        # named syn_indices.
        syn_indices = check_synapses(synapse_obj)
        # draw_firing_neurons_in_stimulus_layer will draw firing neurons in stimulus layer if any.
        draw.draw_firing_neurons_in_stimulus_layer(
            synapse_obj.i[syn_indices]) if syn_obj_idx == 0 and t / ms % 10 == 0 else None
        # Increase received spike count for neurons which received spikes.
        post_neuron_idx = synapse_obj.j[syn_indices]
        layers[syn_obj_idx].received_spike_count[post_neuron_idx] += 1
        # Increase fired spike count for neurons which fired spikes.
        pre_neuron_idx = synapse_obj.i[syn_indices]
        layers[syn_obj_idx - 1].fire_count[pre_neuron_idx] += 1 if syn_obj_idx != 0 else 0
        # If any spikes are received, the indexes would be assigned to syn_indices variable, so the condition below will
        # be True
        if len(syn_indices) > 0:
            # Now we will iterate over syn_indices to put every spike t correct places in our dictionary named as
            # spike_times.
            for syn_idx in syn_indices:
                if (syn_obj_idx, syn_idx) in spike_times:
                    # If we already have a key for the selected Synapse object and synapse_obj index, we append spike t
                    # to there.
                    add_spike_time(synapse_obj, syn_obj_idx, syn_idx, spike_times)
                else:
                    # If we do not have a key for the selected synapse_obj and synapse_obj object we create a new key
                    # and then append the spike t to there.
                    create_key_for_spike_times(syn_obj_idx, syn_idx, spike_times)
                    add_spike_time(synapse_obj, syn_obj_idx, syn_idx, spike_times)

            idx = 0
            range = len(syn_indices)
            # If neuron is selected do not change the weight.
            while idx < range:
                syn_idx = syn_indices[idx]
                if synapse_obj.is_selected[syn_idx]:
                    del syn_indices[idx]
                    range -= 1
                idx += 1

            if len(syn_indices) > 0:
                # Creating key for weight_delay dictionary.
                create_key_for_weight_delay(t, syn_obj_idx, weight_delay)
                # Adding indexes of synapses which received a spike to value side of created key.
                add_indexes_to_weight_delay(t, syn_obj_idx, weight_delay, syn_indices)
