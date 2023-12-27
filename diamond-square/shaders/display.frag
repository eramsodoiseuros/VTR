#version 440

uniform sampler2D terrainTexture;
uniform sampler2D snowTexture;

in vec4 eye;
in vec2 tc;
in vec3 fragNormal;
in vec3 fragPosition;
in vec3 fragLightDirection;

out vec4 fragmentColor;

void main() {
    // Determine the height threshold for snow
    float snowThreshold = 1.9; // Adjust this value to control the snow coverage

    // Sample the grass texture
    vec4 grassColor = texture(terrainTexture, tc);

    // Sample the snow texture
    vec4 snowColor = texture(snowTexture, tc);

    // Calculate lighting intensity
    vec3 surfaceNormal = normalize(fragNormal);
    float lightIntensity = dot(surfaceNormal, fragLightDirection);

    // Check if the height of the terrain is above the snow threshold
    if (fragPosition.y >= snowThreshold) {
        // Use snow texture for high terrain
        fragmentColor = vec4(snowColor.rgb * lightIntensity, snowColor.a);
    } else {
        // Use grass texture for low terrain
        fragmentColor = vec4(grassColor.rgb * lightIntensity, grassColor.a);
    }
}
