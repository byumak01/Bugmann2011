from brian2 import *
import eqs_and_variables as ev

# spike_k represents the k. spike time.
# spike_k_minus_1 represents the k-1. spike time.
# t represents current simulation time.


# Defining a dictionary to hold spike times inside it.
# Every synapse_obj will have its own key and the spike times for that synapse_obj will be stored in the value part.
# The key will be a tuple with 2 values. First value will represent the Synapse object number, second value will
# represent the synapse_obj number. For example if a key is (1, 2) that means this is the key for second synapse_obj of
# first synapse_obj object.
spike_times = {}


# Alpha function
def alpha_function(t, spike_k):
    return (exp(1) / ev.t_max) * (t - spike_k - ev.dirac) * exp(-(t - spike_k - ev.dirac) / ev.t_max) if (
            t > (spike_k + ev.dirac)) else 0


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
def calculate_synaptic_current(t, spike_k, spike_k_minus_1, synaptic_w):
    return alpha_function(t, spike_k) * synaptic_depression(spike_k, spike_k_minus_1, synaptic_w)


def create_key_for_results(results, synapse_obj_idx, post_neuron_idx):
    results[(synapse_obj_idx, post_neuron_idx)] = [0]


def total_synaptic_current(t, spike_times_dict, hidden_layers, synapse_objects):
    # I first create a dictionary to store calculated values inside it.
    # The key side of this dictionary will be very similar to the spike_times dictionary.
    # Key is a tuple with 2 elements. First element represents which hidden layer object index does
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

        # current for selected synapse_obj is calculated (for last 20 spikes) then added to its place in results dictionary.
        for idx in range(length - 1):
            results[(synapse_obj_idx, post_neuron_idx)] += calculate_synaptic_current(t, spike_times_dict[key][idx + 1],
                                                                                      spike_times_dict[key][idx],
                                                                                      synapse_weight)

    # We will add values inside results dictionary to correct places in neuron group objects.
    for key2 in results:
        hidden_layers[key2[0]].total_current[key2[1]] = results[key2]