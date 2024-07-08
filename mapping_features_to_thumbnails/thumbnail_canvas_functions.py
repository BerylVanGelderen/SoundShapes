import cairo
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
from IPython.display import SVG

instrument_labels_list = ['i voice','i choir','i flute', 'i strings','i harp', 'i piano','i guitar','i drums', 'i synth']
# Remove the 'i ' prefix from each element
instrument_labels_list_without_prefix = [label[2:] if label.startswith('i ') else label for label in instrument_labels_list]

colormap_valence = mcolors.LinearSegmentedColormap.from_list(
    "valence",
    [(0.83, 0.05809999999999996, 0.13528999999999966),
     (0.8150599999999999, 0.8209922581951538, 0.83),
     (0.05809999999999996, 0.7379790989317234, 0.83)])

# Get the colormap
colormap_valence_function = plt.get_cmap(colormap_valence)

def get_color_from_cmap(value):
    # Ensure valence is within the bounds
    value = max(0.0, min(1.0, value))

    # Map valence to RGB using the colormap
    rgba = colormap_valence_function(value)
    # Convert to RGB tuple
    return rgba[:3]


def background_color(df_row, context, size=600):
    valence = df_row['spotify valence']
    red, green, blue = get_color_from_cmap(valence)
    context.set_source_rgb(red, green, blue)
    context.paint()
    # # Background color as a gradient
    # gradient = cairo.LinearGradient(0, 0, size, size)
    # gradient.add_color_stop_rgb(0, red, green, blue)
    # context.rectangle(0, 0, size, size)
    # context.set_source(gradient)
    # context.fill()

def setup_surface_init(context):
    # Set the background color
    context.set_source_rgb(1, 1, 1)
    context.paint()


# for debugging purposes for the radar chart
def draw_circular_grid(context, size, angles, radius):
    cx, cy = size / 2, size / 2
    for i in range(1, 5):
        context.set_line_width(1)
        context.set_source_rgb(0.8, 0.8, 0.8)
        for angle in angles:
            x = cx + radius * i / 4 * math.cos(angle)
            y = cy + radius * i / 4 * math.sin(angle)
            if angle == angles[0]:
                context.move_to(x, y)
            else:
                context.line_to(x, y)
        context.close_path()
        context.stroke()


def draw_labels(context, radius, angles, instrument_labels_list_without_prefix, size):
    cx, cy = size / 2, size / 2
    context.set_font_size(18)
    for i, label in enumerate(instrument_labels_list_without_prefix):
        angle = angles[i]
        x = cx + (radius + 20) * math.cos(angle)
        y = cy + (radius + 20) * math.sin(angle)
        if angle > math.pi / 2 and angle < 3 * math.pi / 2:
            x -= context.text_extents(label)[2]
        if angle > math.pi:
            y += context.text_extents(label)[3]
        context.move_to(x, y)
        context.set_source_rgb(0, 0, 0)
        context.show_text(label)


def logistic_scale(x, min_value, max_value, new_min, k=1):
    # k controls the steepness of the curve
    return new_min + (1 - new_min) / (1 + np.exp(-k * (x - min_value) / (max_value - min_value)))


def instrument_scaling(instrument_scores):
    new_min = 0.3
    logistic_scaling_factor = 42

    max_value = max(instrument_scores)
    min_value = min(instrument_scores)

    instrument_scores = [logistic_scale(score, min_value, max_value, 0,logistic_scaling_factor) for score in
                         instrument_scores]
    max_value = max(instrument_scores)
    min_value = min(instrument_scores)

    instrument_scores = [(score - min_value) * (1 - new_min) / (max_value - min_value) + new_min for score in
                         instrument_scores]
    return instrument_scores

def calculate_offset(cx, cy, radius, score, angle, line_width):
    # Calculate the offset radius
    offset_radius = radius * score - line_width / 2
    if offset_radius < 0:
        offset_radius = 0  # Prevent negative radius

    # Calculate the new x, y coordinates with the offset radius
    x = cx + offset_radius * math.cos(angle)
    y = cy + offset_radius * math.sin(angle)
    return x, y

def create_radar_chart(df_row, context, instrument_labels_list=instrument_labels_list,
                       instrument_labels_list_without_prefix=instrument_labels_list_without_prefix, size=600,
                       debug=False):
    WIDTH, HEIGHT = size, size

    instrument_scores = [df_row[label] for label in instrument_labels_list]
    instrument_scores = instrument_scaling(instrument_scores)

    # Number of variables
    num_vars = len(instrument_labels_list)
    angles = [(2 * math.pi * i / num_vars) - 0.5 * math.pi for i in range(num_vars)]

    # Set the center and radius
    cx, cy = WIDTH / 2, HEIGHT / 2
    radius = min(cx, cy) - 40

    if debug:
        radius = min(cx, cy) - 80
        draw_labels(context, radius, angles, instrument_labels_list_without_prefix, size)

    # Draw the data polygon
    # line width corresponds with energy
    line_width = df_row['energy'] * 79 + 1
    half_line_width = line_width / 2
    context.set_line_width(line_width)
    context.set_source_rgb(0, 0, 0)  # Black lines for the radar plot,for now
    context.move_to(cx + (radius-half_line_width) * instrument_scores[0] * math.cos(angles[0]),
                    cy + (radius-half_line_width) * instrument_scores[0] * math.sin(angles[0]))
    for i in range(1, num_vars):
        x = cx + (radius-half_line_width) * instrument_scores[i] * math.cos(angles[i])
        y = cy + (radius-half_line_width) * instrument_scores[i] * math.sin(angles[i])
        context.line_to(x, y)
    context.close_path()
    context.stroke_preserve()

    r, g, b = df_row['g rgb color']
    #context.set_source_rgba(0.95, 0.95, 0.95, 1)  # White fill for the radar plot, for now
    context.set_source_rgba(r,g,b,1)
    context.fill()

    # Draw the axes
    context.set_line_width(3)
    context.set_source_rgb(0.7, 0.7, 0.7)
    for i in range(0, num_vars):
        x = cx + (radius - half_line_width) * math.cos(angles[i]) * instrument_scores[i]
        y = cy + (radius - half_line_width)* math.sin(angles[i]) * instrument_scores[i]
        context.move_to(cx, cy)
        context.line_to(x, y)
        context.stroke()

    if debug:
       draw_circular_grid(context, size, angles, radius)


def create_thumbnail(df_row, dest_folder, size=600, display=False, debug=False):
    # Create a new surface and context
    WIDTH, HEIGHT = size, size

    if debug:
        dest_folder = f'{dest_folder}_debug'

    dest_folder = f'{dest_folder}_{size}px'
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    surface = cairo.SVGSurface(f"{dest_folder}/{df_row.name}.svg", WIDTH, HEIGHT)
    # Just in case, this is how you initialize a png:
    # surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)

    context = cairo.Context(surface)

    setup_surface_init(context)
    background_color(df_row, context, size=size)
    create_radar_chart(df_row, context, size=size, debug=debug)

    surface.finish()
    # this is how you would save a png:
    # surface.write_to_png(f"{dest_folder}/{df_row.name}.png")

    if display:
        return SVG(f"{dest_folder}/{df_row.name}.svg")
    return None