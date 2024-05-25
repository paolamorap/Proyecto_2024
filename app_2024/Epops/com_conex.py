def hex_to_decimal(hex_string):
    """
    Función para realizar conversión de hexadecimal a decimal

    Párametros
    hex_string(str):    Valor Hexadecimal
    
    Returns
    decimal(str):       Valor hexadecimal convertido a decimal
    """

    decimal = int(hex_string, 16)
    return str(decimal)

def b_conex(direc,b_id,stp_in):
    """
    Función para realizar conversión de hexadecimal a decimal

    Párametros
    direc(list):     lista de Direcciones IP
    b_id(dict):      Diccionario con los bridge ID de cada switch
    stp_in(dict):    Información de stp, bridge designados y puertos designados
    
    Returns
    conex(list):     Lista con tuplas que representan las conexiones entre switches
    """
    conex = []
    for i in direc:
        ini = i
        #ini = i.split(".")[-1]
        for j in direc:
            c = 0
            inf = stp_in[j]
            inj = j
            #inj = j.split(".")[-1]
            for p in range(len(inf[0])):
                try:
                    if b_id[i] == inf[0][p] and i!=j:
                    #in inf[1][c][0] COnexion de j
                    #in inf[1][c][1] COnexion de i
                        c_j = inf[1][c][0]
                        c_i = inf[1][c][1]
                        conex.append((ini+"-"+hex_to_decimal(c_i[-2:]),inj+"-"+c_j))
                    c += 1
                except IndexError:
                    pass
                except KeyError:
                    pass
    return conex


