import json


class Generador_informe:

    def generarInforme(self,conjuntoTarget,rutaSalida):

        informe = {}

        for target in conjuntoTarget:
            if len(target.listaVulnerabilidades) > 0: #Solo sacar en el informe los target que tienen vulnerabilidades
                
                dicVulnerabilidades = {}
                #Recorrer la lista de vulnerabilidades y hacer un diccionario con los datos de cada vulnerabilidad
                for vulnerabilidad in target.listaVulnerabilidades:
                    dicVulnerabilidades[vulnerabilidad.nombreVulnerabiliad] = ({
                        "Nombre de la vulnerabilidad" : vulnerabilidad.nombreVulnerabiliad,
                        "Protocolo y puerto" : vulnerabilidad.protocoloYpuerto,
                        "Puntuacion" : vulnerabilidad.impacto,
                        "Severidad" : vulnerabilidad.severidad,
                        "Lista de CVEs" : vulnerabilidad.cves,
                        "Solucion" : vulnerabilidad.solucion,
                        "Resultado" : vulnerabilidad.resultado,
                        "Resumen" : vulnerabilidad.resumen,
                    })
                #Rellenar el informe
                informe[target.mac + ";" + target.ip] = []
                informe[target.mac + ";" + target.ip] = ({
                    "MAC" : target.mac,
                    "IP" : target.ip,
                    "Lista Vulnerabilidades": dicVulnerabilidades
                })

        #Guardar informe
        with open(rutaSalida +'informe.json', 'w') as file:
            json.dump(informe, file, indent=4)