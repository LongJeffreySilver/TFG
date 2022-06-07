import subprocess


class Controlador_ficheros:
   
    def ocho():
        return "8"
    def nueve():
        return "9"

    def A():
        return "a"

    def B():
        return "b"

    def C():
        return "c"

    def D():
        return "d"

    def E():
        return "e"

    def F():
        return "f"

    switchAscii = {
        8: ocho,
        9: nueve,
        10: A,
        11: B,
        12: C,
        13: D,
        14: E,
        15: F
    }

    def rellenarListaPrivadaIPv4(self,listaIPPrivadas):
        rangoIP= 17
        for i in range(15):
            aux = "172."
            aux = aux + str(rangoIP)
            listaIPPrivadas.append(aux)
            rangoIP = rangoIP + 1

    def rellenarListaPrivadaIPv6(self,listaIPPrivadas):
        base = "fe"
        primero = ""
        segundo = ""
        for i in range(8,16):
            primero = self.switchAscii.get(i)()
            basePrimero = base + primero
            for j in range(16):
                if(j > 7):
                    segundo = self.switchAscii.get(j)()
                else:
                    segundo= str(j)
                completo = basePrimero + segundo
                listaIPPrivadas.append(completo)

    '''def abrirFichero(self,nombre,permiso): #w para escribir, r para leer y n si no se quiere permiso
        if permiso == "n":
            fichero = open(nombre)
        else:
            fichero = open(nombre,permiso)
        return fichero'''
    
    '''def cerrarFichero(self,fichero):
        fichero.close()'''

    def escribirFicheroTarget(conjuntoTarget,ruta):
        ficheroTarget = open(ruta + "/Conjunto_MAC;IP.txt",'w')
        for target in conjuntoTarget:
            ficheroTarget.write(target.mac + ";" + target.ip + "\n")
        ficheroTarget.close()


    def escribirIPs(conjuntoTarget,nombreFichero):
        nombreFichero += "/Conjunto_IP.txt"
        ficheroIP = open(nombreFichero,'w')
        for target in conjuntoTarget:
            ficheroIP.write(target.ip + "\n")
        ficheroIP.close()
        return nombreFichero

    def borrarFichero(rutaFichero):
        #hacer la llamada a rm -f fichero
        proceso = subprocess.run(["rm", "-f",rutaFichero])
    
    def creacionCarpetas():
        #Ruta actual
        proceso = subprocess.run(["pwd"],capture_output=True,text=True)
        pwd = proceso.stdout.splitlines()

        #Creacion de nombres de ficheros
        fichEntrada = pwd[0] + "/Ficheros_de_Entrada"
        fichSalida = pwd[0] + "/Ficheros_de_Salida"
        fichMatrices = pwd[0] + "/Matrices_de_Riesgos"

        listaCreacion = list()
        listaCreacion.append(fichEntrada)
        listaCreacion.append(fichSalida)
        listaCreacion.append(fichMatrices)

        #Por cada fichero se comprueba si existe. Si NO existe se crea
        for fichero in listaCreacion:
            proceso = subprocess.run(['test', '-d', fichero]).returncode == 0 #0 si existe, !=0 si no
            if proceso: #Si no existe lo crea
                subprocess.run(["mkdir",fichero])
        return listaCreacion