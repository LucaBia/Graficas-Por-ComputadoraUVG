# Gian Luca Rivera - 18049

# https://docs.python.org/3/library/struct.html
import struct

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
    def __init__(self, width, height, r, g, b):
        self.glCreateWindow(width, height)
        self.bitmap_color = BLACK
        self.pixel_color = LIGHT_GREEN
        self.glClearColor(r, g, b)
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
