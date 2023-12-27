#version 440

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec3 fragmentPosition[];
in vec3 fragmentNormal[];

out vec3 geomPosition;
out vec3 geomNormal;

void main() {
    for (int i = 0; i < 3; ++i) {
        gl_Position = gl_in[i].gl_Position;
        geomPosition = fragmentPosition[i];
        geomNormal = fragmentNormal[i];
        geomHeight = fragmentHeight[i];
        EmitVertex();
    }
    EndPrimitive();
}
