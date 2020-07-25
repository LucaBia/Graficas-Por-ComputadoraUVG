# Gian Luca Rivera - 18049

# https://docs.python.org/3/library/struct.html
import struct
from obj import Obj

# Format characters
# 1 byte
def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def short(s):
    return struct.pack('=h', s)

# 4 bytes
def longc(l):
    return struct.pack('=l', l)

def color(r, g, b):
    return bytes([b, g, r])


BLACK = color(0,0,0)
LIGHT_GREEN = color(128,255,0)


class Render(object):
    # glInit()
    def __init__(self, width, height):
        self.glCreateWindow(width, height)
        self.bitmap_color = BLACK
        self.pixel_color = LIGHT_GREEN
        self.glClear()

    # Llena el mapa de bits con un solo color
    def glClear(self):
        self.pixels = [[self.bitmap_color for x in range(self.width)] for y in range(self.height)]
    
    # Cambia el color con el que funciona glClear
    def glClearColor(self, r, g, b):
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)
        self.bitmap_color = color(red, green, blue)

    # Inicializacion del tamaño del framebuffer
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
    
    # Define el area de la imagen en donde se puede dibujar
    def glViewPort(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.viewPortX = x
        self.viewPortY = y

    # Cambia el color de un punto en la pantalla
    def glVertex(self, x, y):
        # funciones obtenidas de https://www.khronos.org/registry/OpenGL-Refpages/es2.0/xhtml/glViewport.xml
        # (+1)(width/2)+x
        vertexX = int((x+1)*(self.viewPortWidth/2)+self.viewPortX)
        # (+1)(height/2)+y
        vertexY = int((y+1)*(self.viewPortHeight/2)+self.viewPortY)
        self.pixels[vertexY][vertexX] = self.pixel_color

    # Cambia el color de una linea en la pantalla
    def glVertexCoord(self, x, y):
        self.pixels[y][x] = self.pixel_color

    # Cambia el color con el que funciona glVertex()
    def glColor(self, r, g, b):
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)
        self.pixel_color = color(red, green, blue)
    
    # Escribe el archivo de imagen
    def glFinish(self, filename):
        document = open(filename, 'wb')

        # Estructura de un bmp file obtenido de https://itnext.io/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393
        # File header
        document.write(bytes('B'.encode('ascii')))
        document.write(bytes('M'.encode('ascii')))
        document.write(longc(14 + 40 + self.width * self.height * 3))
        document.write(longc(0))
        document.write(longc(14 + 40))

        # Image information
        document.write(longc(40))
        document.write(longc(self.width))
        document.write(longc(self.height))
        document.write(short(1))
        document.write(short(24))
        document.write(longc(0))
        document.write(longc(self.width * self.height * 3))
        document.write(longc(0))
        document.write(longc(0))
        document.write(longc(0))
        document.write(longc(0))

        # Raw pixel data
        for x in range(self.height):
            for y in range(self.width):
                document.write(self.pixels[x][y])

        document.close()

    # Algortimo de Bresenham
    def glLine(self, x0, y0, x1, y1):
        # NDC a pixeles
        x0 = int((x0 + 1) * (self.viewPortWidth/2) + self.viewPortX)
        x1 = int((x1 + 1) * (self.viewPortWidth/2) + self.viewPortX)
        y0 = int((y0 + 1) * (self.viewPortHeight/2) + self.viewPortY)
        y1 = int((y1 + 1) * (self.viewPortHeight/2) + self.viewPortY)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # inclinacion
        inclination = dy > dx

        # si la diferencia en y es mayor a la diferencia en x (mayor a 45º), se recalcula la pendiente
        # de manera que x tenga los valores de Y y viceversa
        if inclination:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        limit = 0.5

        m = dy/dx
        y = y0

        # Dibujo
        for x in range(x0, x1+1):
            if inclination:
                self.glVertexCoord(y, x)
            else:
                self.glVertexCoord(x, y)

            offset += m

            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glLineCoord(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # inclinacion
        inclination = dy > dx

        # si la diferencia en y es mayor a la diferencia en x (mayor a 45º), se recalcula la pendiente
        # de manera que x tenga los valores de Y y viceversa
        if inclination:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        limit = 0.5

        # Si hay una division entre cero, se ignora
        try:
            m = dy/dx
        except ZeroDivisionError:
            pass
        else:
            y = y0

            for x in range(x0, x1+1):
                if inclination:
                    self.glVertexCoord(y, x)
                else:
                    self.glVertexCoord(x, y)

                offset += m

                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1

    #  Modelo OBJ
    def loadObjModel(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vertCount = len(face)

            for vert in range(vertCount):
                v0 = model.vertices[face[vert][0]-1]
                v1 = model.vertices[face[(vert + 1) % vertCount][0] - 1]

                x0 = round(v0[0] * scale[0]  + translate[0])
                y0 = round(v0[1] * scale[1]  + translate[1])
                x1 = round(v1[0] * scale[0]  + translate[0])
                y1 = round(v1[1] * scale[1]  + translate[1])

                self.glLineCoord(x0, y0, x1, y1)