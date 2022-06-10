import subprocess

from GreenBone import GreenBone


class Controlador_Herramientas:

    #Mirar esto https://askubuntu.com/questions/201544/how-to-run-a-file-with-sudo-without-a-password/201551#201551 para habilitar sudo sin contraseña

    def analisisCableado(rutaFicherosEntrada): #sudo ettercap -Tqz -s 's(30)lqq' -i eth1 > /home/kali/Desktop/lista.txt 
        
        #Confirmar si la interfaz cableada eth0 por defecto esta activa con: ip link | grep eth0 -c
        procesoIP = subprocess.Popen(["ip" ,"link"], stdout=subprocess.PIPE)
        procesoGrep = subprocess.Popen(('grep', "eth0", "-c"), stdin=procesoIP.stdout, stdout=subprocess.PIPE,text=True)
        procesoIP.wait()
        salida = procesoGrep.communicate()
        salida = salida[0].strip()

        if salida == 1:
            rutaFichero = rutaFicherosEntrada + "/Entrada_ettercap.txt"
            fichero = open(rutaFichero,"w")
            proceso = subprocess.Popen(["sudo","ettercap", "-Tqz", "-s", "'s(300)lqq'", "-i", "eth0"], stdout=fichero) #Se registran datos durante 5 minutos (300 segundos)
            proceso.communicate()
            fichero.close()
            return rutaFichero
        else:
            return -1 #codigo error porque no hay interfaz cableada

    def analisisInalambrico(self,rutaFicherosEntrada):
        #Confirmar si la interfaz inalambrica eth0 por defecto esta activa con: ip link | grep wlan0 -c
        procesoIP = subprocess.Popen(["ip" ,"link"], stdout=subprocess.PIPE)
        procesoGrep = subprocess.Popen(('grep', "wlan0", "-c"), stdin=procesoIP.stdout, stdout=subprocess.PIPE,text=True)
        procesoIP.wait()
        salida = procesoGrep.communicate()
        salida = salida[0].strip()
        
        if salida == 1:

            #Ejecutar Kismet
            #Generar la traza para pasarsela a TCPdump
            traza = rutaFicherosEntrada + "/Traza_kismet.pcap"
            #kismet wlan0 generar_traza traza
            fichero = open(traza,"w")
            proceso = subprocess.Popen(["kismet", "wlan0", "comando para guardar traza", traza]) #NO hacerlo con sudo
            #Si no funciona bien esto, mirar la respuesta a este hilo https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
            proceso.wait()
            fichero.close()
            return self.lanzarTcpdump(rutaFicherosEntrada,traza) #Pasarle la ruta de la traza
        else:
            return -1 #codigo error porque no hay interfaz inalambrica

    def lanzarTcpdump(rutaFicherosEntrada,traza): # No se usa la opcion tcp en el comando porque solo coge IPv4
        #tcpdump -qns 0 -e -r traza 
        #Genera un fichero para la salida de Kismet + Tcpdump
        rutaFichero = rutaFicherosEntrada + "/Entrada_tcpdump.txt"
        fichero = open(rutaFichero,"w")
        proceso = subprocess.Popen(["tcpdump", "-qns", "0", "e" , "-r", traza], stdout=fichero)
        fichero.close()
        return rutaFichero

    def escanearRed(self,rutaFicherosEntrada): #Ambos generan unos ficheros que se usan mas adelante
        ficheroCableado = self.analisisCableado(rutaFicherosEntrada)
        ficheroInalambrico = self.analisisInalambrico(rutaFicherosEntrada)
        return [ficheroCableado,ficheroInalambrico]
        
    def analisisDeRiesgos(ficheroListaIPs,user,password):
        greenBone = GreenBone()
        #Lanzar el servicio
        subprocess.run(["sudo", "gvm-start"])
        #Meter al usuario actual en el grupo _gvm para poder lanzar los comandos
        proceso = subprocess.run(["whoami"],capture_output=True,text=True)
        whoami = proceso.stdout.splitlines()
        proceso = subprocess.run(["sudo", "usermod", "-a", "-G", "_gvm", whoami[0]])

        #Carpeta de los scripts
        proceso = subprocess.run(["find", "/", "-name", "TFG"], capture_output=True,text=True) #FIXME "TFG" es como se llame el proyecto de git
        rutaScripst = proceso.stdout.splitlines()
        rutaScripst=rutaScripst[0].strip()
        rutaScripst = rutaScripst +"/Scripts/"

        #lanzar un script por cada llamada a una funcion                
        
        idTargets = greenBone.crearTargets(ficheroListaIPs,rutaScripst,user,password)
        idTask, nombreTask = greenBone.crearTask(idTargets,rutaScripst,user,password)
        idReport = greenBone.lanzarTask(idTask,rutaScripst,user,password)
        rutaInforme = greenBone.descargarReporte(idReport,nombreTask,rutaScripst,user,password) 
        #greenBone.borrarTargets(idTargets)

        #Para mantener la seguridad eliminamos al usuario del grupo que puede ejecutar los comandos de Greenbone
        subprocess.run(["sudo", "gpasswd", "-d", whoami[0], "_gvm"])
        #Parar el servicio
        subprocess.run(["sudo", "gvm-stop"])

        return rutaInforme