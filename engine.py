# Gian Luca Rivera - 18049

from gl import Render
from obj import Obj, Texture
from shaders import gooch, static, phong, toon

# bitmap = Render(2000, 2000)
# bitmap.glViewPort(0, 0, 2000 , 2000)
bitmap = Render(1000, 1000)
bitmap.glViewPort(0, 0, 1000 , 1000)
# bitmap.glClearColor(0,0,0)
# bitmap.glClear()


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

# texture = Texture('./Models/Textures/coff.bmp')
# bitmap.active_shader = toon
# bitmap.active_shader = gooch
# bitmap.active_shader = static
# bitmap.active_shader = phong
# bitmap.loadObjModel('./Models/coffee.obj', (1000, 400, 0), (80, 80, 80))


# bitmap.active_texture = Texture('./Models/Textures/Dice_Base.bmp')
# bitmap.active_shader = toon
# bitmap.active_shader = gooch
# bitmap.active_shader = static
# bitmap.active_shader = phong
# bitmap.loadObjModel('./Models/Dice.obj', (500, 500, 0), (600, 600, 600), (0, 90, 0))

# bitmap.active_texture = Texture('./Models/Textures/mask.bmp')
# # bitmap.active_shader = toon
# # bitmap.active_shader = gooch
# # bitmap.active_shader = static
# bitmap.active_shader = phong
# bitmap.loadObjModel('./Models/mascara.obj', (500, 300, 0), (10, 10, 10), (90, 180, 180))

bitmap.active_texture = Texture('./Models/Textures/statue_diffuse.bmp')
# bitmap.active_shader = toon
# bitmap.active_shader = gooch
# bitmap.active_shader = static
bitmap.active_shader = phong
bitmap.loadObjModel('./Models/tom.obj', (500, 0, 0), (3, 3, 3), (270, 0, 0))
# Medium shot
# bitmap.loadObjModel('./Models/tom.obj', (250, 0, 0), (3, 3, 3), (285, 0, 40))
# Low Angle
# bitmap.loadObjModel('./Models/tom.obj', (500, 50, 0), (3, 3, 3), (250, 0, 20))
# High Angle 
# bitmap.loadObjModel('./Models/tom.obj', (500, 50, 0), (3, 3, 3), (310, 0, 20))
# Dutch Angle con 35º
# bitmap.loadObjModel('./Models/tom.obj', (300, 50, 0), (3, 3, 3), (270, 35, 10))

# Modelo de Carlos que se ve bien con la textura 
# texture = Texture('./Models/Textures/model.bmp')
# bitmap.active_shader = toon
# bitmap.active_shader = gooch
# bitmap.active_shader = static
# bitmap.active_shader = phong
# bitmap.loadObjModel('./Models/model.obj', (1000, 1000, 0), (600, 600, 600))

bitmap.glFinish('output.bmp')
# bitmap.glZBuffer('outputZbuffer.bmp')

print("El bitmap se genero exitosamente, revisa la carpeta contenedora")




