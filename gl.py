# Gian Luca Rivera - 18049

import struct
import numpy
from numpy import cos, sin
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

# Crea una matriz llena de ceros
def zeros_matrix(rows, cols):
    m = []
    while len(m) < rows:
        m.append([])
        while len(m[-1]) < cols:
            m[-1].append(0.0)

    return m

# Multiplicacion de dos matrices
def matrix_multiply(m1, m2):
    rowsM1 = len(m1)
    colsM1 = len(m1[0])
    colsM2 = len(m2[0])
 
    c = zeros_matrix(rowsM1, colsM2)
    for i in range(rowsM1):
        for j in range(colsM2):
            total = 0
            for k in range(colsM1):
                total += m1[i][k] * m2[k][j]
            c[i][j] = total
 
    return c

# Multiplicacion de un vector con una matriz
def multiplyVM(v, m):
    result = []
    for i in range(len(m)):
        total = 0
        for j in range(len(v)):
            total += m[i][j] * v[j]
        result.append(total)
    return result  

def degToRad(number):
    pi = 3.141592653589793
    return number * (pi/180)

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
WHITE = color(1,1,1)
LIGHT_GREEN = color(0.5,1,0)


class Render(object):
    # glInit()
    def __init__(self, width, height):
        self.glCreateWindow(width, height)
        self.bitmap_color = BLACK
        self.pixel_color = WHITE
        self.active_texture = None
        self.active_shader = None
        self.lightX, self.lightY, self.lightZ = 0, 0, 1
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

    def transform(self, vertex, vMatrix):
        # V = [Vx, Vy, Vz, 1]
        augVertex = (vertex[0], vertex[1], vertex[2], 1)
        # Vt = M * V
        transVertex = multiplyVM(augVertex, vMatrix)
        # Vf = [Vtx/Vtw, Vty/Vtw, Vtz/Vtw]
        transVertex = (transVertex[0]/transVertex[3],
                       transVertex[1]/transVertex[3],
                       transVertex[2]/transVertex[3])
    
        return transVertex

    def createModelMatrix(self, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0)):
        # Matriz de traslacion
        # [1, 0, 0, Tx]
        # [0, 1, 0, Ty]
        # [0, 0, 1, Tz]
        # [0, 0, 0, 1]
        translateMatrix = [
            [1, 0, 0, translate[0]],
            [0, 1, 0, translate[1]],
            [0, 0, 1, translate[2]],
            [0, 0, 0, 1]
        ]

        # Matriz de escala
        # [Sx, 0, 0, 0]
        # [0, Sy, 0, 0]
        # [0, 0, Sz, 0]
        # [0, 0, 0, 1]
        scaleMatrix = [
            [scale[0], 0, 0, 0],
            [0, scale[1], 0, 0],
            [0, 0, scale[2], 0],
            [0, 0, 0, 1]
        ]

        rotationMatrix = self.createRotationMatrix(rotate)

        # Matriz final del objeto
        # M = Mt * Mr * Ms
        finalObjectMatrix1 = matrix_multiply(translateMatrix, rotationMatrix)
        finalObjectMatrix = matrix_multiply(finalObjectMatrix1, scaleMatrix)

        return finalObjectMatrix

    def createRotationMatrix(self, rotate=(0,0,0)):
        # Rotacion eje X
        pitch = degToRad(rotate[0])
        # Rotacion eje y
        yaw = degToRad(rotate[1])
        # Rotacion eje z
        roll = degToRad(rotate[2])

        # Matriz de rotacion en X
        rotationX = [
            [1, 0, 0, 0],
            [0, cos(pitch), -sin(pitch), 0],
            [0, sin(pitch), cos(pitch), 0],
            [0, 0, 0, 1]
        ]

        # Matriz de rotacion en Y
        rotationY = [
            [cos(yaw), 0, sin(yaw), 0],
            [0, 1, 0, 0],
            [-sin(yaw), 0, cos(yaw), 0],
            [0, 0, 0, 1]
        ]

        # Matriz de rotacion en Z
        rotationZ = [
            [cos(roll), -sin(roll), 0, 0],
            [sin(roll), cos(roll), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        # Matrix final de rotacion
        # Mr = Rx * Ry * Rz
        finalMatrixRotation1 = matrix_multiply(rotationX, rotationY)
        finalMatrixRotation = matrix_multiply(finalMatrixRotation1, rotationZ)
        
        return finalMatrixRotation
        # return rotationX * rotationY * rotationZ

    #  Modelo OBJ
    def loadObjModel(self, filename, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0)):
        model = Obj(filename)
        modelMatrix = self.createModelMatrix(translate, scale, rotate)
        rotationMatrix = self.createRotationMatrix(rotate)

        for face in model.faces:

            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1 ]
            v1 = model.vertices[ face[1][0] - 1 ]
            v2 = model.vertices[ face[2][0] - 1 ]

            v0 = self.transform(v0, modelMatrix)
            v1 = self.transform(v1, modelMatrix)
            v2 = self.transform(v2, modelMatrix)

            x0, x1, x2 = int(v0[0]), int(v1[0]), int(v2[0])
            y0, y1, y2 = int(v0[1]), int(v1[1]), int(v2[1])
            z0, z1, z2 = int(v0[2]), int(v1[2]), int(v2[2])

            # Si los vertices son mayores a 4 se asigna un 3 valor en las dimensiones
            if vertCount > 3: 
                v3 = model.vertices[face[3][0] - 1]
                v3 = self.transform(v3, modelMatrix)

                x3 = int(v3[0])
                y3 = int(v3[1])
                z3 = int(v3[2])



            try:
                if self.active_texture:
                    vt0 = model.texcoords[face[0][1] - 1]
                    vt1 = model.texcoords[face[1][1] - 1]
                    vt2 = model.texcoords[face[2][1] - 1]
                    vt0X, vt0Y = vt0[0], vt0[1]
                    vt1X, vt1Y = vt1[0], vt1[1]
                    vt2X, vt2Y = vt2[0], vt2[1]

                    if vertCount > 3:
                        vt3 = model.texcoords[face[3][1] - 1]
                        vt3X, vt3Y = vt3[0], vt3[1]
                else:
                    vt0X, vt0Y = 0, 0
                    vt1X, vt1Y = 0, 0
                    vt2X, vt2Y = 0, 0
                    vt3X, vt3Y = 0, 0

                # Normales de los vertices del obj
                vn0 = model.normals[face[0][2] - 1]
                vn1 = model.normals[face[1][2] - 1]
                vn2 = model.normals[face[2][2] - 1]

                vn0 = self.transform(vn0, rotationMatrix)
                vn1 = self.transform(vn1, rotationMatrix)
                vn2 = self.transform(vn2, rotationMatrix)

                if vertCount > 3:
                    vn3 = model.normals[face[3][2] - 1]
                    vn3 = self.transform(vn3, rotationMatrix)

            except:
                pass


            self.triangle_bc(x0, x1, x2, y0, y1, y2, z0, z1, z2, vt0X, vt1X, vt2X, vt0Y, vt1Y, vt2Y, normals = (vn0, vn1, vn2))
            if vertCount > 3:
                self.triangle_bc(x0, x2, x3, y0, y2, y3, z0, z2, z3, vt0X, vt2X, vt3X, vt0Y, vt2Y, vt3Y, normals = (vn0, vn2, vn3))
                 
                

     #Barycentric Coordinates
    def triangle_bc(self, Ax, Bx, Cx, Ay, By, Cy, Az, Bz, Cz, taX, tbX, tcX, taY, tbY, tcY, normals = (), _color = None):
        minX = round(min(Ax, Bx, Cx))
        minY = round(min(Ay, By, Cy))
        maxX = round(max(Ax, Bx, Cx))
        maxY = round(max(Ay, By, Cy))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = baryCoords(Ax, Bx, Cx, Ay, By, Cy, x,y)

                if u >= 0 and v >= 0 and w >= 0:
                    z = Az * u + Bz * v + Cz * w
                    if z > self.zbuffer[y][x]:
                        
                        r, g, b = self.active_shader(
                            self,
                            verts = (Ax, Bx, Cx, Ay, By, Cy, Az, Bz, Cz),
                            baryCoords = (u, v, w),
                            texCoords = (taX, tbX, tcX, taY, tbY, tcY),
                            normals = normals,
                            color = _color or self.pixel_color)

                        self.glVertexCoord(x, y, color(r, g, b))
                        self.zbuffer[y][x] = z