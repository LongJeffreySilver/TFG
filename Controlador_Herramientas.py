import subprocess

from GreenBone import GreenBone


class Controlador_Herramientas:

    #Mirar esto https://askubuntu.com/questions/201544/how-to-run-a-file-with-sudo-without-a-password/201551#201551 para habilitar sudo sin contraseña
    #Poner aqui todo lo referente a los comandos de las herramientas
    def analisisCableado(rutaFicherosEntrada): #sudo ettercap -Tqz -s 's(30)lqq' -i eth1 > /home/kali/Desktop/lista.txt 
        rutaFichero = rutaFicherosEntrada + "/Entrada_ettercap.txt"
        fichero = open(rutaFichero,"w")
        result = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result.wait()
        print(result.stdout)
        fichero.write(result.stdout)
        fichero.close()
        return rutaFichero
    
    def analisisInalambrico(self,rutaFicherosEntrada):
        #Ejecutar Kismet
        #Generar la traza para pasarsela a TCPdump
        traza = rutaFicherosEntrada + "/Traza_kismet.pcap"
        #kismet wlan0 generar_traza traza

        self.lanzarTcpdump(rutaFicherosEntrada,traza) #Pasarle la ruta de la traza

    def lanzarTcpdump(rutaFicherosEntrada,traza): # No se usa la opcion tcp en el comando porque solo coge IPv4
        #tcpdump -qns 0 -e -r traza 
        #Genera un fichero en rutaFicherosEntrada
        rutaFichero = rutaFicherosEntrada + "/Entrada_tcpdump.txt"
        fichero = open(rutaFichero,"w")

        fichero.close()
        return rutaFichero

    def escanearRed(self,rutaFicherosEntrada): #Ambos generan unos ficheros que se usan mas adelante
        ficheroCableado = self.analisisCableado(rutaFicherosEntrada)
        ficheroInalambrico = self.analisisInalambrico(rutaFicherosEntrada)
        return [ficheroCableado,ficheroInalambrico]

    def analisisDeRiesgos(controladorFicheros,ficheroListaIPs):
        greenBone = GreenBone()
        
        idTargets = greenBone.crearTargets(controladorFicheros,ficheroListaIPs)
        idTask = greenBone.crearTask(idTargets)
        greenBone.lanzarTask(idTask)
        informe = greenBone.descargarReporte() #devolver la ruta del fichero CSV si ha habido exito
        greenBone.borrarTargets(idTargets) #Se borran para no ocupar espacio en cada analisis
        return informe