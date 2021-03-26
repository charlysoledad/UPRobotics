import sys
from ctypes import *
from logging import getLogger
from textwrap import dedent
from typing import *

from OpenGL.GL import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

logger = getLogger(__name__)


def ctype_array(type: Type, elements):
    array_type: Type = type * len(elements)
    return array_type(*elements)


position = ctype_array(c_float, [
    0.0,0.0, 1.0,0.0, 0.5,1.0,
    0.0,0.0, -1.0,-0.0, -0.5,-1.0,
])

color = ctype_array(c_float, [
    1.0,0.0,0.0, 0.0,1.0,0.0, 0.0,0.0,1.0,
    0.5,0.5,0.0, 0.0,0.5,0.5, 0.5,0.0,0.5,
])

vertex = dedent('''\
    #version 130
    
    in vec2 vPosition;
    in vec3 vColor;
    
    out vec3 ffColor;
    
    void main() {
        gl_Position = vec4(vPosition, 0, 1);
        ffColor = vColor;
    }
''')

fragment = dedent('''\
    #version 130
    
    in vec3 ffColor;
    out vec4 fColor;
    
    void main() {
        fColor = vec4(ffColor, 1);
    }
''')

bindings = (
    ('vPosition', 2, position),
    ('vColor', 3, color),
)


class MyGLWidget(QOpenGLWindow):

    def __init__(self, *args):
        super().__init__(*args)

        # Indicate that the window is to be used for OpenGL rendering and not for rendering raster content with QPainter
        self.setSurfaceType(QWindow.OpenGLSurface)

        self.ctx: QOpenGLContext = None

    def initializeGL(self):
        print('initializeGL()')

        self.makeCurrent()
        self.ctx: QOpenGLContext = self.context()

        program_id = glCreateProgram()
        print(f'Created program id={program_id}')

        for name, type_, source in (
                ('Vertex', GL_VERTEX_SHADER, vertex),
                ('Fragment', GL_FRAGMENT_SHADER, fragment),
        ):
            shader_id = glCreateShader(type_)
            print(f'Created {name} shader id={shader_id}')
            glShaderSource(shader_id, source)
            glCompileShader(shader_id)
            assert glGetShaderiv(shader_id, GL_COMPILE_STATUS), \
                f'{name} Shader compilation failed:\n{glGetShaderInfoLog(shader_id).decode()}'
            glAttachShader(program_id, shader_id)

        glLinkProgram(program_id)
        assert glGetProgramiv(program_id, GL_LINK_STATUS), \
            f'Shader link failed:\n{glGetProgramInfoLog(program_id).decode()}'

        glUseProgram(program_id)

        vao = glGenVertexArrays(1)
        print(f'Created vertex attribute object id={vao}')
        glBindVertexArray(vao)

        for name, elements_per_vertex, data in bindings:
            vbo = glGenBuffers(1)
            print(f'Created vertex buffer for {name!r}; object id={vbo}')
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)

            attribute_id = glGetAttribLocation(program_id, name)
            print(f'Location of {name!r} = {attribute_id}')
            assert attribute_id >= 0, 'Attribute `{name}` is not defined??!?'
            glVertexAttribPointer(attribute_id, elements_per_vertex, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(attribute_id)

            # ^ Notice that the last parameter of `glVertexAttribPointer` is None instead of 0.
            # Under ctypes, pointer arguments handle None and zero are handled differently.
            # None becomes a void pointer; zero likely becomes a pointer to the value 0.
            # (https://stackoverflow.com/questions/43539610#43541948)

    def paintGL(self):
        print('paintGL()')
        self.makeCurrent()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, 6)

        glFlush()

        if self.isExposed():
            print('swapping')
            self.ctx.swapBuffers(self)
        else:
            print('not swapping: not yet exposed')

    def resizeGL(self, w: int, h: int):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyGLWidget()
    window.resize(800, 600)
    window.setTitle('asdf')
    window.show()

    logger.info("entering main loop")
    sys.exit(app.exec_())