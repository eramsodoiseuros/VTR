import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter

# Constants
EDGE_SIZE = 1 + 2 ** 64  # Edge size of the resulting image in pixels
ROUGHNESS_DELTA = 0.7  # Roughness delta, 0 < ds < 1 : smaller ds => smoother results
PERIODIC = True  # Set the boundary type

# Initialize heightmap with an array full of zeros
heightmap = np.zeros((EDGE_SIZE, EDGE_SIZE))


def calculate_average_fixed(d, i, j, v, offsets):
    """Calculate average for fixed boundaries."""
    n = d.shape[0]

    total, count = 0, 0
    for p, q in offsets:
        pp, qq = i + p * v, j + q * v
        if 0 <= pp < n and 0 <= qq < n:
            total += d[pp, qq]
            count += 1.0
    return total / count


def calculate_average_periodic(d, i, j, v, offsets):
    """Calculate average for periodic boundaries."""
    n = d.shape[0] - 1

    total = 0
    for p, q in offsets:
        total += d[(i + p * v) % n, (j + q * v) % n]
    return total / 4.0


def diamond_square_step(heightmap, size, roughness_delta, avg_func):
    """Apply diamond square step."""
    n = heightmap.shape[0]
    half_size = size // 2

    diamond_offsets = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    square_offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    # Diamond Step
    for i in range(half_size, n, size):
        for j in range(half_size, n, size):
            heightmap[i, j] = avg_func(heightmap, i, j, half_size, diamond_offsets) + random.uniform(-roughness_delta,
                                                                                                     roughness_delta)

    # Square Step, rows
    for i in range(half_size, n, size):
        for j in range(0, n, size):
            heightmap[i, j] = avg_func(heightmap, i, j, half_size, square_offsets) + random.uniform(-roughness_delta,
                                                                                                    roughness_delta)

    # Square Step, cols
    for i in range(0, n, size):
        for j in range(half_size, n, size):
            heightmap[i, j] = avg_func(heightmap, i, j, half_size, square_offsets) + random.uniform(-roughness_delta,
                                                                                                    roughness_delta)
def generate_heightmap(heightmap, edge_size, roughness_delta, is_periodic):
    """Generate heightmap using the Diamond-Square algorithm."""
    size, roughness = edge_size-1, 1.0
    avg_func = calculate_average_periodic if is_periodic else calculate_average_fixed
    while size > 1:
        diamond_square_step(heightmap, size, roughness, avg_func)

        size //= 2
        roughness *= roughness_delta

    return heightmap

def load_colormap(filename):
    """Load colormap from a file."""
    colormap = []
    try:
        for row in np.loadtxt(filename):
            colormap.append([row[0], row[1:4]])
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    return matplotlib.colors.LinearSegmentedColormap.from_list("geo-smooth", colormap)

# Create a colormap
colormap = load_colormap("geo-smooth.gpf")

if colormap is not None:
    # Generate the heightmap
    terrain = generate_heightmap(heightmap, EDGE_SIZE, ROUGHNESS_DELTA, PERIODIC)

    # Create an image using the colormap
    plt.figure(figsize=(EDGE_SIZE / 100, EDGE_SIZE / 100), dpi=100) # create n-by-n pixel fig
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    plt.imshow(terrain, cmap=colormap)

    plt.savefig("terrain.png")  # Save to file
    plt.show()                  # Show interactive

def plot_3D(heightmap, colormap):
    """Plot the terrain in 3D."""
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Get x, y coordinates from the indices of the heightmap
    x = np.arange(heightmap.shape[0])
    y = np.arange(heightmap.shape[1])
    X, Y = np.meshgrid(x, y)

    # Plot the surface
    surf = ax.plot_surface(X, Y, heightmap, cmap=colormap, linewidth=0, antialiased=False)

    # Add a color bar which maps values to colors
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

if colormap is not None:
    terrain = generate_heightmap(heightmap, EDGE_SIZE, ROUGHNESS_DELTA, PERIODIC)

    plot_3D(terrain, colormap)


def smooth_heightmap(heightmap, sigma):
    """Smooth the heightmap using a Gaussian filter."""
    return gaussian_filter(heightmap, sigma=sigma)


if colormap is not None:
    terrain = generate_heightmap(heightmap, EDGE_SIZE, ROUGHNESS_DELTA, PERIODIC)

    terrain_smoothed = smooth_heightmap(terrain, sigma=1)  # you can change sigma to increase or decrease the smoothing

    plot_3D(terrain_smoothed, colormap)