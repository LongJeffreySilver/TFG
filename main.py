
from Controlador_extractor import Controlador_extractor
from Controlador_ficheros import Controlador_ficheros
from Generador_informe import Generador_informe
from Controlador_Herramientas import Controlador_Herramientas
from Valorador_riesgo import Valorador_riesgo

#Creacion y gestion de rutas de ficheros y carpetas
controladorFicheros = Controlador_ficheros()
rutasCarpetas = controladorFicheros.creacionCarpetas() # [0] entrada, [1] salida y [2] matriz de riesgos

#Lanzar el escaner de red cableado e inalambrico
controladorHerramientas = Controlador_Herramientas
ficherosEntrada = controladorHerramientas.escanearRed(rutasCarpetas[0])

#Se rellenan la lista de IPs privadas en IPv4 e IPv6
listaIPPrivadas = ["10.0","172.16","192.168","169.254"]
controladorFicheros.rellenarListaPrivadaIPv4(listaIPPrivadas)
controladorFicheros.rellenarListaPrivadaIPv6(listaIPPrivadas)

#Se crea un conjunto de target (IP,MAC,Version) con los 2 ficheros de entradas de herramientas diferentes
controladorExtractor = Controlador_extractor()
conjuntoTarget = set()
conjuntoTarget = controladorExtractor.rellenarListaTargetEttercap(listaIPPrivadas, ficherosEntrada[0]) #ficherosEntrada[0] contiene la ruta del fichero generado por Ettercap
conjuntoTarget = controladorExtractor.rellenarListaTargetTCPdump(listaIPPrivadas, conjuntoTarget, ficherosEntrada[1]) #ficherosEntrada[1] contiene la ruta del fichero generado por Tcpdump

#Para no ocupar espacio y que se acumulenb siempre ficheros, se van a ir borrando que ya no se utilizan
controladorFicheros.borrarFichero(ficherosEntrada[0])
controladorFicheros.borrarFichero(ficherosEntrada[1])

#Se escribe el conjunto final en un fichero
controladorFicheros.escribirFicheroTarget(conjuntoTarget,rutasCarpetas[1]) #Fichero con la vinculacion MAC;IP actual
ficheroListaIPs = controladorFicheros.escribirIPs(conjuntoTarget,rutasCarpetas[1])# Fichero con la lista de IPs actual para Greenbone

rutaInforme = controladorHerramientas.analisisDeRiesgos(ficheroListaIPs) #Escribir ruta despues y devolver ruta del fichero CSV

#Se extrae la informacion del reporte CSV generado por Greenbone
conjuntoTarget = controladorExtractor.extraerCVS(conjuntoTarget,rutasCarpetas[0],rutaInforme)

#Valoracion del riesgo y generacion de la matriz de riesgos
valoradorRiesgo = Valorador_riesgo()
conjuntoTarget = valoradorRiesgo.valoracionRiesgo(conjuntoTarget,rutasCarpetas[2])#Retorna el conjuntoTarget modificado con el impacto y severidad actualizado

#Generar informe final en JSON
informe = Generador_informe()
informe.generarInforme(conjuntoTarget,rutasCarpetas[1])