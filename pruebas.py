import subprocess
import time
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

#find carpeta_del_registro -type f -ctime -20
def consultarRegistroVulnerabilidades(self,rutaRegistros,vulnerabilidad):

    proceso = subprocess.run(["find", rutaRegistros, "-type", "f", "-ctime" ,"-20"], capture_output=True,text=True)
    informes = proceso.stdout.splitlines()
    contador_vulnerabilidad = 0
    for rutaFichero in informes:  #Recorrer los informes de los ultimos 20 dias
        fichero = open(rutaFichero,"r")
        linea = fichero.readline()
        while linea != "":
            #SI grep con la MAC == ok ENTONCES
                #Grep nombre vulnerabilidad + ; + protocoloYpuerto
                #Si eso da bien, entonces contador_vulnerabilidad ++
            #Sino coincide la MAC en el fichero
                #break y a otro fichero



            linea = fichero.readline()
        
        fichero.close()