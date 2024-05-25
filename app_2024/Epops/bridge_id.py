from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()


def bri_id(ips,datos):
    """
    Función devuelve el bridge id de un grupo de switches
    Párametros
    ips(list)   :       Lista de Direcciones IP de los switches 
    datos(dict) :       Diccionario con información de los switches
    
    Returns
    b_info(dict):       Diccionario con bridge id de cada dispositivo
    f (int)     :       Bandera de Error en comunicación SNMP
    fif (list)  :       Lista de dispositivos en los que hubo problemas
    """
    b_info = {}
    f = 0
    fif = []
    for server_ip in ips:
        comunidad = datos[server_ip]["snmp"]
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.17.1.1'
        )
        if errorIndication != None:
            f = 1
            fif.append(server_ip)

        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                b_info[server_ip] = (val.prettyPrint())[-12:]
    return b_info,f,fif
