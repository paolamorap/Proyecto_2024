import random
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

def eliminar_elementos(lista_principal, elementos_a_borrar):
    for elemento in elementos_a_borrar:
        if elemento in lista_principal:
            lista_principal.remove(elemento)

    ip = random.choice(lista_principal)

    return  ip 

def obtr(datos,l2):
    try:
        ip = l2[0]
        comunidad = datos[ip]["snmp"]
        # Realizar la solicitud SNMP para obtener estadísticas
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((ip, 161)),
            0, 2,
            '1.3.6.1.2.1.17.2.5'
        )

        # Procesar los resultados
        if errorIndication:
            print(f"Error: {errorIndication}")
        else:
            c = 0
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    ro =  str(val.prettyPrint())[-12:]
                    return ro
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")  

