import subprocess
import time
#Antes hay que crear una carpeta para guardar todos los registros de vulnerabilidades

#Crear el registro de este informe



'''
Linea 1: Mac (conjunto target), num vulnerabilidades en ese informe (conjunto target)
Resto de lineas: nombre vulnerabilidad, puerto y protocolo 
'''


def crearRegistroVulnerabilidades(self,ruta,conjuntoTarget):

    nombreFichero = ruta + f"Registro_vulnerabilidades_{time.strftime('%Y/%m/%d-%H:%M')}.txt"
    ficheroVulnerabilidades = open(nombreFichero,'w')
    for target in conjuntoTarget:
        numVulnerabilidades = len(target.listaVulnerabilidades)
        encabezado = target.mac + ";" + numVulnerabilidades + "\n"
        ficheroVulnerabilidades.write(encabezado)
        for vulnerabilidad in target.listaVulnerabilidades:
            nombre = vulnerabilidad.nombreVulnerabiliad
            protocoloYpuerto = vulnerabilidad.protocoloYpuerto
            restoLineas = nombre + ";" + protocoloYpuerto + "\n"
            ficheroVulnerabilidades.write(restoLineas)

    ficheroVulnerabilidades.close()


#Leer los registros anteriores

def consultarRegistroVulnerabilidades(self,rutaRegistros,vulnerabilidad):

    procesoFind = subprocess.run(["find", rutaRegistros, "-type", "f", "-ctime" ,"-20"], capture_output=True,text=True) #Saca los informes de los ultimos 20 dias
    informes = procesoFind.stdout.splitlines()
    contador_vulnerabilidad = 0
    for rutaFichero in informes:  #Recorrer los informes de los ultimos 20 dias
        fichero = open(rutaFichero,"r")
        linea = fichero.readline()
        while linea != "": 
            procesoGrepMac = subprocess.run(["grep", vulnerabilidad.hostname, fichero]).returncode == 0 #0 si existe, !=0 si no
            #SI grep con la MAC == ok ENTONCES
            if procesoGrepMac == True:
                vul = vulnerabilidad.nombreVulnerabiliad + ";" + vulnerabilidad.protocoloYpuerto
                #Grep nombre vulnerabilidad + ; + protocoloYpuerto
                procesoGrepVul = subprocess.run(["grep", vul, fichero]).returncode == 0 #0 si existe, !=0 si no || FIXME Si no funciona, capar el espacio del final
                if procesoGrepVul == True: #Hay repeticion de vulnerabilidad
                    contador_vulnerabilidad+=1
            else: #Si no coincide la MAC en el fichero no hay ni repeticion
                fichero.close()
                break
            linea = fichero.readline()
        
        fichero.close()
    return contador_vulnerabilidad