# Code is written by: Barış YUMAK
# 12/06/2023  01.36

from brian2 import *
import connection_of_synapses as cofs
import eqs_and_variables as ev
import synaptic_current as sc
import create_layers as cl
import check_for_spikes as cs
import weight_rule as wr
import enable_flag as ef
import time
import draw

# Starting time to calculate how much time it takes to run simulation.
start = time.time()

# Defining a dictionary to hold spike times inside it.
# Every synapse_obj will have its own key and the spike times for that synapse_obj will be stored in the value part.
# The key will be a tuple with 2 values. First value will represent the Synapse object number, second value will
# represent the synapse_obj number. For example if a key is (1, 2) that means this is the key for second synapse_obj of
# first synapse_obj object.
spike_times = ev.create_dictionary()

# Dictionary named as weight_delay holds a dictionary named "indexes" until delay time is passed.
# Key for this dictionary is the time and Synapse object which received a spike.
# For example if a spike came at 20. ms, a key will be created and its first value will be 20 + delay and second
# value will be the Synapse objects index.
# Create a dictionary for holding weight until delay time is passed.
weight_delay = ev.create_dictionary()

# Dictionary which hold indices of enabled neurons for each layer. key represents the hidden layer index,
# value side has index values for enabled neurons in selected layer.
# This dictionary will be useful while we perform pruning.
enabled_neurons = ev.create_dictionary()

# Defining input layer as a Poisson Group.
# Their firing rate will be changed later.
input_layer = cl.create_poisson_group(ev.neuron_count, ev.firing_rate)

# I define a spike monitor to be able to track spike times.
input_layer_mon = SpikeMonitor(input_layer, record=True)

# Creating hidden layers, used variables and equations are defined inside eqs_and_variables.py file.
layers = cl.create_layers(ev.layer_count, ev.neuron_count, ev.neuron_eqs, ev.pool_capacity)

# Creating State Monitors for each hidden layer to be able to track voltage, total current values and pool reserves of
# neurons in the layers.
layer_mon = cl.create_layer_mon(layers)

# Creating synapse objects that connects layers to each other.
synapse_objects = cl.create_synapse_objects(ev.syn_eqs, layers, input_layer, ev.on_pre_arg,
                                            ev.on_post_arg)

# Finding which neuron in last hidden layer will be the head of the cone then setting its flag to true.
target_neuron_idx = ef.set_target_neuron_flag(layers, enabled_neurons)

# Setting enable flag for rest of the layers
if len(layers) - 3 >= 0:
    ef.set_enable_flags_for_rest(layers, target_neuron_idx, ev.ng_row_count, ev.ng_column_count, ev.rf_row_count,
                                 ev.rf_column_count, len(layers) - 3, enabled_neurons)

for i in range(len(layers)):
    print(layers[i].flag)

# Making synaptic connections between layers.
for post_neuron_idx in range(ev.neuron_count):
    cofs.make_synaptic_connections(post_neuron_idx, ev.ng_row_count, ev.ng_column_count, ev.rf_row_count,
                                   ev.rf_column_count, synapse_objects)

# Giving initial values to synapse objects
cofs.set_initial_variables(synapse_objects, ev.initial_weights, ev.probability)

# Drawing enabled neurons.
draw.draw_enabled_neurons(layers)


@network_operation(when='after_end')
def updater(t):
    # I am resetting the board's part which shows voltage levels of the neurons so that I can draw current
    # voltage levels.
    draw.reset_board()

    # check_any_spikes function will check if a spike is fired during current time step.
    # If a spike is fired it will be stored inside a dictionary. For more explanation about dictionary please check
    # spike_times = {} declaration inside synaptic_current.py
    # Also indexes of synapses which received a spike will be stored inside a dictionary. When delay time is passed,
    # weight update function will be called by using information stored in this dictionary and weights will be updated.
    cs.check_any_spikes(t, synapse_objects, weight_delay, spike_times)

    # check_if_delay_time_passed function will check if any weights needs to be updated at current time step.
    # If there are any weights that needs to be updated key to reach that synaptic indexes is returned.
    # Otherwise, function returns 0.
    wd_keys = wr.check_if_delay_time_passed(t / ms, weight_delay)

    # If wd_key has another value than [] that means there are synapses
    if wd_keys:
        wr.call_weight_update(wd_keys, weight_delay, layers, synapse_objects)
        # print("Current time", t)
        # print(synapse_objects[0].w)
    # total_synaptic_current function will calculate total synaptic current for every neuron.
    sc.total_synaptic_current(t, spike_times, layers, synapse_objects)


# Arraylarin icinde tanimlanmis NG'leri vs. bu sekilde yapmak lazim !!!
net = Network(collect())
net.add(layers, layer_mon, synapse_objects)

input_layer.rates[:16] = 100 * Hz

net.run(50 * ms)

end = time.time()

elapsed_time = end - start
print('Execution time:', elapsed_time, 'seconds')

# plt.figure(300)
# plt.plot(layer_mon[0].t / ms, layer_mon[0].v[5], label='v', color='b')
# plt.plot(layer_mon[0].t / ms, (layer_mon[0].total_current[5]) / 400, label='current', color='r',
#          linestyle='dashed')
# plt.title("Graph for v")
# xlabel('Time (ms)')
# ylabel('v (volt)')
# legend()
# plt.show()

print(input_layer_mon.i)
print(input_layer_mon.t)
print(synapse_objects[0].w)
