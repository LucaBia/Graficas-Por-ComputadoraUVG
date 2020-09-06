from gl import Raytracer, color
from obj import Obj, Texture
from sphere import Sphere, Material


snow = Material(diffuse = color(0.91, 0.93, 0.95))
button = Material(diffuse = color(0, 0, 0))
nose = Material(diffuse = color(1, 0.35, 0.02))
eye = Material(diffuse = color(1, 1, 1))
mouth = Material(diffuse = color(0.46, 0.44, 0.43))


rayTracer = Raytracer(500, 700)


rayTracer.scene.append(Sphere((0, 1.2,  -4), 0.6, snow))
rayTracer.scene.append(Sphere((0, 0.2, -4), 0.8, snow))
rayTracer.scene.append(Sphere((0, -1, -4), 1, snow))

rayTracer.scene.append(Sphere((0, 0.2,  -3), 0.1, button))
rayTracer.scene.append(Sphere((0, -0.2, -3), 0.1, button))
rayTracer.scene.append(Sphere((0, -0.7, -3), 0.13, button))

rayTracer.scene.append(Sphere((0, 0.9,  -3), 0.1, nose))

rayTracer.scene.append(Sphere((-0.13, 1.1,  -3), 0.08, eye))
rayTracer.scene.append(Sphere((0.13, 1.1,  -3), 0.08, eye))
rayTracer.scene.append(Sphere((-0.11, 0.92,  -2.5), 0.03, button))
rayTracer.scene.append(Sphere((0.11, 0.92,  -2.5), 0.03, button))

rayTracer.scene.append( Sphere((-0.08, 0.7,  -3), 0.04, mouth))
rayTracer.scene.append( Sphere((0.08, 0.7,  -3), 0.04, mouth))
rayTracer.scene.append( Sphere((-0.20, 0.77,  -3), 0.04, mouth))
rayTracer.scene.append( Sphere((0.20, 0.77,  -3), 0.04, mouth))

 
rayTracer.rtRender()

rayTracer.glFinish('output.bmp')

print("El bitmap se ha generado con exito, revisa la carpeta contenedora")





