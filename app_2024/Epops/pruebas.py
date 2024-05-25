epping = [ '10.0.1.16', '10.0.1.21', '10.0.1.3', '10.0.1.9', '10.0.1.5', '10.0.1.6', '10.0.1.8', '10.0.1.10', '10.0.1.4', '10.0.1.11', '10.0.1.15', '10.0.1.17', '10.0.1.18', '10.0.1.19', '10.0.1.13', '10.0.1.14']
eaping = ['10.1.100.17', '10.0.1.7', '10.0.1.16', '10.0.1.21', '10.0.1.3', '10.0.1.9', '10.0.1.5', '10.0.1.6', '10.0.1.8', '10.0.1.10', '10.0.1.4', '10.0.1.11', '10.0.1.15', '10.0.1.17', '10.0.1.18', '10.0.1.19', '10.0.1.13', '10.0.1.14']


if eaping != epping:
    print("Se comparo lista de pings - Listas Diferentes")
    fp = 1
    faux = 1
    # Convertir las listas a conjuntos
    epping_set = set(epping)
    eaping_set = set(eaping)
    # Encontrar los elementos diferentes
    diferentes_en_epping = epping_set - eaping_set
    diferentes_en_eaping = eaping_set - epping_set
    for elemento in diferentes_en_epping:
        print("Dispositivo sin acceso: "+str(elemento)+"\n")
    for elemento in diferentes_en_eaping:
        print("Dispositivo nuevamente con acceso: "+str(elemento)+"\n")

epping=eaping