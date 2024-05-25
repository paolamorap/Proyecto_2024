from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import read_yaml
import snmp_int
import stp_active_int
import vlan_int
import logs_int

class MyHandler(FileSystemEventHandler):
    def __init__(self, snmp_path, stp_path, stpPriority_path, vlan_path, logs_path):
        self.snmp_path = snmp_path
        self.stp_path = stp_path
        self.stpPriority_path = stpPriority_path
        self.vlan_path = vlan_path
        self.logs_path = logs_path
        self.last_handled = time.time()
        self.debounce_seconds = 10  # Configura este valor para el retardo deseado entre las ejecuciones

    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.last_handled < self.debounce_seconds:
            return  # Salir si el último manejo fue hace menos del tiempo de retardo configurado

        if event.src_path == self.snmp_path:
            print("Archivo SNMP modificado. Ejecutando el script...")
            self.handle_snmp_update()
            self.last_handled = current_time
        elif event.src_path == self.stp_path:
            print("Archivo STP modificado. Ejecutando el script...")
            self.handle_stp_update()
            self.last_handled = current_time
        elif event.src_path == self.stpPriority_path:
            print("Archivo STPPriority modificado. Ejecutando el script...")
            self.handle_stpPriority_update()
            self.last_handled = current_time
        elif event.src_path == self.vlan_path:
            print("Archivo VLAN modificado. Ejecutando el script...")
            self.handle_vlan_update()
            self.last_handled = current_time
        elif event.src_path == self.logs_path:
            print("Archivo LOGS modificado. Ejecutando el script...")
            self.handle_logs_update()
            self.last_handled = current_time

    def handle_snmp_update(self):
        # Llama a la función del módulo auto_snmp para cargar la configuración y procesarla
        datos_yaml = read_yaml.cargar_configuracion_yaml(self.snmp_path)
        snmp_int.procesar_dispositivos_snmp(datos_yaml)

    def handle_stp_update(self):
        datos_yaml = read_yaml.cargar_configuracion_yaml(self.stp_path)
        stp_active_int.procesar_dispositivos_stpActive(datos_yaml)
    
    def handle_stpPriority_update(self):
        datos_yaml = read_yaml.cargar_configuracion_yaml(self.stpPriority_path)
        stp_active_int.procesar_dispositivos_stpPriority(datos_yaml)

    def handle_vlan_update(self):
        try:
            datos_yaml = read_yaml.cargar_configuracion_yaml(self.vlan_path)
            if datos_yaml is not None:
                vlan_int.procesar_dispositivos_vlan(datos_yaml)
            else:
                print("No se encontraron datos en el archivo VLAN.")
        except Exception as e:
            print(f"Error al procesar el archivo VLAN: {e}")
    def handle_logs_update(self):
        try:
            datos_yaml = read_yaml.cargar_configuracion_yaml(self.logs_path)
            if datos_yaml is not None:
                logs_int.procesar_dispositivos_logs(datos_yaml)
            else:
                print("No se encontraron datos en el archivo VLAN.")
        except Exception as e:
            print(f"Error al procesar el archivo VLAN: {e}")
            


if __name__ == "__main__":
    base_path = "/home/du/app_2024/modulo_automatizacion/registros"
    snmp_path = os.path.join(base_path, "datos_snmp.yaml")
    stp_path = os.path.join(base_path, "datos_stp.yaml")
    stpPriority_path = os.path.join(base_path, "datos_stpPriority.yaml")
    vlan_path = os.path.join(base_path, "datos_vlan.yaml")
    logs_path = os.path.join(base_path, "datos_logs.yaml")

    event_handler = MyHandler(snmp_path, stp_path, stpPriority_path, vlan_path, logs_path)
    observer = Observer()
    observer.schedule(event_handler, base_path, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

