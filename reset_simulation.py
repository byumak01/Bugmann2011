# THIS FUNCTION IS CALLED AFTER PRUNING, BEFORE START OF NEW RUN.
def reset_simulation(layers, weight_delay, spike_times):
    weight_delay.clear()
    spike_times.clear()
    for i in range(len(layers)):
        layers[i].v = 0
        layers[i].fire_count = 0
        layers[i].total_current = 0
