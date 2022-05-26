import subprocess


class Lanzador_herramientas:

    #Mirar esto https://askubuntu.com/questions/201544/how-to-run-a-file-with-sudo-without-a-password/201551#201551 para habilitar sudo sin contraseña
    #Poner aqui todo lo referente a los comandos de las herramientas
    def lanzarEttercap(self): #sudo ettercap -Tqz -s 's(30)lqq' -i eth1 > /home/kali/Desktop/lista.txt 
        fichero = open("/home/kali/Desktop/mierdero.txt","w")
        result = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result.wait()
        print(result.stdout)
        fichero.write(result.stdout)
        fichero.close()
    def lanzarKismet(self):
        a
    def lanzarTcpdump(self): # No se usa la opcion tcp en el comando porque solo coge IPv4
        #tcpdump -qns 0 -e -r nombre_traza.pcap 
        a