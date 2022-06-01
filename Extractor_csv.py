import csv

from Vulnerabilidad import Vulnerabilidad
#from googletrans import Translator #https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group


class Extractor_csv:
    '''def traducir(self,cadena):
        translator = Translator() 
        cadena = translator.translate(cadena,dest ='es').text #traducir al castellano
        return cadena'''

    def arreglarCadena(self,cadena):
        cadenaSinEspacio = cadena.split() #Quitar varios espacios en blanco
        cadena = ""
        for palabra in cadenaSinEspacio:
                cadena+=palabra + " "
        cadena = cadena.replace('\n', ' ')
        return cadena # self.traducir(cadena)

    def extraerCVS(self,conjuntoTarget,rutaFicherosEntrada): 
        ficheroCSV = open(rutaFicherosEntrada + "/Reporte_greenbone.csv", "r")

        with ficheroCSV as csvfile: #El grande Dataset-Unicauca-Version2-87Atts.csv
            reader = csv.DictReader(csvfile)
            for elemento in reader: #Recorrer el fichero por filas
                ip = elemento['IP']
                    
                nombreVulnerabiliad = elemento['NVT Name']
                nombreVulnerabiliad = self.arreglarCadena(nombreVulnerabiliad)

                resumen = elemento['Summary']
                resumen = self.arreglarCadena(resumen)

                protocoloYpuerto = elemento['Port'] + " " + elemento['Port Protocol']
                cvss = elemento['CVSS']

                severidad = elemento['Severity']
                severidad = self.arreglarCadena(severidad)
                
                cves = elemento['CVEs']
                if not cves ==  "":
                    cves = self.arreglarCadena(cves)
                
                tipoSolucion = elemento['Solution Type']
                if tipoSolucion == "VendorFix":
                    tipoSolucion = "Vendor fix"
                tipoSolucion = self.arreglarCadena(tipoSolucion)
                
                descripcionSolucion = elemento['Solution']
                descripcionSolucion = self.arreglarCadena(descripcionSolucion)

                resultado = elemento['Specific Result']
                #resultado = self.traducir(resultado)

                vulnerabilidad = Vulnerabilidad(ip,"",nombreVulnerabiliad,protocoloYpuerto,cvss,severidad,tipoSolucion,descripcionSolucion,resultado,resumen,cves)
                for target in conjuntoTarget:
                    if target.ip == ip:
                        vulnerabilidad.hostname = target.mac
                        target.listaVulnerabilidades.append(vulnerabilidad)
                        break

                ''' Guardar esto para tener en cuenta el formato que se le quiere dar de cara a futuro
                print("***********************************" + "IP: " + ip + "***********************************" + "\n "
                "\tNombre de la vulnerabiliad: " + nombreVulnerabiliad + "\n " +
                "\tProtocolo y puerto: " + protocoloYpuerto + "\n " +
                "\tPuntuacion: " + cvss + "\n " +
                "\tSeveridad: " + severidad + "\n " +
                "\tSolucion: " + tipoSolucion + "\n " +
                "\t\t" + descripcionSolucion + "\n " +
                "\tResultado: \n" + resultado + "\n " +
                "\tResumen: \n" + resumen + "\n " +
                "\tCVEs: " + cves + "\n "
                )'''

        ficheroCSV.close()
        return conjuntoTarget