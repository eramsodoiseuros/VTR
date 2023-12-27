#to be run after generating heightmap with heightmap.py

import numpy as np
from PIL import Image

def generate_normals(heightmap):
    heightmap = np.array(heightmap)
    height, width = heightmap.shape

    # Calculate the surface normals using the central difference method
    dx = np.gradient(heightmap, axis=1)
    dy = np.gradient(heightmap, axis=0)

    # Create an empty normals image
    normals = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Calculate the surface normal vector
            normal = np.array([-dx[y, x], -dy[y, x], 1.0])
            normal /= np.linalg.norm(normal)  # Normalize the normal vector
            normal = (normal + 1.0) * 0.5  # Map the normal vector to the range [0, 1]
            normals[y, x] = (normal * 255.0).astype(np.uint8)

    return normals

# Example usage:
heightmap_image = Image.open('../textures/heightmap.jpg').convert('L')
heightmap = np.array(heightmap_image)
normals = generate_normals(heightmap)

# Save the normals image
normals_image = Image.fromarray(normals, mode='RGB')
normals_image.save('../textures/heightmap_normals.jpg')
