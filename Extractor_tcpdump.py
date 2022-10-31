from Target import Target


class Extractor_tcpdump:

    def tratarIPv4(self,ip,mac,listaIPPrivadas,conjuntoTarget):
        lineaPorPuntos = ip.split(sep='.')
        ipCorta = lineaPorPuntos[0] + "." + lineaPorPuntos[1]
        repeticion = 0
        if ipCorta in listaIPPrivadas:
            for elemento in conjuntoTarget:
                if not elemento.mac == mac:
                    repeticion = repeticion + 1
            if repeticion == len(conjuntoTarget): #Si es igual el numero es porque no hay ningun elemento con la misma MAC
                ip = ipCorta + "." + lineaPorPuntos[2] + "." + lineaPorPuntos[3] #192.168.1.70
                return [ip,1]
        return ["",0]
  
    def tratarIPv6(self,ip,mac,listaIPPrivadas,conjuntoTarget): #Para IPv6
        lineaPorPuntos = ip.split(sep='.')
        ipv6 = lineaPorPuntos[0] #Ya no tiene puerto
        ipCortada = ipv6.split(sep=':')
        ipCorta = ipCortada[0]
        repeticion = 0
        if ipCorta in listaIPPrivadas:
            for elemento in conjuntoTarget:
                if not elemento.mac == mac:
                    repeticion = repeticion + 1
            if repeticion == len(conjuntoTarget): #Si es igual el numero es porque no hay ningun elemento con la misma MAC
                return [lineaPorPuntos[0],1]
        return ["",0]

    def rellenarListaTargetTCPdump(self,listaIPPrivadas,conjuntoTarget,rutaFicherosEntrada):
        ficheroEntrada = open(rutaFicherosEntrada,"r")
        linea = ficheroEntrada.readline()

        while linea != "":
            lineaPorComas = linea.split(sep=',') #Tres campos: 0 MACs, 1 version, 2 IPs
            lineaFragmento = lineaPorComas[0] #08:00:27:47:89:2e > 98:97:d1:35:7b:d5
            lineaPorMac = lineaFragmento.split(sep=' ')
            mac1 = lineaPorMac[0].upper() #08:00:27:47:89:2e
            mac2 = lineaPorMac[2].upper() #98:97:d1:35:7b:d5
            version = lineaPorComas[1] #IPv4
            lineaFragmento = lineaPorComas[2]
            lineaPorIP = lineaFragmento.split(sep=' ')
            ip1 = lineaPorIP[3] #192.168.1.70.43900
            ip2 = lineaPorIP[5] #155.54.212.96.443:
            
            #Hay que quitar el puerto de la IPv4 solo
            if version == " IPv4": #ojo al espacio del principio
                version = "4"
                IPyBooleano = self.tratarIPv4(ip1,mac1,listaIPPrivadas,conjuntoTarget)
                if IPyBooleano[1]: #Si se cumple es una IP privada
                    target = Target(IPyBooleano[0],mac1,version)
                    conjuntoTarget.add(target)
                
                IPyBooleano = self.tratarIPv4(ip2,mac2,listaIPPrivadas,conjuntoTarget)
                if IPyBooleano[1]:
                    target = Target(IPyBooleano[0],mac2,version)
                    conjuntoTarget.add(target)
                
            else:
                version = "6"
                #Ver si es una IP privada
                IPyBooleano = self.tratarIPv6(ip1,mac1,listaIPPrivadas,conjuntoTarget)
                if IPyBooleano[1]:
                    target = Target(IPyBooleano[0],mac1,version)
                    conjuntoTarget.add(target)

                IPyBooleano = self.tratarIPv6(ip2,mac2,listaIPPrivadas,conjuntoTarget)
                if IPyBooleano[1]:
                    target = Target(IPyBooleano[0],mac2,version)
                    conjuntoTarget.add(target)

             
            linea = ficheroEntrada.readline()
        
        ficheroEntrada.close()
        return conjuntoTarget
