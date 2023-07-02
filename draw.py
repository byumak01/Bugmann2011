from PIL import Image, ImageDraw
import receptive_field as rf
import eqs_and_variables as ev

width = 15 * ev.layer_count + 1 * ev.ng_column_count
height = 20 * ev.ng_row_count + 25

image = Image.new('RGBA', (width, height), 'black')
draw = ImageDraw.Draw(image)


def reset_board():
    draw.rectangle([(0, 0), ((10 * ev.ng_row_count), (10 * ev.ng_column_count))], fill='black')


def draw_recruited_neurons(x1, y1, x2, y2):
    draw.rectangle([(x1, y1), (x2, y2)], fill='red')


def draw_enabled_neurons(layers):
    for layer_obj in layers:
        layer_idx = layers.index(layer_obj)
        for flag in layer_obj.flag:
            flag_list = layer_obj.flag
            neuron_idx = flag_list.index(flag)
            if flag:
                draw_current_state(5, neuron_idx, layer_idx, 'white', True)
            else:
                draw_current_state(5, neuron_idx, layer_idx, 'black', True)


def draw_current_state(voltage, neuron_idx, layer_idx, color, flag):
    neuron_row, neuron_col = rf.get_2d_indices(neuron_idx, ev.ng_row_count, ev.ng_column_count)

    row_start_position = 10 * ev.ng_row_count + 25 if flag else 5
    x1 = (layer_idx + 1) * (10 * ev.ng_column_count + 5) + (10 * neuron_col + 5 - voltage)
    y1 = row_start_position + (10 * neuron_row + 5 - voltage)
    x2 = (layer_idx + 1) * (10 * ev.ng_column_count + 5) + (10 * (neuron_col + 1) - 5 + voltage)
    y2 = row_start_position + (10 * (neuron_row + 1) - 5 + voltage)

    draw_voltage_level(x1, y1, x2, y2, color)
    draw_outlines(x1 - (5 - voltage), y1 - (5 - voltage), x2 + (5 - voltage), y2 + (5 - voltage))
    draw_recruited_neurons(x1 - (5 - voltage), y1 - (5 - voltage), x2 + (5 - voltage),
                           y2 + (5 - voltage)) if voltage > 0 else None
    image.save("test.png", "PNG")


def draw_voltage_level(x1, y1, x2, y2, color):
    draw.rectangle([(x1, y1), (x2, y2)], fill=color)


def draw_outlines(x1, y1, x2, y2):
    draw.rectangle([(x1, y1), (x2, y2)], outline='gray')


draw_current_state(1, 5, 2, 'white', False)
