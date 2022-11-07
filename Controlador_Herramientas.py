import subprocess
import time

from GreenBone import GreenBone
from threading import Timer

class Controlador_Herramientas:

    def comprobarInterfaz(self,listaInterfazActual):
        result = subprocess.run(["ls","/sys/class/net"], check=True, capture_output=True, text=True)
        output = result.stdout.split('\n')
  
        interface = ""
        for interface in output: #Wired: en (enps1, eno1 or ens1) and eth (eth0) | Wifi: wl (wlan wlp)
            if (("en" in interface) or ("wl" in interface)  or ("eth" in interface)) and (len(interface) < 8):
              
                for interfazActual in listaInterfazActual:

                    if interfazActual in interface:
                        rutaInterface = "/sys/class/net/" + interface + "/operstate"
                        proceso = subprocess.Popen(["cat", rutaInterface], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
                        salida,err = proceso.communicate()
                        estadoInterfaz = salida.split(sep="\n")
                        if estadoInterfaz[0] == "up":
                            return interface                    
        return "-1"

    def analisisCableado(self,rutaFicherosEntrada): 
        
        #Si la conexion a eth0 es up, realiza el analisis. En caso de no existir o ser down, entonces no se realiza el analisis.
        listaInterfazActual = ["enp","eno","ens","eth"] #Tipos de redes cableadas
        interfaz = self.comprobarInterfaz(listaInterfazActual)
        if interfaz != "-1":
            rutaFichero = rutaFicherosEntrada + "/Entrada_ettercap.txt"
            fichero = open(rutaFichero,"w")
            proceso = subprocess.Popen(["sudo","ettercap", "-Tqz", "-s", "'s(300)lqq'", "-i", interfaz], stdout=fichero) #Se registran datos durante 5 minutos (300 segundos)
            proceso.communicate()
            fichero.close()
            return rutaFichero
        else:
            return "-1" #codigo error porque no hay interfaz cableada

    def analisisInalambrico(self,rutaFicherosEntrada):
        #Si la conexion a wlan0 es up, realiza el analisis. En caso de no existir o ser down, entonces no se realiza el analisis.
        listaInterfazActual = ["wlan","wlp"]
        interfaz = self.comprobarInterfaz(listaInterfazActual)
        if interfaz != "-1":
            return self.lanzarTcpdump(rutaFicherosEntrada,interfaz) #Pasarle la ruta de la traza
        else:
            return "-1" #codigo error porque no hay interfaz inalambrica

    def lanzarTcpdump(self,rutaFicherosEntrada,interfaz):
        #Crea y rellena la traza de red inalambrica con tcpdump hasta que pasan 30 segundos.
        traza = rutaFicherosEntrada+ "/Traza_tcpdump.pcap"
        fichero = open(traza, "w")
        def kill(process): return process.kill()

        proceso = subprocess.Popen(["sudo", "tcpdump", "-w", traza, "-i", interfaz])

        my_timer = Timer(300, kill, [proceso])

        try:
            my_timer.start()
            proceso.communicate()
        finally:
            my_timer.cancel()
            fichero.close()

        #Debido a que la traza se crea con el usuario tcpdump, se cambia al actual para poder tratarla.
        proceso = subprocess.run(["whoami"], capture_output=True, text=True)
        whoami = proceso.stdout.splitlines()

        proceso = subprocess.Popen(["sudo", "chown", whoami[0], traza])

        #Se genera un fichero txt con las trazas unicamente de los protocolos upd y tcp, tanto con IPv4 como IPv6.
        rutaFichero = rutaFicherosEntrada + "/Entrada_tcpdump.txt"
        fichero = open(rutaFichero, "w")
        proceso = subprocess.Popen(
            ["tcpdump", "udp", "or", "tcp", "-qns", "0", "-e", "-t", "-r", traza], stdout=fichero)
        fichero.close()

        return rutaFichero
    
    def escanearRed(self,rutaFicherosEntrada): #Ambos generan unos ficheros que se usan mas adelante
        ficheroCableado = self.analisisCableado(rutaFicherosEntrada=rutaFicherosEntrada)
        ficheroInalambrico = self.analisisInalambrico(rutaFicherosEntrada=rutaFicherosEntrada)
        return [ficheroCableado,ficheroInalambrico]
        
    def analisisDeVulnerabilidades(self,ficheroListaIPs,user,password,carpetaEntrada):
        #Meter al usuario actual en el grupo _gvm para poder lanzar los comandos
        proceso = subprocess.run(["whoami"],capture_output=True,text=True)
        whoami = proceso.stdout.splitlines()
        proceso = subprocess.run(["sudo", "usermod", "-a", "-G", "_gvm", whoami[0]])
        
        greenBone = GreenBone()
        #Lanzar el servicio
        subprocess.run(["sudo", "gvm-start"],capture_output=True,text=True)
        #Cambio de permisos del socket para que lo pueda utilizar el usuario
        subprocess.run(["sudo", "chmod", "662", "/var/run/gvmd/gvmd.sock"])

        #Carpeta de los scripts
        proceso = subprocess.run(["find", "/", "-name", "TFG"], capture_output=True,text=True) #FIXME "TFG" es como se llame el proyecto de git
        rutaScripst = proceso.stdout.splitlines()
        rutaScripst=rutaScripst[0].strip()
        rutaScripst = rutaScripst +"/Scripts/"

        #lanzar un script por cada llamada a una funcion                
        time.sleep(60) #Durmiendo el proceso para esperar a que se lance Greenbone

        idTarget = greenBone.crearTargets(ficheroListaIPs,rutaScripst,user,password)
        idTask, nombreTask = greenBone.crearTask(idTarget,rutaScripst,user,password)
        idReport = greenBone.lanzarTask(idTask,rutaScripst,user,password)
        rutaInforme = greenBone.descargarReporte(idReport,nombreTask,rutaScripst,user,password,carpetaEntrada) #pasarle el sitio del reporte
        #greenBone.borrarTargets(idTargets)

        #Para mantener la seguridad eliminamos al usuario del grupo que puede ejecutar los comandos de Greenbone
        subprocess.run(["sudo", "gpasswd", "-d", whoami[0], "_gvm"])
        #Parar el servicio
        #subprocess.run(["sudo", "gvm-stop"],capture_output=True,text=True)

        return rutaInforme
