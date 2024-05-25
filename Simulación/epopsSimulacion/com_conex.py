def hex_to_decimal(hex_string):
    decimal = int(hex_string, 16)
    return str(decimal)

def b_conex(direc,b_id,stp_in):
    lc = []
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
                        lc.append((ini+"-"+hex_to_decimal(c_i[-2:]),inj+"-"+c_j))
                    c += 1
                except IndexError:
                    pass
                except KeyError:
                    pass
    return lc


