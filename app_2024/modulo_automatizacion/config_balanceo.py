import paramiko
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command
import os

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_balanceo_cisco(connection, vlan_id, interfaz, save_config=False):
    """
    Configura el balanceo de carga para una VLAN específica en un dispositivo Cisco.

    Esta función establece la configuración del árbol de expansión (MST) para una VLAN 
    y ajusta el costo de envío a través de una interfaz dada. Si se solicita, también guarda 
    la configuración en la memoria del dispositivo.

    Parámetros:
        connection (objeto): Una instancia de conexión con el dispositivo Cisco.
        vlan_id (int): El identificador de la VLAN para la cual se configurará el MST.
        interfaz (str): La interfaz donde se aplicará el costo modificado del MST.
        save_config (bool): Si es True, guarda la configuración en la memoria del dispositivo. 
                            Por defecto es False.
    """
    commands = [
        f'vlan {vlan_id}',
        'exit',
        'spanning-tree mst configuration',
        f'instance 1 vlan {vlan_id}',
        'exit',
        f'int {interfaz}',
        'spanning-tree mst 1 cost 10',
    ]

    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print("Configuración de balanceo de carga completada exitosamente")
    except Exception as e:
        print(f"Error al configurar balanceo de carga: {e}")


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_balanceo_hp(connection, vlan_id, interfaz, save_config=False):
    """
    Configura el balanceo de carga en un dispositivo HP A5120 para una VLAN específica.

    Esta función establece la configuración de la región de spanning tree protocol (STP) y ajusta
    el costo de la ruta STP para una interfaz dada. Si se solicita, también guarda la configuración
    de manera forzada en la memoria del dispositivo.

    Parámetros:
        connection (objeto): Una instancia de conexión con el dispositivo HP.
        vlan_id (int): El identificador de la VLAN para la cual se configurará el STP.
        interfaz (str): La interfaz donde se aplicará el costo modificado del STP.
        save_config (bool): Si es True, guarda la configuración de manera forzada en la memoria 
                            del dispositivo. Por defecto es False.

    """
    commands = [
        f'vlan {vlan_id}',
        'quit',
        'stp region-configuration',
        f'instance 1 vlan {vlan_id}',
        'quit',
        'stp pathcost-standard dot1d-1998',
        f'interface {interfaz}',
        f'stp instance 2 cost 10',
        'quit',
    ]

    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')
        print("Configuración de balanceo de carga completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar balanceo de carga: {e}")


#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_balanceo_3com(ip, username, password, vlan_id, interfaz, save_config=False):
    """
    Configura el balanceo de carga en dispositivos 3COM y HP V1910 para una VLAN especifica.

    Parámetros:
    - ip (str): Dirección IP del dispositivo 3Com.
    - username (str): Nombre de usuario para la autenticación SSH.
    - password (str): Contraseña para la autenticación SSH.
    - vlan_id (int): Identificador de la VLAN a configurar.
    - interfaz (str): Interfaz en la que se aplica la configuración de balanceo.
    - save_config (bool): Si es True, guarda la configuración en el dispositivo.

    La función establece una conexión SSH al dispositivo, ejecuta una serie de comandos para configurar
    el balanceo de carga STP (Spanning Tree Protocol) y opcionalmente guarda la configuración.
    Maneja excepciones para asegurar que cualquier fallo en la configuración sea capturado y reportado.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        channel = ssh.invoke_shell()
        # Secuencia de comandos para configurar el balanceo de carga
        send_command(channel, "_cmdline-mode on", wait_time=2)
        interactive_send_command(
            channel,
            "Y",
            "Please input password:",
            "512900",
            wait_time=2
        )
        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"vlan {vlan_id}", wait_time=2)
        send_command(channel, "quit", wait_time=2)
        send_command(channel, "stp region-configuration", wait_time=2)
        send_command(channel, f"instance 1 vlan {vlan_id}", wait_time=2)
        send_command(channel, "quit", wait_time=2)
        send_command(channel, "stp pathcost-standard dot1d-1998", wait_time=2)
        send_command(channel, f"interface {interfaz}", wait_time=2)
        send_command(channel, "stp instance 2 cost 10", wait_time=2)
        send_command(channel, "quit", wait_time=2)

        # Guardar la configuración si se requiere
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)
        print("Configuración de balanceo de carga completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar balanceo de carga: {e}")
    finally:
        ssh.close()

#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_balanceo_tplink(vlan_id, interfaz, archivo_destino=None):
    """
    Genera un archivo de texto con comandos para configurar el balanceo de carga en dispositivos TPLink
    para una VLAN especifica.

    Parámetros:
    - vlan_id (int): Identificador de la VLAN a configurar.
    - interfaz (str): Interfaz en la que se aplica la configuración de balanceo.
    - archivo_destino (str): Ruta del archivo donde se guardarán los comandos. Si es None, se usa una ruta predeterminada.

    Retorna:
    - str: Ruta del archivo donde se han guardado los comandos.

    La función crea un archivo de texto que contiene una serie de comandos para configurar el balanceo de carga
    mediante STP (Spanning Tree Protocol) en un dispositivo TPLink.
    """

    current_dir = os.path.dirname(__file__)

    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        #archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_balanceo.txt'
        archivo_destino = os.path.join(current_dir, 'comandos', 'comandos_balanceo.txt')
    comandos = dedent(f"""
        configure
        vlan {vlan_id}
        exit
        spanning-tree mst configuration
        instance 2 vlan {vlan_id}
        exit
        interface {interfaz}
        spanning-tree mst instance 1 cost 10
        end
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino
    