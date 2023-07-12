from PIL import Image, ImageDraw, ImageFont
import receptive_field as rf
import eqs_and_variables as ev
from brian2 import *

width = 15 * ev.layer_count * ev.ng_column_count
height = 21 * ev.ng_row_count + 70

image = Image.new('RGBA', (width, height), 'black')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 16)


# reset_board function resets the board so that we can draw the current state.
def reset_board():
    draw.rectangle([(0, 0), ((width), (height))], fill='black')


# draw_recruited_neuron function makes recruited neurons red.
def draw_recruited_neurons(voltage, neuron_idx, layer_idx, flag):
    x1, y1, x2, y2 = get_coordinates(voltage, neuron_idx, layer_idx, flag)
    draw.rectangle([(x1, y1), (x2, y2)], fill='red')


def get_voltage_rate(voltage):
    voltage = voltage * 5 / 0.015
    if voltage >= 5:
        return 5
    elif 5 > voltage >= 4.70:
        return 4
    elif 4.70 > voltage >= 4.55:
        return 3
    elif 4.55 > voltage >= 4:
        return 2
    elif 4 > voltage > 0:
        return 1
    else:
        return 0


# draw_enabled_neurons function will make enabled neurons white.
def draw_enabled_neurons(layers):
    for layer_obj in layers:
        layer_idx = layers.index(layer_obj)
        for neuron_idx in range(len(layer_obj.flag)):
            flag = layer_obj.flag[neuron_idx]
            if flag:
                draw_current_state(5, neuron_idx, layer_idx, 'white', True)
            else:
                draw_current_state(5, neuron_idx, layer_idx, 'black', True)


# get_coordinates function will return coordinates for squares which are presenting neurons.
def get_coordinates(voltage, neuron_idx, layer_idx, flag):
    neuron_row, neuron_col = rf.get_2d_indices(neuron_idx, ev.ng_row_count, ev.ng_column_count)

    row_start_position = 10 * ev.ng_row_count + 55 if flag else 25
    x1 = layer_idx * (10 * ev.ng_column_count + 30) + (10 * neuron_col + 5 - voltage) + 10
    y1 = row_start_position + (10 * neuron_row + 5 - voltage)
    x2 = layer_idx * (10 * ev.ng_column_count + 30) + (10 * (neuron_col + 1) - 5 + voltage) + 10
    y2 = row_start_position + (10 * (neuron_row + 1) - 5 + voltage)

    return x1, y1, x2, y2


def draw_current_state(voltage, neuron_idx, layer_idx, color, flag):
    voltage = get_voltage_rate(voltage)
    x1, y1, x2, y2 = get_coordinates(voltage, neuron_idx, layer_idx + 1, flag)
    draw_voltage_level(x1, y1, x2, y2, color)
    draw_recruited_neurons(5, neuron_idx, layer_idx + 1, True) if voltage > 0 and flag == False else None


def draw_voltage_level(x1, y1, x2, y2, color):
    draw.rectangle([(x1, y1), (x2, y2)], fill=f'{color}')


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

    draw.text((x1 + 15, y1 - 25), layer_name, fill='white', font=font)


def print_time(t, x1, y1):
    draw.text((x1 + 20, y1 + 30), f"t = {t/ms} ms", font=font, fill='white')


def draw_outlines_layer_names_and_time(t, folder_path):
    for layer_idx in range(ev.layer_count + 1):
        for neuron_idx in range(ev.neuron_count):
            x1, y1, x2, y2 = get_coordinates(5, neuron_idx, layer_idx, False)
            draw.rectangle([(x1, y1), (x2, y2)], outline='gray')
            print_layer_names(x1, y1, layer_idx, False) if neuron_idx == 0 else None

            x1, y1, x2, y2 = get_coordinates(5, neuron_idx, layer_idx, True)
            print_time(t, x1, y1) if neuron_idx == 0 and layer_idx == 0 else None
            draw.rectangle([(x1, y1), (x2, y2)], outline='gray') if layer_idx != 0 else None
            print_layer_names(x1, y1, layer_idx, True) if layer_idx != 0 and neuron_idx == 0 else None

    image_name = f"{folder_path}/{t / ms}.png"
    image.save(image_name, "PNG")
