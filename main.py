
from Controlador_extractor import Controlador_extractor
from Controlador_ficheros import Controlador_ficheros
from Generador_informe import Generador_informe
from Controlador_Herramientas import Controlador_Herramientas
from Valorador_riesgo import Valorador_riesgo

#Variables
listaIPPrivadas = ["10.0","172.16","192.168","169.254"]
rutaFicherosEntrada = "/home/kali/Escritorio/TFG/Ficheros_de_Entrada/" #Como esta en git se puede llegar a lanzar un pwd y que se cree ahi
rutaFicherosSalida =  "/home/kali/Escritorio/TFG/Ficheros_de_Salida/"
rutaMatrizRiesgos = "/home/kali/Escritorio/TFG/Matrices_de_Riesgos/"

#Lanzar herramientas -> Lo mas seguro es que estoy cambie por un controlador de herramientas
lanzador = Controlador_Herramientas
ficherosEntrada = lanzador.escanearRed(rutaFicherosEntrada)

controladorExtractor = Controlador_extractor()
controladorFicheros = Controlador_ficheros()

#Se rellenan la lista de IPs privadas en IPv4 e IPv6
controladorFicheros.rellenarListaPrivadaIPv4(listaIPPrivadas)
controladorFicheros.rellenarListaPrivadaIPv6(listaIPPrivadas)

#Se crea un conjunto de target (IP,MAC,Version) con los 2 ficheros de entradas de herramientas diferentes
conjuntoTarget = set()
conjuntoTarget = controladorExtractor.rellenarListaTargetEttercap(controladorFicheros,listaIPPrivadas, ficherosEntrada[0]) #ficherosEntrada[0] contiene la ruta del fichero generado por Ettercap
conjuntoTarget = controladorExtractor.rellenarListaTargetTCPdump(controladorFicheros,listaIPPrivadas, conjuntoTarget, ficherosEntrada[1]) #ficherosEntrada[1] contiene la ruta del fichero generado por Tcpdump

#Para no ocupar espacio y que se acumule siempre, se van a ir borrando los ficheros que ya no se utilizan
controladorFicheros.borrarFichero(ficherosEntrada[0])
controladorFicheros.borrarFichero(ficherosEntrada[1])

#Se escribe el conjunto final en un fichero
controladorFicheros.escribirFicheroTarget(conjuntoTarget,rutaFicherosSalida) #Fichero con la vinculacion MAC;IP actual
ficheroListaIPs = controladorFicheros.escribirIPs(conjuntoTarget,rutaFicherosSalida)# Fichero con la lista de IPs actual para Greenbone

lanzador.analisisDeRiesgos(controladorFicheros,ficheroListaIPs) #Escribir ruta despues y devolver ruta del fichero CSV

#Se extrae la informacion del reporte CSV generado por Greenbone
conjuntoTarget = controladorExtractor.extraerCVS(controladorFicheros,conjuntoTarget,rutaFicherosEntrada)

#Valoracion del riesgo y generacion de la matriz de riesgos
valoradorRiesgo = Valorador_riesgo()
conjuntoTarget = valoradorRiesgo.valoracionRiesgo(conjuntoTarget,rutaMatrizRiesgos)#Retorna el conjuntoTarget modificado con el impacto y severidad actualizado

#Generar informe final en JSON
informe = Generador_informe()
informe.generarInforme(conjuntoTarget,rutaFicherosSalida)