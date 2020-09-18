from gl import Raytracer, color
from obj import Obj, Texture
from sphere import Sphere, Material, PointLight, AmbientLight


snow = Material(diffuse = color(0.91, 0.93, 0.95), spec = 96)
button = Material(diffuse = color(0, 0, 0), spec = 32)
nose = Material(diffuse = color(1, 0.35, 0.02), spec = 64)
eye = Material(diffuse = color(1, 1, 1), spec = 64)
mouth = Material(diffuse = color(0.46, 0.44, 0.43), spec = 16)


rayTracer = Raytracer(500, 700)

rayTracer.pointLight = PointLight(position = (-0.5, 1, 0), intensity = 1)
rayTracer.ambientLight = AmbientLight(strength = 0.1)

rayTracer.scene.append(Sphere((0, 1.4,  -4), 0.6, snow))
rayTracer.scene.append(Sphere((0, 0.3, -4), 0.8, snow))
rayTracer.scene.append(Sphere((0, -1, -4), 1, snow))

# rayTracer.pointLight = PointLight(position = (-1, 0.3, 0), intensity = 1)
# rayTracer.ambientLight = AmbientLight(strength = 0.1)

rayTracer.scene.append(Sphere((0, 0.3,  -3), 0.1, button))
rayTracer.scene.append(Sphere((0, -0.1, -3), 0.1, button))
rayTracer.scene.append(Sphere((0, -0.6, -3), 0.13, button))

# rayTracer.pointLight = PointLight(position = (-2, 2, 0), intensity = 1)
# rayTracer.ambientLight = AmbientLight(strength = 0.1)

rayTracer.scene.append(Sphere((0, 1.1,  -3), 0.1, nose))

rayTracer.scene.append(Sphere((-0.13, 1.3,  -3), 0.08, eye))
rayTracer.scene.append(Sphere((0.13, 1.3,  -3), 0.08, eye))
rayTracer.scene.append(Sphere((-0.11, 1.08,  -2.5), 0.03, button))
rayTracer.scene.append(Sphere((0.11, 1.08,  -2.5), 0.03, button))

# rayTracer.pointLight = PointLight(position = (-0.5, 1, 0), intensity = 1)
# rayTracer.ambientLight = AmbientLight(strength = 0.1)

rayTracer.scene.append( Sphere((-0.08, 0.9,  -3), 0.04, mouth))
rayTracer.scene.append( Sphere((0.08, 0.9,  -3), 0.04, mouth))
rayTracer.scene.append( Sphere((-0.20, 0.99,  -3), 0.04, mouth))
rayTracer.scene.append( Sphere((0.20, 0.99,  -3), 0.04, mouth))

 
rayTracer.rtRender()

rayTracer.glFinish('output.bmp')

print("El bitmap se ha generado con exito, revisa la carpeta contenedora")





