import subprocess

from GreenBone import GreenBone


class Controlador_Herramientas:

    #Mirar esto https://askubuntu.com/questions/201544/how-to-run-a-file-with-sudo-without-a-password/201551#201551 para habilitar sudo sin contraseña
    #Poner aqui todo lo referente a los comandos de las herramientas
    def analisisCableado(rutaFicherosEntrada): #sudo ettercap -Tqz -s 's(30)lqq' -i eth1 > /home/kali/Desktop/lista.txt 
        rutaFichero = rutaFicherosEntrada + "/Entrada_ettercap.txt"
        fichero = open(rutaFichero,"w")
        proceso = subprocess.Popen(["sudo","ettercap", "-Tqz", "'s(30)lqq'", "-i", "eth1"], stdout=fichero) #Ojo porque hay que hacerlo con sudo
        proceso.wait()
        fichero.close()
        return rutaFichero
    
    def analisisInalambrico(self,rutaFicherosEntrada):
        #Ejecutar Kismet
        #Generar la traza para pasarsela a TCPdump
        traza = rutaFicherosEntrada + "/Traza_kismet.pcap"
        #kismet wlan0 generar_traza traza
        fichero = open(traza,"w")
        proceso = subprocess.Popen(["kismet", "wlan0", "comando para guardar traza", traza]) #NO hacerlo con sudo a poder ser
        #Si no funciona bien esto, mirar la respuesta a este hilo https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
        proceso.wait()
        fichero.close()
        self.lanzarTcpdump(rutaFicherosEntrada,traza) #Pasarle la ruta de la traza

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

    def analisisDeRiesgos(ficheroListaIPs):
        greenBone = GreenBone()
        #Meter al usuario actual en el grupo _gvm para poder lanzar los comandos
        proceso = subprocess.run(["whoami"],capture_output=True,text=True)
        whoami = proceso.stdout.splitlines()
        proceso = subprocess.run(["sudo", "usermod", "-a", "-G", "_gvm", whoami[0]])
 
        #lanzar un script por cada llamada a una funcion                
        
        idTargets = greenBone.crearTargets(ficheroListaIPs)
        idTask = greenBone.crearTask(idTargets)
        greenBone.lanzarTask(idTask)
        informe = greenBone.descargarReporte() #devolver la ruta del fichero CSV si ha habido exito
        greenBone.borrarTargets(idTargets) #Se borran para no ocupar espacio en cada analisis

        #Para mantener la seguridad eliminamos al usuario del grupo que puede ejecutar los comandos de Greenbone
        subprocess.run(["sudo", "gpasswd", "-d", whoami[0], "_gvm"])
        return informe