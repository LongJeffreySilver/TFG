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

    def extraerCVS(self,conjuntoTarget,rutaInforme): 
        ficheroCSV = open(rutaInforme, "r")

        with ficheroCSV as csvfile:
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
                    
        ficheroCSV.close()
        return conjuntoTarget