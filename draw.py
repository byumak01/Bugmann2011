from PIL import Image, ImageDraw, ImageFont
import receptive_field as rf
import eqs_and_variables as ev
from brian2 import *

width = 15 * ev.layer_count * ev.ng_column_count
height = 21 * ev.ng_row_count + 70

image = Image.new('RGBA', (width, height), 'black')
dr = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 16)


# reset_board function resets the board so that we can dr the current state.
def reset_board():
    dr.rectangle([(0, 0), ((width), (height))], fill='black')


# draw_recruited_neuron function makes recruited neurons red.
def draw_if_recruited(neuron_idx, layer_idx):
    state_of_neuron = get_state_of_neuron(ev.threshold)
    get_coordinates_and_draw(state_of_neuron, neuron_idx, layer_idx + 1, 'red', True)


def get_coordinates_and_draw(state_of_neuron, neuron_idx, layer_idx, color, if_lower_grid):
    x1, y1, x2, y2 = get_coordinates(state_of_neuron, neuron_idx, layer_idx, if_lower_grid)
    draw_given_coordinates(x1, y1, x2, y2, f"{color}")


def get_state_of_neuron(voltage):
    if voltage >= ev.threshold:
        return 5
    elif 0 < voltage < ev.threshold:
        return 1.5
    else:
        return 0


# draw_enabled_neurons function will make enabled neurons white.
def draw_enabled_neurons(layers):
    for layer_obj in layers:
        layer_idx = layers.index(layer_obj) + 1
        for neuron_idx in range(len(layer_obj.is_enabled)):
            enabled_flag_of_neuron = layer_obj.is_enabled[neuron_idx]
            color = 'white' if enabled_flag_of_neuron else 'black'
            get_coordinates_and_draw(5, neuron_idx, layer_idx, color, True)


# get_coordinates function will return coordinates for squares which are presenting neurons.
def get_coordinates(state_of_neuron, neuron_idx, layer_idx, if_lower_grid):
    # Get 2D indices of the neuron
    neuron_row, neuron_col = rf.get_2d_indices(neuron_idx, ev.ng_row_count, ev.ng_column_count)

    # Calculate row start position based on the lower or upper grid
    row_start_position = 10 * ev.ng_row_count + 60 if if_lower_grid else 25

    # Calculate x1, y1, x2, y2 coordinates
    column_offset = 10 * ev.ng_column_count + 20
    x1 = layer_idx * column_offset + (10 * neuron_col + 5 - state_of_neuron) + 10
    y1 = row_start_position + (10 * neuron_row + 5 - state_of_neuron)
    x2 = layer_idx * column_offset + (10 * (neuron_col + 1) - 5 + state_of_neuron) + 10
    y2 = row_start_position + (10 * (neuron_row + 1) - 5 + state_of_neuron)

    return x1, y1, x2, y2


def draw_neuron_activity(voltage, neuron_idx, layer_idx):
    state_of_neuron = get_state_of_neuron(voltage)
    get_coordinates_and_draw(state_of_neuron, neuron_idx, layer_idx + 1, 'white', False)


def draw_given_coordinates(x1, y1, x2, y2, color):
    dr.rectangle([(x1, y1), (x2, y2)], fill=f'{color}')


def get_layer_names_for_upper_grid(layer_idx):
    if layer_idx == 0:
        return "Stimulus"
    elif layer_idx == ev.layer_count:
        return "Response"
    else:
        return f"Layer {layer_idx}"


def get_layer_names_for_lower_grid(layer_idx):
    if layer_idx == ev.layer_count:
        return "Target_R"
    else:
        return f"Target {layer_idx}"


def print_layer_names(x1, y1, layer_idx, flag):
    if flag:
        layer_name = get_layer_names_for_lower_grid(layer_idx)
    else:
        layer_name = get_layer_names_for_upper_grid(layer_idx)

    dr.text((x1 + 15, y1 - 22), layer_name, fill='white', font=font)


def print_time(t, x1, y1):
    x_coord = x1 + 20
    y_coord = y1 + 30
    if t <= ev.run_time:
        dr.text((x_coord, y_coord), f"t = {round(t / ms, 2)} ms", font=font, fill='white')
    else:
        dr.text((x_coord, y_coord), f"PRUNING", font=font, fill='white')


def draw_active_neurons_in_stimulus_layer(active_poisson_neurons, if_pruning):
    fill = 5 if if_pruning else 1.5

    for idx in active_poisson_neurons:
        get_coordinates_and_draw(fill, idx, 0, 'white', False)


def draw_firing_neurons_in_stimulus_layer(firing_poisson_neurons):
    for idx in firing_poisson_neurons:
        get_coordinates_and_draw(5, idx, 0, 'white', False)


def draw_outlines_layer_names_and_time(t, folder_path, pruning, run_count):
    for layer_idx in range(ev.layer_count + 1):
        for neuron_idx in range(ev.neuron_count):
            # Draw outlines for the lower grid
            x1_lower, y1_lower, x2_lower, y2_lower = get_coordinates(5, neuron_idx, layer_idx, False)
            dr.rectangle([(x1_lower, y1_lower), (x2_lower, y2_lower)], outline='gray')
            print_layer_names(x1_lower, y1_lower, layer_idx, False) if neuron_idx == 0 else None

            # Draw outlines for the upper grid
            x1_upper, y1_upper, x2_upper, y2_upper = get_coordinates(5, neuron_idx, layer_idx, True)
            if neuron_idx == 0 and layer_idx == 0:
                print_time(t, x1_upper, y1_upper)
            elif layer_idx != 0:
                dr.rectangle([(x1_upper, y1_upper), (x2_upper, y2_upper)], outline='gray')
                if neuron_idx == 0:
                    print_layer_names(x1_upper, y1_upper, layer_idx, True)

    # Save the image
    label = t / ms if not pruning else f"pruning_{run_count + 1}"
    image_name = f"{folder_path}/{label}.png"
    image.save(image_name, "PNG")

