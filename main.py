
from Controlador_extractor import Controlador_extractor
from Controlador_ficheros import Controlador_ficheros
from Lanzador_herramientas import Lanzador_herramientas
from Valorador_riesgo import Valorador_riesgo

#Variables globales
listaIPPrivadas = ["10.0","172.16","192.168","169.254"]
rutaFicherosEntrada = "/home/kali/Desktop/TFG/Ficheros_de_Entrada/" #Como esta en git se puede llegar a lanzar un pwd y que se cree ahi
rutaFicherosSalida =  "/home/kali/Desktop/TFG/Ficheros_de_Salida/"

#Lanzar herramientas
#lanzador = Lanzador_herramientas()
#lanzador.lanzarEttercap()
#lanzador.lanzarKismet()
#lanzador.lanzarTcpdump()

controladorExtractor = Controlador_extractor()
controladorFicheros = Controlador_ficheros()

#Se rellenan la lista de IPs privadas en IPv4 e IPv6
controladorFicheros.rellenarListaPrivadaIPv4(listaIPPrivadas)
controladorFicheros.rellenarListaPrivadaIPv6(listaIPPrivadas)

#Se crea un conjunto de target (IP,MAC,Version) con los 2 ficheros de entradas de herramientas diferentes
conjuntoTarget = set()
conjuntoTarget = controladorExtractor.rellenarListaTargetEttercap(controladorFicheros,listaIPPrivadas, rutaFicherosEntrada) #MAC:IP
conjuntoTarget = controladorExtractor.rellenarListaTargetTCPdump(controladorFicheros,listaIPPrivadas, conjuntoTarget, rutaFicherosEntrada) #MAC:IP

#Se escribe el conjunto final en un fichero
controladorFicheros.escribirFicheroTarget(conjuntoTarget,rutaFicherosSalida + "conjunto_MAC;IP.txt") #Fichero con la vinculacion MAC;IP actual
controladorFicheros.escribirIPs(conjuntoTarget,rutaFicherosSalida + "conjunto_IP.txt")# Fichero con la lista de IPs actual para Greenbone

#lanzador.borrarTargets()
#lanzador.rellenarTargetGreenbone()
#lanzador.crearTaskGreenbone()
#lanzador.descargarReporteGreenbone()

#Se extra la informacion del reporte CSV generado por Greenbone
conjuntoTarget = controladorExtractor.extraerCVS(controladorFicheros,conjuntoTarget,rutaFicherosEntrada)

valoradorRiesgo = Valorador_riesgo()
conjuntoTarget = valoradorRiesgo.valoracionRiesgo(conjuntoTarget)