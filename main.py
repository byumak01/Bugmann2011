# Code is written by: Barış YUMAK
# 12/06/2023  01.36

from brian2 import *
import save_simulation_setup_and_results as sssr
import connection_of_synapses as cofs
import eqs_and_variables as ev
import synaptic_current as sc
import create_layers as cl
import check_for_spikes as cs
import weight_rule as wr
import enable_flag as ef
import time
import draw
import datetime
import os

# Starting t to calculate how much t it takes to run simulation.
start = time.time()

# Creating path for saving results and variables used in simulation.
current_date = datetime.datetime.now().strftime("%d%m%Y_%H%M")
folder_path = f"RESULTS/{ev.input_shape}_{current_date}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Creating a hashmap for alpha function values.
hash_map = sc.create_hash_map_for_alpha_function()

# Defining a dictionary to hold spike times inside it.
# Every synapse_obj will have its own key and the spike times for that synapse_obj will be stored in the value part.
# The key will be a tuple with 2 values. First value will represent the Synapse object number, second value will
# represent the synapse_obj number. For example if a key is (1, 2) that means this is the key for second synapse_obj of
# first synapse_obj object.
spike_times = ev.create_dictionary()

# Dictionary named as weight_delay holds a dictionary named "indexes" until delay t is passed.
# Key for this dictionary is the t and Synapse object which received a spike.
# For example if a spike came at 20. ms, a key will be created and its first value will be 20 + delay and second
# value will be the Synapse objects index.
# Create a dictionary for holding weight until delay t is passed.
weight_delay = ev.create_dictionary()

# Dictionary which hold indices of enabled neurons for each layer_idx. key represents the hidden layer_idx index,
# value side has index values for enabled neurons in selected layer_idx.
# This dictionary will be useful while we perform pruning.
enabled_neurons = ev.create_dictionary()

# Defining input layer_idx as a Poisson Group.
# Their firing rate will be changed later.
input_layer = cl.create_poisson_group(ev.neuron_count, ev.initial_firing_rate)

# I define a spike monitor to be able to track spike times.
input_layer_mon = SpikeMonitor(input_layer, record=True)

# Creating hidden layers, used variables and equations are defined inside eqs_and_variables.py file.
layers = cl.create_layers(ev.layer_count, ev.neuron_count, ev.neuron_eqs, ev.pool_capacity)

# Creating State Monitors for each hidden layer_idx to be able to track state_of_neuron, total current values and pool reserves of
# neurons in the layers.
layer_mon = cl.create_layer_mon(layers)

# Creating synapse objects that connects layers to each other.
synapse_objects = cl.create_synapse_objects(ev.syn_eqs, layers, input_layer, ev.on_pre_arg,
                                            ev.on_post_arg)

# Finding which neuron in last hidden layer_idx will be the head of the cone then setting its flag to true.
target_neuron_idx = ef.set_target_neuron_flag(layers, enabled_neurons)

# Setting enable flag for rest of the layers
if len(layers) - 3 >= 0:
    ef.set_enable_flags_for_rest(layers, target_neuron_idx, ev.ng_row_count, ev.ng_column_count, ev.rf_row_count,
                                 ev.rf_column_count, len(layers) - 3, enabled_neurons)

# Making synaptic connections between layers.
for post_neuron_idx in range(ev.neuron_count):
    cofs.make_synaptic_connections(post_neuron_idx, ev.ng_row_count, ev.ng_column_count, ev.rf_row_count,
                                   ev.rf_column_count, synapse_objects, ev.syn_connection_prob)

# Giving initial values to synapse objects
cofs.set_initial_variables(synapse_objects, ev.initial_weights, ev.probability)

for element in ev.responses[ev.response_shape]:
    layers[len(layers) - 1].flag[element] = True


@network_operation(when='after_end')
def updater(t):
    # I am resetting the board's part which shows state_of_neuron levels of the neurons so that I can draw current
    # state_of_neuron levels.
    draw.reset_board()
    # Drawing enabled neurons.
    draw.draw_enabled_neurons(layers)
    # Drawing active neurons in stimulus layer.
    draw.draw_active_neurons_in_stimulus_layer(ev.inputs[ev.input_shape])

    # check_any_spikes function will check if a spike is fired during current t step.
    # If a spike is fired it will be stored inside a dictionary. For more explanation about dictionary please check
    # spike_times = {} declaration inside synaptic_current.py
    # Also indexes of synapses which received a spike will be stored inside a dictionary. When delay t is passed,
    # weight update function will be called by using information stored in this dictionary and weights will be updated.
    cs.check_any_spikes(t, synapse_objects, weight_delay, spike_times)

    # check_if_delay_time_passed function will check if any weights needs to be updated at current t step.
    # If there are any weights that needs to be updated key to reach that synaptic indexes is returned.
    # Otherwise, function returns 0.
    wd_keys = wr.check_if_delay_time_passed(t / ms, weight_delay)

    # If wd_key has another value than [] that means there are synapses
    if wd_keys:
        wr.call_weight_update(wd_keys, weight_delay, layers, synapse_objects)
        # print("Current t", t)
        # print(synapse_objects[0].w)
    # total_synaptic_current function will calculate total synaptic current for every neuron.
    sc.total_synaptic_current(t, spike_times, layers, synapse_objects, folder_path, hash_map)


# Arraylarin icinde tanimlanmis NG'leri vs. bu sekilde yapmak lazim !!!
net = Network(collect())
net.add(layers, layer_mon, synapse_objects)

for element in ev.inputs[ev.input_shape]:
    input_layer.rates[element] = ev.firing_rate

net.run(ev.run_time)

end = time.time()

elapsed_time = end - start
sssr.save_simulation_setup_and_results(folder_path, elapsed_time)
print('Execution t:', elapsed_time, 'seconds')


print(input_layer_mon.i)
print(input_layer_mon.t)
"""
print(synapse_objects[0].w)
print(len(layers))
"""

print(layers[0].fire_count)
print(layers[1].fire_count)
print(layers[2].fire_count)
print(layers[3].fire_count)
print(layers[4].fire_count)
print(layers[5].fire_count)
