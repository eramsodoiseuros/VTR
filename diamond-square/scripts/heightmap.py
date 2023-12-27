import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image

# Define the size of the heightmap
size = 129  # Must be a power of 2 plus 1
roughness = 0.7
smoothing_sigma = 1.0

# Create a numpy array to store the height values
heightmap = np.zeros((size, size), dtype=np.float32)

# Initialize the four corners with random values
heightmap[0, 0] = np.random.uniform(0, 1)
heightmap[0, size - 1] = np.random.uniform(0, 1)
heightmap[size - 1, 0] = np.random.uniform(0, 1)
heightmap[size - 1, size - 1] = np.random.uniform(0, 1)

# Perform the Diamond-Square algorithm
step = size - 1
scale = 1.0
while step > 1:
    half = step // 2

    # Diamond step
    for y in range(half, size - 1, step):
        for x in range(half, size - 1, step):
            average = (heightmap[y - half, x - half] +
                       heightmap[y - half, x + half] +
                       heightmap[y + half, x - half] +
                       heightmap[y + half, x + half]) / 4.0
            heightmap[y, x] = average + np.random.uniform(-roughness, roughness) * scale

    # Square step
    for y in range(0, size, half):
        for x in range((y + half) % step, size, step):
            average = (heightmap[(y - half) % size, x] +
                       heightmap[(y + half) % size, x] +
                       heightmap[y, (x - half) % size] +
                       heightmap[y, (x + half) % size]) / 4.0
            heightmap[y, x] = average + np.random.uniform(-roughness, roughness) * scale

    step //= 2
    scale *= roughness

# Normalize the height values to the range [0, 1]
heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))

# Smooth the heightmap using a Gaussian filter
smoothed_heightmap = gaussian_filter(heightmap, sigma=smoothing_sigma)

# Convert the smoothed heightmap to a grayscale image
image = Image.fromarray((smoothed_heightmap * 255).astype(np.uint8), mode="L")

# Save the image as a heightmap file
image.save("../textures/heightmap.png")