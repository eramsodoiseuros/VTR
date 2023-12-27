#version 440

layout (points) in;
layout (points, max_vertices = 1) out;

uniform float roughness;
uniform float heightScale;

in vec4 fragPosition[];
in vec3 fragNormal[];

out vec4 outPosition;
out vec3 outNormal;

const int TerrainSize = 512; // Adjust this based on the desired size of the terrain

float terrainHeights[TerrainSize][TerrainSize]; // 2D array to store terrain heights

void initializeTerrain()
{
    // Set initial terrain heights (e.g., initialize to 0)
    for (int i = 0; i < TerrainSize; ++i)
    {
        for (int j = 0; j < TerrainSize; ++j)
        {
            terrainHeights[i][j] = 0.0;
        }
    }
}

float getTerrainHeight(int x, int z)
{
    // Retrieve the terrain height at the given (x, z) coordinates
    return terrainHeights[x][z];
}

void setTerrainHeight(int x, int z, float height)
{
    // Set the terrain height at the given (x, z) coordinates
    terrainHeights[x][z] = height;
}

float random(float min, float max)
{
    // Generate a random value between min and max
    return min + fract(sin(dot(vec2(gl_PrimitiveID, gl_PrimitiveID), vec2(12.9898, 78.233))) * 43758.5453) * (max - min);
}

void main()
{
    vec4 position = fragPosition[0];
    vec3 normal = fragNormal[0];

    float terrainSize = float(TerrainSize);
    int numIterations = int(log2(terrainSize - 1));

    initializeTerrain();

    // Perform the Diamond-Square algorithm
    for (int iteration = 1; iteration <= numIterations; iteration *= 2)
    {
        int halfStepSize = int(terrainSize / float(iteration));
        int stepSize = halfStepSize * 2;
        
        for (int x = halfStepSize; x < int(terrainSize); x += stepSize)
        {
            for (int z = halfStepSize; z < int(terrainSize); z += stepSize)
            {
                float averageHeight = (getTerrainHeight(x - halfStepSize, z - halfStepSize) +
                                       getTerrainHeight(x + halfStepSize, z - halfStepSize) +
                                       getTerrainHeight(x - halfStepSize, z + halfStepSize) +
                                       getTerrainHeight(x + halfStepSize, z + halfStepSize)) * 0.25;

                float randomOffset = random(-roughness, roughness);
                float newHeight = averageHeight + randomOffset * heightScale;

                setTerrainHeight(x, z, newHeight);
            }
        }
        
        // Diamond step
        for (int x = 0; x < int(terrainSize); x += halfStepSize)
        {
            for (int z = 0; z < int(terrainSize); z += halfStepSize)
            {
                float averageHeight = 0.0;
                int count = 0;
                
                if (x - halfStepSize >= 0)
                {
                    averageHeight += getTerrainHeight(x - halfStepSize, z);
                    ++count;
                }
                if (x + halfStepSize < int(terrainSize))
                {
                    averageHeight += getTerrainHeight(x + halfStepSize, z);
                    ++count;
                }
                if (z - halfStepSize >= 0)
                {
                    averageHeight += getTerrainHeight(x, z - halfStepSize);
                    ++count;
                }
                if (z + halfStepSize < int(terrainSize))
                {
                    averageHeight += getTerrainHeight(x, z + halfStepSize);
                    ++count;
                }

                averageHeight /= float(count);

                float randomOffset = random(-roughness, roughness);
                float newHeight = averageHeight + randomOffset * heightScale;

                setTerrainHeight(x, z, newHeight);
            }
        }
    }

    // Emit the generated point as output
    outPosition = position;
    outNormal = normal;
    EmitVertex();

    EndPrimitive();
}
