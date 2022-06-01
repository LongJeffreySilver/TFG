from Target import Target


class Extractor_ettercap:

    def getIpVersion(self,ip): #diferenciar entre IPv4 e IPv6 para el tratamiento
        aux = list(ip)
        caracter = aux[0] #coger el primer caracter que sera un numero en IPv4 o una letra f en IPv6
        
        if caracter == "f": #es IPv6
            aux2 = ip.split(sep=":") #tratamiento IPv6
            ipCortada = aux2[0] #Cortar la IP para que sea FEXX
            version = "6"
        else: #es IPv4
            aux2 = ip.split(sep=".") #tratamiento IPv4
            ipCortada = aux2[0] + "." + aux2[1] #Cortar la IP para que sea X.X
            version = "4"
        return [ipCortada,version]

    def rellenarListaTargetEttercap(self,listaIPPrivadas, rutaFicherosEntrada):
        ficheroEntrada = open(rutaFicherosEntrada,"r")
        linea = ficheroEntrada.readline()
        condicionHostList = 0
        conjuntoTarget= set()
        
        while linea != "": #recorre hasta el final del fichero txt
            
            if linea == "Closing text interface...\n":
                condicionHostList = 0

            if condicionHostList == 1 and linea != "\n":
            # 1)\t192.168.1.1\t98:97:D1:35:7B:D5\n
                lineaCortada = linea.split(sep='\t') 
                ip = lineaCortada[1] #192.168.1.1 o fe80::5ec1:d7ff:fef4:32a8
                mac = lineaCortada[2] #98:97:D1:35:7B:D5\n
                mac2 = mac.split(sep='\n')
                mac = mac2[0]
                aux = self.getIpVersion(ip) #se devuelven dos valores
                ipCortada = aux[0]
                version = aux[1]
                #Parte comun para las IPs
                if ipCortada in listaIPPrivadas: #Si los dos valores son de IP privada
                    target = Target(ip,mac,version)
                    conjuntoTarget.add(target)    
            
            if linea == "Hosts list:\n":
                condicionHostList = 1
            
            linea = ficheroEntrada.readline()
            
        ficheroEntrada.close()
        return conjuntoTarget