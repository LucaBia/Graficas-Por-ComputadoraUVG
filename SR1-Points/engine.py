# Gian Luca Rivera - 18049

from gl import Render

continuar = True
while continuar:
    print("""
    1. Generar bitmap default
    2. Generar bitmap personalizado
    """)

    opcion = int(input("Ingresa un numero del menu: "))
    if(opcion == 1):
        bitmap = Render(1000, 1000,0, 0, 0)
        bitmap.glViewPort(250, 250, 500 , 500)
        bitmap.glVertex(0, 0)
        bitmap.glFinish('output.bmp')
    elif(opcion == 2):
        ancho = int(input("Ingresa el ancho del framebuffer: "))
        alto = int(input("Ingresa el alto del framebuffer: "))
        vpAncho = int(input("Ingresa el ancho del viewport: "))
        vpAlto = int(input("Ingresa el alto del viewport: "))
        vpX = int(input("Ingresa la coordenada en X del viewport: "))
        vpY = int(input("Ingresa la coordenada en Y del viewport: "))
        coordenadaX = int(input("Ingresa la coordenada en x donde quieres dibujar el punto (rango de -1 a 1): "))
        coordenadaY = int(input("Ingresa la coordenada en y donde quieres dibujar el punto (rango de -1 a 1): ")) 
        opcionColor = input("Quieres cambiar el color del bit map y del punto? (s/n): ")
        if (opcionColor == "s"):
            redMapa = int(input("Ingresa el numero de rojo para el bitmap (rango de 0 a 1): "))
            greenMapa = int(input("Ingresa el numero de verde para el bitmap (rango de 0 a 1): "))
            blueMapa = int(input("Ingresa el numero de azul para el bitmap (rango de 0 a 1): "))
            redPoint = int(input("Ingresa el numero de rojo para el punto (rango de 0 a 1): "))
            greenPoint = int(input("Ingresa el numero de verde para el punto (rango de 0 a 1): "))
            bluePoint = int(input("Ingresa el numero de azul para el punto (rango de 0 a 1): "))
            bitmap = Render(ancho, alto, redMapa, greenMapa, blueMapa)
            bitmap.glColor(redPoint, greenPoint, bluePoint)
            bitmap.glViewPort(vpX, vpY, vpAncho, vpAlto)
            bitmap.glVertex(coordenadaX, coordenadaY)
            bitmap.glFinish('outputPersonalizadocolor.bmp') 
        else:
            bitmap = Render(ancho, alto, 0 , 0, 0)
            bitmap.glViewPort(vpX, vpY, vpAncho, vpAlto)
            bitmap.glVertex(coordenadaX, coordenadaY)
            bitmap.glFinish('outputPersonalizado.bmp') 
    else:
        print("Opcion incorrecta")

    print("El bitmap se genero exitosamente, revisa la carpeta contenedora")

