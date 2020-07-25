# Gian Luca Rivera - 18049

# carga e identifica los elemetnos de un archivo obj
class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.read()

    def read(self):
        for line in self.lines:
            if line:
                if (len(line.split(" ")) > 1) :

                    prefix, value = line.split(' ', 1)

                    if prefix == 'v': # Vertices
                        self.vertices.append(list(map(float,value.split(' '))))
                    elif prefix == 'vn': # Vertives normales
                        self.normals.append(list(map(float,value.split(' '))))
                    elif prefix == 'vt': #Coordenada de texturas 
                        self.texcoords.append(list(map(float,value.split(' '))))
                    elif prefix == 'f': #Cara del poligono
                        self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])
            

