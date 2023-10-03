from brian2 import *

# Simulation run time
# If u want to run simulation for 100 second please select runtime as 101 ms so code can draw the situation at 100 ms.
run_time = 501 * ms

run_counter = 0

number_of_runs = 3

selected_synapses = {}

termination_condition = False

# Initializing variables.
# threshold represents threshold value for post-synaptic neuron.
threshold = 15 / 1000

# beta
beta = 0.91

# tau represents RC time constant.
tau = 50 * ms

# t_max represents dendritic distance between synapse and soma.
t_max = 1 * ms

# dirac represents axonal propagation t between the pre-synaptic neuron and synapse.
dirac = 1 * ms

# fraction represents how much of the pool will be taken. (Takes values between 0 and 1).
# If fraction is 1, then it takes all the pool.
fraction = 0.8

# delay represents how much t needs to pass until new synaptic weights become active after a spike arrives.
delay = 2 * ms

# Refractory period.
refractory_period = 2 * ms

# initial_weights represents initial synaptic weights.
initial_weights = 0

# Synaptic transmission probability
transmission_p = 1

# synaptic connection probability
syn_connection_prob = 1

# pool_capacity represents weight pool capacity of neuron
pool_capacity = 8

# firing_rate shows firing rate of active poisson neurons.
firing_rate = 100 * Hz

# initial_firing_rate represents the initial firing rate of Poisson group neurons
initial_firing_rate = 0 * Hz

# layer_count represents how many hidden layers will be in simulation.
# If layer count is 6 that means 5 hidden layers and 1 response layer.
# MUST BE EQUAL OR BIGGER THAN 2 !!!!
layer_count = 6

# neuron_count variable shows how many neurons will be in a layer_idx.
neuron_count = 100

# row count
ng_row_count = 10

# column count
ng_column_count = 10

# rf row count   (rf means receptive field)
rf_row_count = 5

# rf column count
rf_column_count = 5

# input shape make it 'A' or 'B' or 'C' or 'D'
input_shape = 'A'

# rf array will be used in weight updates
rf_array = []

# response shape 'RIGHT_HAND' or 'LEFT_HAND'
response_shape = 'RIGHT_HAND'

responses = {'RIGHT_HAND': [26, 36, 37, 38, 46, 47, 48, 56, 57, 58, 64, 65, 66, 67, 68],
             'LEFT_HAND': [23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63, 64, 65]}

inputs = {'A': [14, 23, 25, 33, 35, 43, 45, 52, 56, 62, 63, 64, 65, 66, 71, 77, 81, 87],
          'B': [12, 13, 14, 15, 16, 22, 27, 32, 37, 42, 43, 44, 45, 46, 47, 52, 57, 62, 67, 72, 77, 82, 83, 84, 85, 86],
          'C': [14, 15, 16, 23, 27, 32, 42, 52, 62, 73, 77, 84, 85, 86],
          'D': [12, 13, 14, 15, 22, 26, 32, 37, 42, 47, 52, 57, 62, 67, 72, 76, 82, 83, 84, 85]}


def create_dictionary():
    return {}


# Defining necessary equations and variables for Neuron Group object.
neuron_eqs = '''
dv/dt = -(v/(tau)) + total_current*Hz : 1 # Equation 1 from article.
w_pool : 1   # w_pool will be used for weight pool of neuron.
total_current : 1 # Represents total synaptic current from article.
fire_count : integer # This variable is used for finding out how many times a neuron produced a spike.
is_enabled : boolean # If flag value of a neuron is True, that means neuron can receive and produce spikes.
received_spike_count : integer
'''

# Defining necessary variables for Synapse object.
syn_eqs = '''  
w : 1 # w represents the weights.
spike_fired : boolean # Becomes true if pre-synaptic neuron fired a spike, variable is used to determine which synapse_obj transmitted the spike.
spike_time : second # Records the firing t.
is_selected : boolean # True if neuron is selected after pruning.
'''

# Defining necessary arguments to execute when a pre-synaptic spike is fired.
# spike_fired = True*is_enabled*(rand() < transmission_p)
# The line above provides us a way for saving spike times for only neurons that are enabled and transmitted
# (If there is a transmission probability).
# It works like following:
# Lets say a neuron fired spike, that means one_pre_arg will be activated for the synapse between pre and post
# synaptic neuron.
# spike_fired variable will only be True if the neuron is enabled and the random number which is created by rand()
# is smaller than transmission probability. If transmission probability is 1 it will always be true, so the condition
# for spike_fired to be true will only depend on if neuron is enabled or not.
# If spike_fired variable does not take "True" value at the end we do not save spike time for that spike.
# This way the neurons which are not enabled will not take spike. Also, we are able to add a mechanism for making
# spike transmission probabilistic.
on_pre_arg = '''
spike_fired = True*is_enabled
spike_time = t
'''

# Defining necessary arguments to execute when post-synaptic spike is fired.
on_post_arg = '''

'''
