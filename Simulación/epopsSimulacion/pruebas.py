import time

while True:
    # Variables que deseas compartir
    valor1 = 42
    valor2 = "Hola mundo"

    # Escribe las variables en un archivo
    with open('datos.txt', 'w') as archivo:
        archivo.write(f"{valor1}\n")
        archivo.write(f"{valor2}\n")

    # Espera 30 segundos antes de escribir de nuevo
    time.sleep(30)
