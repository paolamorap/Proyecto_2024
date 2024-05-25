import yaml

# Obtener las IPs de los switches TPLink
def filtplink(nombre):
    # Cargar el archivo YAML
    with open(nombre, "r") as archivo:
       datos = yaml.safe_load(archivo)

    ips_tplink = []
    credenciales_tplink = {}

    # Obtener las IPs de los switches TPLink y las credenciales SSH
    if 'switchs_tplink' in datos:
        configuracion_tplink = datos['switchs_tplink']
        for switch, detalles in configuracion_tplink['hosts'].items():
            if 'host' in detalles:
                ip = detalles['host']
                ips_tplink.append(ip)
                credenciales_tplink[ip] = {
                    'usuario': configuracion_tplink['vars'].get('usuario'),
                    'contraseña': configuracion_tplink['vars'].get('contrasena')
                }

    return ips_tplink, credenciales_tplink

