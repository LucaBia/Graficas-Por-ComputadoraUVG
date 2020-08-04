# Gian Luca Rivera - 18049

from gl import Render

bitmap = Render(2000, 2000)
bitmap.glViewPort(0, 0, 2000 , 2000)
bitmap.glClearColor(0,0,0)
bitmap.glClear()


# ---------------------------
# Dibujo de puntos
# ---------------------------
# bitmap.glVertex(0, 0)
# bitmap.glVertex(1, 1)
# bitmap.glVertex(1, -1)
# bitmap.glVertex(-1, 1)
# bitmap.glVertex(-1, -1)
# bitmap.glVertex(0.2, 0.8)
# bitmap.glVertex(0.5, 0.7)
# bitmap.glVertex(0.75, 0.5)

# ---------------------------
# Dibujo de lineas
# ---------------------------
# bitmap.glLine(0,0,1,0)
# bitmap.glLine(0,0,1,0.5)
# bitmap.glLine(0,0,1,1)
# bitmap.glLine(0,0,0.5,1)
# bitmap.glLine(0,0,0,1)
# bitmap.glLine(0,0,-0.5,1)
# bitmap.glLine(0,0,-1,1)
# bitmap.glLine(0,0,-1,0.5)
# bitmap.glLine(0,0,-1,0)
# bitmap.glLine(0,0,-1,-0.5)
# bitmap.glLine(0,0,-1,-1)
# bitmap.glLine(0,0,-0.5,-1)
# bitmap.glLine(0,0,0.5,-1)
# bitmap.glLine(0,0,0.5,-1)
# bitmap.glLine(0,0,1,-1)
# bitmap.glLine(0,0,1,-0.5)
# bitmap.glLine(0,0,0,-1)

bitmap.loadObjModel('./Models/coffee.obj', (1000, 400, 0), (80, 80, 80))

bitmap.glFinish('output.bmp')
bitmap.glZBuffer('outputZbuffer.bmp')

print("El bitmap se genero exitosamente, revisa la carpeta contenedora")




