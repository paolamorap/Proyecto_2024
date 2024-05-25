import yaml

def crear_diccionario_host_marca(archivo):
    diccionario = {}
    with open(archivo, 'r') as file:
        data = yaml.safe_load(file)
        for grupo, info_grupo in data.items():
            for host, info_host in info_grupo['hosts'].items():
                diccionario[info_host['host']] = grupo

    return diccionario

