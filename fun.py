import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

def generate_corin_gene_visualization(width=8, height=6, num_base_pairs=1000, line_width=0.5, line_color='blue', base_pair_spacing=0.3):
    """
    Generates a visual representation of the Corin gene, mimicking the stacked base pair effect.

    Args:
        width: Width of the gene representation.
        height: Height of the gene representation.
        num_base_pairs: Number of base pairs to generate.
        line_width: Width of the lines representing base pairs.
        line_color: Color of the lines.
        base_pair_spacing:  Spacing between base pairs.

    Returns:
        A matplotlib Figure and Axes object.
    """

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')  # Ensure equal aspect ratio
    ax.axis('off') # Turn off axis

    # Generate data for the base pairs
    x = np.arange(num_base_pairs) * (width / num_base_pairs) + (width - (width / num_base_pairs)) / 2  # positions
    y = np.zeros(num_base_pairs)

    # Draw base pairs as lines
    for i in range(num_base_pairs):
        ax.plot(x[i], y[i], linewidth=line_width, color=line_color)

    # Adjust spacing
    ax.set_xlim(0, width) #ensure the array is fully visible
    ax.set_ylim(0, height)

    return fig, ax


if __name__ == '__main__':
    fig, ax = generate_corin_gene_visualization(width=8, height=6, num_base_pairs=1000, line_width=0.5, line_color='blue', base_pair_spacing=0.3)
    plt.show()