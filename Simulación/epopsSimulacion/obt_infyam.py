import yaml

def infyam(nombre):
# Cargar el archivo YAML
    with open(nombre, "r") as archivo:
           datos = yaml.safe_load(archivo)
    # Inicializar un diccionario para almacenar las credenciales SSH y la comunidad SNMP
    # Inicializar un diccionario para almacenar las credenciales SSH y la comunidad SNMP
    credenciales_switches = {}

    # Obtener las credenciales SSH y la comunidad SNMP de todos los switches
    for categoria, configuracion in datos.items():
        if categoria.startswith('switchs_'):
            marca = categoria.replace('switchs_', '')  # Obtener la marca del switch
            for switch, detalles in configuracion['hosts'].items():
                if 'host' in detalles:
                    ip = detalles['host']
                    usuario = configuracion['vars'].get('usuario')
                    contraseña = configuracion['vars'].get('contrasena')
                    snmp = configuracion['vars'].get('comunidad_snmp')
                    credenciales_switches[ip] = {'marca': marca, 'usuario': usuario, 'contrasena': contraseña, 'snmp': snmp}

# Imprimir el diccionario de credenciales SSH y SNMP para todos los switches
    return credenciales_switches
