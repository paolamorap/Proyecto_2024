import subprocess

def epmiko(networking, password, direcciones):
    # Crear la lista de argumentos para el comando
    args = ['./b_id.sh', networking, password] + direcciones
    
    try:
        # Abrir el archivo en modo escritura
        with open('b_id.txt', 'w') as output_file:
            # Ejecutar el comando y redirigir la salida al archivo
            subprocess.run(args, stdout=output_file, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")


