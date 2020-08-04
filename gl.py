# Gian Luca Rivera - 18049

# https://docs.python.org/3/library/struct.html
import struct
from obj import Obj

# ----------------------
# Librerias matematicas
# ----------------------
# Suma de vectores de 3 elementos
def sum(x0, x1, y0, y1, z0, z1):
    arr_sum = []
    arr_sum.extend((x0 + x1, y0 + y1, z0 + z1))
    return arr_sum

# Resta de vectores de 3 elementos
def sub(x0, x1, y0, y1, z0, z1):
    arr_sub = []
    arr_sub.extend((x0 - x1, y0 - y1, z0 - z1))
    return arr_sub
    
# Producto cruz entre dos vectores
def cross(v0, v1):
    arr_cross = []
    arr_cross.extend((v0[1] * v1[2] - v1[1] * v0[2], -(v0[0] * v1[2] - v1[0] * v0[2]), v0[0] * v1[1] - v1[0] * v0[1]))
    return arr_cross

# Producto punto (utilizado para la matriz con las coordenadas de luz)
def dot(norm, lX, lY, lZ):
    return ((norm[0] * lX) + (norm[1] * lY) + (norm[2] * lZ))

# Calculo de la normal de un vector
def norm(v0):
    if (v0 == 0):
        arr0_norm = []
        arr0_norm.extend((0,0,0))
        return arr0_norm

    return((v0[0]**2 + v0[1]**2 + v0[2]**2)**(1/2))

# Division vector con normal
def div(v0, norm):
    if (norm == 0):
        arr0_norm = []
        arr0_norm.extend((0,0,0))
        return arr0_norm
    else:
        arr_div = []
        arr_div.extend((v0[0] / norm, v0[1] / norm, v0[2] / norm))
        return arr_div

def baryCoords(Ax, Bx, Cx, Ay, By, Cy, Px, Py):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((By - Cy)*(Px - Cx) + (Cx - Bx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        v = ( ((Cy - Ay)*(Px - Cx) + (Ax - Cx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w
# -------------------------------------------------------------


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
LIGHT_GREEN = color(0.5,1,0)


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
        #Z - buffer, depthbuffer, buffer de profudidad
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]
    
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
        try:
            self.pixels[vertexY][vertexX] = self.pixel_color
        except:
            pass


    # Cambia el color de una linea en la pantalla
    def glVertexCoord(self, x, y, color = None):
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.pixel_color
        except:
            pass

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
    


    #  Modelo OBJ
    def loadObjModel(self, filename, translate, scale, isWireframe = False):
        model = Obj(filename)

        # Coordenadas del vector de luz, equivalente a V3(0,0,1)
        lightX, lightY, lightZ = 0, 0, 1

        for face in model.faces:

            vertCount = len(face)

            if isWireframe:
                for vert in range(vertCount):
                    v0 = model.vertices[face[vert][0] - 1]
                    v1 = model.vertices[face[(vert + 1) % vertCount][0] - 1]
                    x0 = round(v0[0] * scale[0]  + translate[0])
                    y0 = round(v0[1] * scale[1]  + translate[1])
                    x1 = round(v1[0] * scale[0]  + translate[0])
                    y1 = round(v1[1] * scale[1]  + translate[1])
                    
                    self.glLineCoord(x0, y0, x1, y1)

            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]

                x0 = int(v0[0] * scale[0]  + translate[0])
                y0 = int(v0[1] * scale[1]  + translate[1])
                z0 = int(v0[2] * scale[2]  + translate[2])
                x1 = int(v1[0] * scale[0]  + translate[0])
                y1 = int(v1[1] * scale[1]  + translate[1])
                z1 = int(v1[2] * scale[2]  + translate[2])
                x2 = int(v2[0] * scale[0]  + translate[0])
                y2 = int(v2[1] * scale[1]  + translate[1])
                z2 = int(v2[2] * scale[2]  + translate[2])

                # Operaciones para el calculo de la normal
                sub1 = sub(x1, x0, y1, y0, z1, z0)
                sub2 = sub(x2, x0, y2, y0, z2, z0)
                cross1 = cross(sub1, sub2 )
                norm1 = norm(cross1)
                cross2 = cross(sub1, sub2)

                normal = div(cross2, norm1)
                intensity = dot(normal, lightX, lightY, lightZ)

                if intensity >= 0:
                    self.triangle_bc(x0,x1,x2, y0, y1, y2, z0, z1, z2, color(intensity, intensity, intensity))
                
                # Si los vertices son mayores a 4 se asigna un 3 valor en las dimensiones
                if vertCount > 3: 
                    v3 = model.vertices[face[3][0] - 1]
                    x3 = int(v3[0] * scale[0]  + translate[0])
                    y3 = int(v3[1] * scale[1]  + translate[1])
                    z3 = int(v3[2] * scale[2]  + translate[2])

                    if intensity >= 0:
                        self.triangle_bc(x0,x2,x3, y0, y2,y3, z0, z2,z3, color(intensity, intensity, intensity))

    #Barycentric Coordinates
    def triangle_bc(self, Ax, Bx, Cx, Ay, By, Cy, Az, Bz, Cz, color = None):
        minX = min(Ax, Bx, Cx)
        minY = min(Ay, By, Cy)
        maxX = max(Ax, Bx, Cx)
        maxY = max(Ay, By, Cy)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(Ax, Bx, Cx, Ay, By, Cy, x,y)

                if u >= 0 and v >= 0 and w >= 0:

                    z = Az * u + Bz * v + Cz * w

                    if z > self.zbuffer[y][x]:
                        self.glVertexCoord(x, y, color)
                        self.zbuffer[y][x] = z