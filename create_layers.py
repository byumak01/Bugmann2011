# Layers used in simulation are created here.

from brian2 import *
import eqs_and_variables as ev


# create_poisson_group function creates a poisson group object as input layer.
def create_poisson_group(neuron_count, firing_rate):
    return PoissonGroup(neuron_count, firing_rate)


# create_hidden_layers function creates an array which consists ever.
# IMPORTANT: Every hidden layer will use same equations and will have same number of neurons.
# IMPORTANT: Simulation must have at least 1 hidden layer.
# In other words you can not directly connect input_layer to response_layer with this code structure.
def create_hidden_layers(hidden_layer_count, neuron_count, neuron_eqs, pool_capacity):
    arr = []
    for i in range(hidden_layer_count):
        arr.append(
            NeuronGroup(neuron_count, neuron_eqs, threshold='v>v_th', reset='v = beta*v_th', method='euler',
                        refractory='refractory_period'))
        arr[i].w_pool = pool_capacity
        arr[i].namespace['tau'] = ev.tau
        arr[i].namespace['v_th'] = ev.threshold
        arr[i].namespace['beta'] = ev.beta
        arr[i].namespace['refractory_period'] = ev.refractory_period
    return arr


# create_hidden_layer_mon function creates monitors for every hidden layer,
# which will allow us to monitor values like voltage, total_current values of neurons etc.
def create_hidden_layer_mon(hidden_layers):
    arr = []
    for i in range(len(hidden_layers)):
        arr.append(StateMonitor(hidden_layers[i], ['v', 'total_current', 'w_pool'], record=True))
    return arr


# create_response_layer function will create response layer
def create_response_layer(neuron_count, neuron_eqs, pool_capacity):
    response_layer = NeuronGroup(neuron_count, neuron_eqs, threshold='v>v_th', reset='v = beta*v_th', method='euler',
                                 refractory='refractory_period')
    response_layer.w_pool = pool_capacity
    response_layer.namespace['tau'] = ev.tau
    response_layer.namespace['v_th'] = ev.threshold
    response_layer.namespace['beta'] = ev.beta
    response_layer.namespace['refractory_period'] = ev.refractory_period
    return response_layer


# Creating Synapse Objects
# IMPORTANT: Every synapse_obj object will use same equations and on_pre, on_post arguments.
# connect() call between synapses is made inside another function. (Check connection_of_synapses.py)
def create_synapse_objects(syn_eqs, hidden_layers, response_layer, input_layer, on_pre_arg, on_post_arg):
    hidden_layers_len = len(hidden_layers)
    # First I connect input_layer with first hidden_layer,
    # since input_layer is not in the same list with hidden layers I do that separately.
    arr = [Synapses(input_layer, hidden_layers[0], model=syn_eqs, on_pre=on_pre_arg, on_post=on_post_arg)]

    # Then I connect other hidden layers here. Every hidden layer is connected to next hidden layer in the list.
    # For example hidden layer 2 is connected to hidden layer 3 and hidden layer 3 is connected to hidden layer 4.
    for i in range(1, hidden_layers_len - 1):
        arr.append(
            Synapses(hidden_layers[i], hidden_layers[i + 1], model=syn_eqs, on_pre=on_pre_arg, on_post=on_post_arg))

    # Lastly I make the connection between last hidden layer and Response layer.
    # I do this separately because connection rule between last layer and response layer is different.
    # Also for same reason I did create response layer separately in another function.
    arr.append(Synapses(hidden_layers[hidden_layers_len - 1], response_layer, model=syn_eqs, on_pre=on_pre_arg))

    return arr
