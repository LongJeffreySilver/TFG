from sympy import arg
from Controlador_ficheros import Controlador_Ficheros
from Generador_informe import Generador_informe
from  Controlador_extractor import Controlador_extractor
from Controlador_Herramientas import Controlador_Herramientas
from argparse import Namespace
import sys

def main(args: Namespace) -> None:

    #Creacion y gestion de rutas de ficheros y carpetas

    print("Se procede a la creacion de carpetas")
    controlador_ficheros = Controlador_Ficheros()
    rutasCarpetas = controlador_ficheros.creacionCarpetas() # [0] entrada, [1] salida, [2] Informes, [3] Informe actual, [4] Matrices de riesgos del informe actual y [5] Registro de vulnerabilidades
    print("Carpetas creadas con exito")

    #Lanzar el escaner de red cableado e inalambrico
    controlador_herramientas = Controlador_Herramientas()

    print("Se lanza el escaner")
    ficherosEntrada = controlador_herramientas.escanearRed(rutaFicherosEntrada=rutasCarpetas[0])
    print("Red escaneada con exito")

    #Se rellenan la lista de IPs privadas en IPv4 e IPv6
    print("Rellenando lista de IPs privadas")
    listaIPPrivadas = ["10.0","172.16","192.168","169.254"]

    controlador_ficheros.rellenarListaPrivadaIPv4(listaIPPrivadas)
    controlador_ficheros.rellenarListaPrivadaIPv6(listaIPPrivadas)
    print("Lista de IPs privadas rellena")

    #Se crea un conjunto de target (IP,MAC,Version) con los 2 ficheros de entradas de herramientas diferentes
    controlador_extractor = Controlador_extractor()
    conjuntoTarget = set()
    print("El valor de cableado es: " + ficherosEntrada[0] + " y el de inalambrico: " + ficherosEntrada[1])
    if ficherosEntrada[0] != "-1":
        conjuntoTarget = controlador_extractor.rellenarListaTargetEttercap(listaIPPrivadas=listaIPPrivadas,rutaFicherosEntrada=ficherosEntrada[0]) #ficherosEntrada[0] contiene la ruta del fichero generado por Ettercap
        print("Se procede a borrar el fichero cableado")
        controlador_ficheros.borrarFichero(ficherosEntrada[0])
    if ficherosEntrada[1] != "-1":
        conjuntoTarget = controlador_extractor.rellenarListaTargetTCPdump(listaIPPrivadas, conjuntoTarget, ficherosEntrada[1]) #ficherosEntrada[1] contiene la ruta del fichero generado por Tcpdump
        print("Se procede a borrar el fichero inalambrico")
        controlador_ficheros.borrarFichero(ficherosEntrada[1])
    if ficherosEntrada[0] == "-1" and ficherosEntrada[1] == "-1":
        print("No hay ninguna interfaz de red conectada.")
        sys.exit()
    #Para no ocupar espacio y que se acumulen siempre ficheros, se van a ir borrando que ya no se utilizan



    #Se escribe el conjunto final en un fichero
    controlador_ficheros.escribirFicheroTarget(conjuntoTarget,rutasCarpetas[1]) #Fichero con la vinculacion MAC;IP actual
    ficheroListaIPs = controlador_ficheros.escribirIPs(conjuntoTarget,rutasCarpetas[1])# Fichero con la lista de IPs actual para Greenbone

    user = args[1] #"admin"
    password = args[2] 
    rutaInforme = controlador_herramientas.analisisDeVulnerabilidades(ficheroListaIPs,user,password,rutasCarpetas[0]) #Escribir ruta despues y devolver ruta del fichero CSV
    print("Finalizado el analisis de vulnerabilidades")
    #rutaInforme = "/home/kali/Desktop/TFG/Ficheros_de_Entrada/Reporte_greenbone.csv"

    #Se extrae la informacion del reporte CSV generado por Greenbone
    conjuntoTarget = controlador_extractor.extraerCVS(conjuntoTarget,rutaInforme)

    #Valoracion del riesgo y generacion de la matriz de riesgos
    conjuntoTarget = controlador_extractor.valoracionRiesgo(conjuntoTarget,rutasCarpetas[4],rutasCarpetas[5])#Retorna el conjuntoTarget modificado con el impacto y severidad actualizado
    print("Finalizada la valoracion de riesgos")
    #Generar informe final en JSON
    generador_informe = Generador_informe()
    generador_informe.generarInforme(conjuntoTarget,rutasCarpetas[3])
    controlador_ficheros.crearRegistroRiesgos(rutasCarpetas[5],conjuntoTarget)
    print("Informe creado con exito")

#Generar el main
if __name__ == '__main__':
   main(sys.argv)
