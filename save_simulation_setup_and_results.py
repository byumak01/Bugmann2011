import matplotlib.pyplot as plt

import eqs_and_variables as ev
from brian2 import *
import os


def plot_graph(figure_num, layer_mon, layer_idx, neuron_idx, graphs_folder):
    plt.figure(figure_num)
    plt.plot(layer_mon[layer_idx].t / ms, layer_mon[layer_idx].v[neuron_idx], label='v', color='b')
    plt.plot(layer_mon[layer_idx].t / ms, (layer_mon[layer_idx].total_current[neuron_idx]) / 1000,
             label='current', color='r', linestyle='dashed')
    plt.title(f"Voltage Graph of {neuron_idx}. of {layer_idx + 1}. layer")
    plt.axhline(y=ev.threshold, color='y', linestyle='--', label=f'Threshold level')
    xlabel('Time (ms)')
    ylabel('v (volt)')
    legend()
    save_path = os.path.join(graphs_folder, f'layer{layer_idx + 1}_neuron{neuron_idx}.png')
    plt.savefig(save_path)
    return figure_num + 1


def draw_neuron_state_graphs(folder_path, layer_mon, layers):
    graphs_folder = os.path.join(folder_path, 'GRAPHS')
    os.makedirs(graphs_folder, exist_ok=True)
    figure_num = 0
    for layer_idx in range(ev.layer_count):
        for neuron_idx in range(ev.neuron_count):
            if layers[layer_idx].v[neuron_idx] != 0:
                figure_num = plot_graph(figure_num, layer_mon, layer_idx, neuron_idx, graphs_folder)


def save_simulation_setup_and_results(folder_path, execution_time):
    file_path = f"{folder_path}/used_setup_and_results.txt"
    with open(file_path, "w") as file:
        file.write(f"Run t of simulation: {ev.run_time}\n")
        file.write(f"Execution t of simulation: {execution_time}\n")
        file.write("\n")
        file.write("USED SETUP:\n")
        file.write(f"neuron count per layer: {ev.neuron_count}\n")
        file.write(f"layout of neurons: {ev.ng_row_count} x {ev.ng_column_count}\n")
        file.write(f"layout of receptive fields: {ev.rf_row_count} x {ev.rf_column_count}\n")
        file.write(f"hidden layer count: {ev.layer_count - 1}\n")
        file.write(f"input shape: {ev.input_shape}\n")
        file.write(f"response shape: {ev.response_shape}\n")
        file.write("\n")
        file.write("USED VARIABLES:\n")
        file.write("Explanation about variables are given at the bottom of file.\n")
        file.write("\n")
        file.write(f"Threshold: {ev.threshold} volt\n")
        file.write(f"Beta: {ev.beta}\n")
        file.write(f"Delay: {ev.delay}\n")
        file.write(f"Refractory period: {ev.refractory_period}\n")
        file.write(f"Tau: {ev.tau}\n")
        file.write(f"t_max: {ev.t_max}\n")
        file.write(f"dirac: {ev.dirac}\n")
        file.write(f"fraction: {ev.fraction}\n")
        file.write(f"pool capacity: {ev.pool_capacity}\n")
        file.write(f"Initial weights of synapses: {ev.initial_weights}\n")
        file.write(f"Synaptic transmission probability: {ev.transmission_p}\n")
        file.write(f"Synaptic connection probability: {ev.syn_connection_prob}\n")
        file.write(f"Firing rate of active poisson neurons: {ev.firing_rate}\n")
        file.write("\n\n")
        file.write("EXPLANATION ABOUT VARIABLES: \n")
        file.write("Threshold is multiplied by beta for threshold reset.\n")
        file.write("Delay represents how much t after new weights becomes effective after a spike is received.\n")
        file.write("t_max represents dendritic distance between the synapse and the soma.\n")
        file.write("dirac represents axonal propagation t between pre-synaptic neuron and synapse.\n")
        file.write("fraction shows how much of the pool will be given to the synapse which transmitted a spike.\n")
        file.write(
            "pool capacity shows how much weight a neuron has its disposal at the beginning of the simulation.\n")
