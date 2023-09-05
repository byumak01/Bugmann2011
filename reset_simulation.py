def reset_simulation(layers, weight_delay, spike_times):
    weight_delay.clear()
    spike_times.clear()
    for i in range(len(layers)):
        layers[i].v = 0
        layers[i].fire_count = 0
