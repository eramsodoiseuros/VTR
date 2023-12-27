#version 440

uniform mat4 projectionViewModel;
uniform mat3 normalMatrix;
uniform vec3 lightDirection;
uniform mat4 viewMatrix;
uniform mat4 viewModel;

in vec4 position;
in vec3 normal;
in vec2 texCoord0;

out vec4 eye;
out vec2 tc;
out vec3 fragNormal;
out vec3 fragPosition;
out vec3 fragLightDirection;

void main() {
    gl_Position = projectionViewModel * position;
    
    eye = -(viewModel * position);
    tc = texCoord0;
    fragNormal = normalize(normalMatrix * normal);
    fragPosition = vec3(position);

    vec4 lightDirViewSpace = viewMatrix * vec4(lightDirection, 0.0);
    fragLightDirection = normalize(-lightDirViewSpace.xyz);
}
