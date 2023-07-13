# Layers used in simulation are created here.

from brian2 import *
import eqs_and_variables as ev


# create_poisson_group function creates a poisson group object as input layer_idx.
def create_poisson_group(neuron_count, firing_rate):
    return PoissonGroup(neuron_count, firing_rate)


# create_hidden_layers function creates an array which consists ever.
# IMPORTANT: Every hidden layer_idx will use same equations and will have same number of neurons.
# IMPORTANT: Simulation must have at least 1 hidden layer_idx.
# In other words you can not directly connect input_layer to response_layer with this code structure.
def create_layers(layer_count, neuron_count, neuron_eqs, pool_capacity):
    arr = []
    for i in range(layer_count):
        arr.append(
            NeuronGroup(neuron_count, neuron_eqs, threshold='v>v_th', reset='v = beta*v_th', method='euler',
                        refractory='refractory_period'))
        arr[i].w_pool = pool_capacity
        arr[i].namespace['tau'] = ev.tau
        arr[i].namespace['v_th'] = ev.threshold
        arr[i].namespace['beta'] = ev.beta
        arr[i].namespace['refractory_period'] = ev.refractory_period
    return arr


# create_hidden_layer_mon function creates monitors for every hidden layer_idx,
# which will allow us to monitor values like state_of_neuron, total_current values of neurons etc.
def create_layer_mon(layers):
    arr = []
    for i in range(len(layers)):
        arr.append(StateMonitor(layers[i], ['v', 'total_current', 'w_pool'], record=True))
    return arr


# Creating Synapse Objects
# IMPORTANT: Every synapse_obj object will use same equations and on_pre, on_post arguments.
# connect() call between synapses is made inside another function. (Check connection_of_synapses.py)
def create_synapse_objects(syn_eqs, layers, input_layer, on_pre_arg, on_post_arg):
    hidden_layers_len = len(layers)
    # First I connect input_layer with first hidden_layer,
    # since input_layer is not in the same list with hidden layers I do that separately.
    arr = [Synapses(input_layer, layers[0], model=syn_eqs, on_pre=on_pre_arg, on_post=on_post_arg)]

    # Then I connect other hidden layers here. Every hidden layer_idx is connected to next hidden layer_idx in the list.
    # For example hidden layer_idx 2 is connected to hidden layer_idx 3 and hidden layer_idx 3 is connected to hidden layer_idx 4.
    for i in range(0, hidden_layers_len - 1):
        arr.append(Synapses(layers[i], layers[i + 1], model=syn_eqs, on_pre=on_pre_arg, on_post=on_post_arg))


    return arr
