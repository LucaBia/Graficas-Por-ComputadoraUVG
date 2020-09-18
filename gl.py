# Gian Luca Rivera - 18049

import struct
from obj import Obj
from mathLib import *

import numpy as np
from numpy import tan


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
    return bytes([int(b*255), int(g*255), int(r*255)])



BLACK = color(0,0,0)
WHITE = color(1,1,1)
LIGHT_GREEN = color(0.5,1,0)
pi = 3.141592653589793


class Raytracer(object):
    # glInit()
    def __init__(self, width, height):
        self.pixel_color = WHITE
        self.bitmap_color = BLACK
        self.glCreateWindow(width, height)

        self.camPosition = (0,0,0)
        self.fov = 60

        self.scene = []

        self.pointLight = None
        self.ambientLight = None

    # Inicializacion del tamaño del framebuffer
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewPort(0, 0, width, height)

    # Define el area de la imagen en donde se puede dibujar
    def glViewPort(self, x, y, width, height):
        self.viewPortX = x
        self.viewPortY = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    # Llena el mapa de bits con un solo color
    def glClear(self):
        self.pixels = [[self.bitmap_color for x in range(self.width)] for y in range(self.height)]
        self.zbuffer = [[float('inf') for x in range(self.width)] for y in range(self.height) ]

    # Cambia el color de un punto en la pantalla
    def glVertex(self, x, y, color = None):
        # funciones obtenidas de https://www.khronos.org/registry/OpenGL-Refpages/es2.0/xhtml/glViewport.xml
        # (+1)(width/2)+x
        vertexX = (x+1) * (self.viewPortWidth/2) + self.viewPortX
        # (+1)(height/2)+y
        vertexY = (y+1) * (self.viewPortHeight/2) + self.viewPortY
        try:
            self.pixels[vertexY][vertexX] = color or self.pixel_color
        except:
            pass

    # Cambia el color de una linea en la pantalla
    def glVertexCoord(self, x, y, color = None):
        if x < self.viewPortX or x >= self.viewPortX + self.viewPortWidth or y < self.viewPortY or y >= self.viewPortY + self.viewPortHeight:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.pixel_color
        except:
            pass

    # Cambia el color con el que funciona glVertex()
    def glColor(self, r, g, b):
        self.pixel_color = color(r, g, b)

    # Cambia el color con el que funciona glClear
    def glClearColor(self, r, g, b):
        self.bitmap_color = color(r, g, b)

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

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header compuesto por 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(longc(14 + 40 + self.width * self.height * 3))
        archivo.write(longc(0))
        archivo.write(longc(14 + 40))

        # Image Header compuesto por 40 bytes
        archivo.write(longc(40))
        archivo.write(longc(self.width))
        archivo.write(longc(self.height))
        archivo.write(short(1))
        archivo.write(short(24))
        archivo.write(longc(0))
        archivo.write(longc(self.width * self.height * 3))
        archivo.write(longc(0))
        archivo.write(longc(0))
        archivo.write(longc(0))
        archivo.write(longc(0))

        # Calculo del minimo y maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth,depth,depth))

        archivo.close()

    def rtRender(self):
        for y in range(self.height):
            for x in range(self.width):

                # conversion a NDC
                Px = 2 * ( (x+0.5) / self.width) - 1
                Py = 2 * ( (y+0.5) / self.height) - 1

                #FOV = angulo de vision
                t = tan( (self.fov * pi / 180) / 2 )
                r = t * self.width / self.height
                Px *= r
                Py *= t

                direction = (Px, Py, -1)
                direction = direction / frobeniusNorm(direction)

                material = None
                intersect = None

                for obj in self.scene:
                    hit = obj.ray_intersect(self.camPosition, direction)
                    if hit is not None:
                        if hit.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = hit.distance
                            material = obj.material
                            intersect = hit

                if intersect is not None:
                    self.glVertexCoord(x, y, self.pointColor(material, intersect))

    def pointColor(self, material, intersect):

        objectColor = [material.diffuse[2] / 255,
                       material.diffuse[1] / 255,
                       material.diffuse[0] / 255]

        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specColor = [0,0,0]

        shadow_intensity = 0

        if self.ambientLight:
            ambientColor = [self.ambientLight.strength * self.ambientLight.color[2] / 255,
                            self.ambientLight.strength * self.ambientLight.color[1] / 255,
                            self.ambientLight.strength * self.ambientLight.color[0] / 255]

        if self.pointLight:
            light_dir = subVectors(self.pointLight.position, intersect.point)
            light_dir = light_dir / frobeniusNorm(light_dir)

            intensity = self.pointLight.intensity * max(0, dotVectors(light_dir, intersect.normal))
            diffuseColor = [intensity * self.pointLight.color[2] / 255,
                            intensity * self.pointLight.color[1] / 255,
                            intensity * self.pointLight.color[2] / 255]

            view_dir = subVectors(self.camPosition, intersect.point)
            view_dir = view_dir / frobeniusNorm(view_dir)

            reflect = 2 * dotVectors(intersect.normal, light_dir)
            reflect = multiply(reflect, intersect.normal)
            reflect = subVectors(reflect, light_dir)

            spec_intensity = self.pointLight.intensity * (max(0, dotVectors(view_dir, reflect)) ** material.spec)

            specColor = [spec_intensity * self.pointLight.color[2] / 255,
                         spec_intensity * self.pointLight.color[1] / 255,
                         spec_intensity * self.pointLight.color[0] / 255]

            for obj in self.scene:
                if obj is not intersect.sceneObject:
                    hit = obj.ray_intersect(intersect.point,  light_dir)
                    if hit is not None and intersect.distance < frobeniusNorm(subVectors(self.pointLight.position, intersect.point)):
                        shadow_intensity = 1


        finalColor = mulVectors(sumVectors(ambientColor, multiply((1 - shadow_intensity), sumVectors(diffuseColor, specColor))), objectColor)

        r = min(1,finalColor[0])
        g = min(1,finalColor[1])
        b = min(1,finalColor[2])

        return color(r, g, b)