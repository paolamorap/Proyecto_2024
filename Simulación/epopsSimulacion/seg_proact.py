import subprocess
import time 
# Lista de scripts a ejecutar
scripts = ['mon3.py', 'cpu.py', 'war_cpu.py','war_disp.py','war_logs.py']

# Lista para almacenar los procesos
procesos = []

# Iniciar cada script en un proceso separado
for script in scripts:
    print("-"*30)
    print("Se ejecuto el script",script)
    print("-"*30)
    proceso = subprocess.Popen(['python3', script])
    time.sleep(10)
    procesos.append(proceso)

# Opcional: Esperar a que todos los procesos terminen y capturar sus salidas
for proceso in procesos:
    proceso.wait()

print("Todos los scripts han terminado su ejecución.")
