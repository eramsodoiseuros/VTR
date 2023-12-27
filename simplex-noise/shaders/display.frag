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
    float snowThreshold = 15.0; // Adjust this value to control the snow coverage

    // Sample the grass texture
    vec4 grassColor = texture(terrainTexture, tc);

    // Sample the snow texture
    vec4 snowColor = texture(snowTexture, tc);

    // Calculate lighting intensity
    vec3 surfaceNormal = normalize(fragNormal);
    float lightIntensity = dot(surfaceNormal, fragLightDirection);

    // Displace the vertex position along the normal direction based on the height
    vec3 displacedPosition = fragPosition + surfaceNormal * fragPosition.y;

    // Check if the displaced height of the terrain is above the snow threshold
    if (displacedPosition.y >= snowThreshold) {
        // Use snow texture for high terrain
        fragmentColor = vec4(snowColor.rgb * lightIntensity, snowColor.a);
    } else {
        // Use grass texture for low terrain
        fragmentColor = vec4(grassColor.rgb * lightIntensity, grassColor.a);
    }
}

