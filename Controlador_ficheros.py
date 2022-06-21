import subprocess
import time


class Controlador_Ficheros:
   
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

    def escribirFicheroTarget(self,conjuntoTarget,ruta):
        ficheroTarget = open(ruta + "/Conjunto_MAC;IP.txt",'w')
        for target in conjuntoTarget:
            ficheroTarget.write(target.mac + ";" + target.ip + "\n")
        ficheroTarget.close()


    def escribirIPs(self,conjuntoTarget,nombreFichero):
        nombreFichero += "/Conjunto_IP.txt"
        ficheroIP = open(nombreFichero,'w')
        for target in conjuntoTarget:
            ficheroIP.write(target.ip + "\n")
        ficheroIP.close()
        return nombreFichero

    def borrarFichero(self,rutaFichero):
        #hacer la llamada a rm -f fichero
        proceso = subprocess.run(["rm", "-f",rutaFichero])
    
    def creacionCarpetas(self):
        #Ruta actual
        proceso = subprocess.run(["find", "/", "-name", "TFG"], capture_output=True,text=True) #FIXME "TFG" es como se llame el proyecto de git
        rutaApp = proceso.stdout.splitlines()
        rutaApp=rutaApp[0].strip()

        #Creacion de nombres de directorios
        dirEntrada = rutaApp + "/Ficheros_de_Entrada"
        dirSalida = rutaApp + "/Ficheros_de_Salida"
        dirInformes = rutaApp + "/Informes"
        dirInformeActual = dirInformes + "/Informe_"+ f"{time.strftime('%d.%m.%Y-%H:%M:%S')}"
        dirMatricesRiesgos = dirInformeActual + "/Matrices_de_riesgos"
        dirRegistroRiesgos = rutaApp + "/Registro_Riesgos"

        listaCreacion = list()
        listaCreacion.append(dirEntrada)
        listaCreacion.append(dirSalida)
        listaCreacion.append(dirInformes)
        listaCreacion.append(dirInformeActual) #Se crea siempre porque lleva marca de tiempo actual
        listaCreacion.append(dirMatricesRiesgos)
        listaCreacion.append(dirRegistroRiesgos)

        #Por cada directorio se comprueba si existe. Si NO existe se crea
        for fichero in listaCreacion:
            proceso = subprocess.run(['test', '-d', fichero]).returncode == 0 #0 si existe, !=0 si no
            if proceso == False: #Si no existe lo crea
                subprocess.run(["mkdir",fichero])
        return listaCreacion

    def crearRegistroRiesgos(self,ruta,conjuntoTarget):

        nombreFichero = ruta + "/" + f"Registro_riesgos_{time.strftime('%d.%m.%Y-%H:%M:%S')}.txt"
        ficheroVulnerabilidades = open(nombreFichero,'w')
        for target in conjuntoTarget:
            if len(target.listaVulnerabilidades) > 0:
                numVulnerabilidades = len(target.listaVulnerabilidades)
                encabezado = target.mac + ";" + str(numVulnerabilidades) + "\n"
                ficheroVulnerabilidades.write(encabezado)
                for vulnerabilidad in target.listaVulnerabilidades:
                    nombre = vulnerabilidad.nombreVulnerabiliad
                    protocoloYpuerto = vulnerabilidad.protocoloYpuerto
                    restoLineas = nombre + ";" + protocoloYpuerto + "\n"
                    ficheroVulnerabilidades.write(restoLineas)

        ficheroVulnerabilidades.close()