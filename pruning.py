import eqs_and_variables as ev
import draw


def selected_synapses_after_pruning():
    return {}


# STIMULUS ILE LAYER 1 ARASINDA PRUNING YOOK LAYER 5 RESPONSE ARASINDA DA PRUNING YOK
def add_key(layer_obj_idx, neuron_idx, selected_synapses):
    key = (layer_obj_idx, neuron_idx)
    selected_synapses[key] = None


def add_synapse_idx(layer_obj_idx, neuron_idx, selected_synapses, selected_synapse_idx):
    key = (layer_obj_idx, neuron_idx)
    selected_synapses[key] = selected_synapse_idx


# spesifik bir norondan cikan butun agirliklari yazdir yaptigi secimi kontrol et
#
# find_synapse_with_the_lowest_weight function finds synapse with the lowest weight outgoing from a neuron, for every
# neuron in a layer.
def find_synapse_with_the_lowest_weight(syn_obj_idx, syn_obj):
    selected_synapses = selected_synapses_after_pruning()

    min_w = ev.pool_capacity + 1
    syn_idx_with_min_w = None

    for idx in range(len(syn_obj.w)):
        pre_idx = syn_obj.i[idx]
        prev_pre_idx = syn_obj.i[idx - 1] if idx != 0 else -1

        if pre_idx == prev_pre_idx or prev_pre_idx == -1:
            if syn_obj.w[idx] < min_w:
                if syn_obj.w[idx] != 0:
                    min_w = syn_obj.w[idx]
                    syn_idx_with_min_w = idx
        else:
            add_key(syn_obj_idx - 1, pre_idx, selected_synapses)
            add_synapse_idx(syn_obj_idx - 1, pre_idx, selected_synapses, syn_idx_with_min_w)

            min_w = syn_obj.w[idx]
            syn_idx_with_min_w = idx

            # sonda tek bir sinapsa bagli tek bir noron kaldiysa diye onlem
            add_key(syn_obj_idx - 1, pre_idx, selected_synapses) if idx == len(syn_obj.w) - 1 else None
            add_synapse_idx(syn_obj_idx - 1, pre_idx, selected_synapses, syn_idx_with_min_w) if idx == len(
                syn_obj.w) - 1 else None

    return selected_synapses


def give_weights_back_to_the_pool(obj_idx, layer_obj, syn_obj, selected_synapses):

    synapses_with_min_weight = set()
    for key in selected_synapses:
        if key[0] == obj_idx - 1:
            synapses_with_min_weight.add(selected_synapses[key])

    for syn_idx in range(len(syn_obj.w)):
        if syn_idx not in synapses_with_min_weight:
            post_idx = syn_obj.j[syn_idx]

            layer_obj.w_pool[post_idx] += syn_obj.w[syn_idx]
            syn_obj.w[syn_idx] = 0


def pruning(layers, synapse_objects, folder_path):
    len_syn_objects = len(synapse_objects)

    for idx in range(0, len_syn_objects - 1):
        selected_synapses = find_synapse_with_the_lowest_weight(idx, synapse_objects[idx])
        give_weights_back_to_the_pool(idx, layers[idx], synapse_objects[idx], selected_synapses)
