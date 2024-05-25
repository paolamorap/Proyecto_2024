import bridge_id
import stp_info
import com_conex
import map_int
import stp_blk
import verstp
import time 
import leer
import tp_linkssh
import f
import obt_infyam
import obt_tplink
import obt_root
import bridge_id_root
import tree
import os

print("Ejecutando Fase 1 - Lectura de Archivo de Configuraciones")
#Fase 1
#Lectura de Archivo Yaml - Configuraciones
current_dir = os.path.dirname(__file__)
nombreyaml = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
datos = obt_infyam.infyam(nombreyaml)
direc = datos.keys()
iptp,credenciales = obt_tplink.filtplink(nombreyaml)
b_root,froot,fifroot = obt_root.obtr(datos,iptp)

print("Ejecutando Fase 2 - Almacenamiento de Datos")
#Fase 2
#Informacion STP
# Bridge ID, Designed Bridge
b_id,ff,fif = bridge_id.bri_id(direc,datos)
st_inf,ff,fif = stp_info.stp_inf(direc,datos)
#Proceso extra para conmutadores TPLINK
f.epmiko(credenciales[iptp[0]]["usuario"],credenciales[iptp[0]]["contraseña"], iptp)
tp_d = leer.fil_bid("b_id.txt")
print(tp_d)
b_root,froot,fifroot = obt_root.obtr(datos,iptp)
stn = tp_linkssh.tplink_id(b_root,st_inf,tp_d,iptp) 

print("Ejecutando Fase 3 - Identificacion de Conexiones")
#Fase 3
#Identificación de Conexiones
l = com_conex.b_conex(direc,b_id,stn)
#print(l)
#Mapeo de Las etiquetas
info_int = map_int.ma_int(direc,datos)
#print(info_int)

nf = verstp.obtener_numeros_despues_del_punto(l)
#print(nf)
nodb=stp_blk.stp_status(direc,nf,datos)
#print(nodb)

#Fase 4 - Despligue del arbol en la web
print("Ejecutando Fase 4 - Despliegue del Arbol")

bridge_id_root_dis =  bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
#print(bridge_id_root_dis)
root_bridge_id = bridge_id_root.obtener_bridge_id_root(bridge_id_root_dis)
#print(root_bridge_id)
b_root = bridge_id_root.encontrar_ip_por_bridge_id(b_id,root_bridge_id) 

bloq_int=tree.identificar_interfaces_bloqueadas(nodb, info_int)
interconnections = tree.generar_arbol_conexiones_web(l,info_int)
conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
info_disp = tree.obtener_informacion_dispositivos(direc,datos)
discovered_hosts = tree.generate_switch_names(direc)

OUTPUT_TOPOLOGY_FILENAME = 'topology.js' 
TOPOLOGY_FILE_PATH = r"/var/www/topologia/topology.js" 
TOPOLOGY_FILE_HEAD = f"\n\nvar topologyData = "
TOPOLOGY_DICT = tree.generate_topology_json(discovered_hosts, interconnections,b_root,conexiones_blok, info_disp) 
tree.write_topology_file(TOPOLOGY_DICT,TOPOLOGY_FILE_HEAD,TOPOLOGY_FILE_PATH) 
print("------------FIN----------")
