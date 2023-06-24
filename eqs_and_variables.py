from brian2 import *

# Initializing variables.
# threshold represents threshold value for post-synaptic neuron.
threshold = 15 / 1000

# beta
beta = 0.91

# tau represents RC time constant.
tau = 50 * ms

# t_max represents dendritic distance between synapse_obj and soma.
t_max = 1 * ms

# dirac represents axonal propagation time between the pre-synaptic neuron and synapse_obj.
dirac = 1 * ms

# fraction represents how much of the pool will be taken. (Takes values between 0 and 1).
# If fraction is 1, then it takes all the pool.
fraction = 0.8

# delay represents how much time needs to pass until new synaptic weights become active after a spike arrives.
delay = 2 * ms

refractory_period = 2*ms

# initial_weights represents initial synaptic weights.
initial_weights = 0

# Synaptic transmission probability
probability = 1

# pool_capacity represents weight pool capacity of neuron
pool_capacity = 8

# firing_rate represents the initial firing rate of Poisson group neurons
firing_rate = 0 * Hz

# hidden_layer_count represents how many hidden layers will be in simulation.
hidden_layer_count = 1

# neuron_count variable shows how many neurons will be in a layer.
neuron_count = 100

# row count
ng_row_count = 10

# column count
ng_column_count = 10

# rf row count
rf_row_count = 5

# rf column count
rf_column_count = 5


def create_dictionary():
    return {}


# Defining necessary equations and variables for Neuron Group object.
neuron_eqs = '''
dv/dt = -(v/(tau)) + total_current*Hz : 1 # Equation 1 from article.
w_pool : 1   # w_pool will be used for weight pool of neuron.
total_current : 1 # Represents total synaptic current from article.
fire_count : 1 # This variable is used for finding out how many times a neuron produced a spike.
flag : boolean # If flag value of a neuron is True, that means neuron can receive and produce spikes.
'''

# Defining necessary variables for Synapse object.
syn_eqs = '''  
w : 1 # w represents the weights.
spike_fired : boolean # Becomes true if pre-synaptic neuron fired a spike, variable is used to determine which synapse_obj transmitted the spike.
spike_time_syn : second # Records the firing time.
p : 1 # Will represent probability.
'''

# Defining necessary arguments to execute when a pre-synaptic spike is fired.
on_pre_arg = '''
spike_fired = True*(rand()<p)
spike_time_syn = t
'''

# Defining necessary arguments to execute when post-synaptic spike is fired.
on_post_arg = '''
fire_count += 1/N_incoming  # When a post-synaptic neuron fires a spike this equation will increase the fire_count by 1 for the neuron that fired spike.
'''
# NOTE ABOUT fire_count variable: I could also do this incrementation in on_pre arguments but then I would not be able to increment this value for Response layer neurons.
# Because Response layer is not in a position as pre-synaptic variable in any of the Synapse objects.

# ANOTHER NOTE ABOUT fire_count variable: In the on_post_argument when I am incrementing fire_count I am dividing 1 by N_incoming.
# The reason for that is, when because of the definition of Brian's on_post argument, it will increment the value for every synapse_obj that is connected to post-synaptic neuron.
# Let's say there are 5 synapses connected to a post-synaptic neuron. If I define " fire_count += 1 " in on_post argument, it WILL NOT increment fire_count value by 1.
# Instead of that it will increment it by 5, but I want to increment it by 1. So I divided 1 by N_incoming so that in the end variable will be incremented by 1.
