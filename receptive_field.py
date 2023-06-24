# The functions that are used for defining receptive fields are defined here.

# get_1d_indices function transforms a 2D to index to 1D index.
def get_1d_indices(neuron_2d_indices, ng_row_count):
    return [(pre_row_idx * ng_row_count) + pre_col_idx for pre_row_idx, pre_col_idx in neuron_2d_indices]


# get_2d_indices function transforms a 1D to index to 2D index.
def get_2d_indices(neuron_idx, ng_row_count, ng_column_count):
    neuron_row_idx = neuron_idx // ng_row_count
    neuron_col_idx = neuron_idx % ng_column_count
    return neuron_row_idx, neuron_col_idx


# find_rf_neurons function finds the indices of pre-synaptic neurons which are in the receptive field
# of given-post synaptic neuron, then returns their indices as 2D.
def find_rf_neurons(post_neuron_row_idx, post_neuron_col_idx, row_range, col_range, ng_row_count,
                    ng_column_count):
    return [(post_neuron_row_idx - row_iter, post_neuron_col_idx - col_iter)
            for row_iter in range(-row_range, row_range + 1)
            for col_iter in range(-col_range, col_range + 1)
            # if condition checks whether results are valid or not.
            if 0 <= (post_neuron_row_idx - row_iter) < ng_row_count
            and 0 <= (post_neuron_col_idx - col_iter) < ng_column_count]


# get_2d_indices_of_rf neurons function will transform given 1D post-synaptic neuron index to 2D then will call
# find_rf_neurons to get 2D indices for pre-synaptic neurons.
def get_2d_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count, rf_column_count):
    post_neuron_row_idx, post_neuron_col_idx = get_2d_indices(post_neuron_idx, ng_row_count, ng_column_count)

    row_range = rf_row_count // 2
    col_range = rf_column_count // 2
    pre_neuron_2d_indices = find_rf_neurons(post_neuron_row_idx, post_neuron_col_idx, row_range, col_range,
                                            ng_row_count, ng_column_count)

    return pre_neuron_2d_indices


# get_indices_of_rf_neurons function will call some functions and return the indexes of pre-synaptic neurons which are
# in the receptive field of given post-synaptic neuron.
def get_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count, rf_column_count):
    indices_of_rf_neurons_2d = get_2d_indices_of_rf_neurons(post_neuron_idx, ng_row_count, ng_column_count, rf_row_count,
                                                            rf_column_count)

    # transforming 2d indices to 1d then returning it.
    return get_1d_indices(indices_of_rf_neurons_2d, ng_row_count)
