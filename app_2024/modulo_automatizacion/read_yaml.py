import yaml
from yaml.loader import SafeLoader

def cargar_datos_yaml(filepath):
    try:
        with open(filepath, 'r') as file:
            return yaml.load(file, Loader=SafeLoader)
    except Exception as e:
        print(f"Error al cargar el archivo YAML: {e}")
        return None