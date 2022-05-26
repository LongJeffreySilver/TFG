import matplotlib.pyplot as plot
import numpy as np


class Valorador_riesgo:
    def azul():
        return "blue"

    def amarillo():
        return "yellow"

    def marron():
        return "brown"

    def rojo():
        return "red"

    switchSeveridad = {
        "bajo": azul,
        "medio": amarillo,
        "alto": marron,
        "critico": rojo,
    }

    def aplicarFormula(self, valorVulnerabilidad):
        #implementar la formula
        return valorVulnerabilidad

    def revaluarSeveridad(self, valorVulneravilidad): #Estas valoraciones limite estan puestas a ojo sin ningun criterio
        if valorVulneravilidad < 5.0:
            return "bajo"
        elif valorVulneravilidad < 7.0:
            return "medio"
        elif valorVulneravilidad < 9.0:
            return "alto"
        else:
            return "Critico"

    def dibujarMatriz(self,matrizX,matrizY, mac, ip,severidad): #Poner una leyenda con esos colores.
            plot.ylim(0,10) #El eje Y es el unico fijo
            for i in range(0,len(matrizX),1):
                plot.scatter(matrizX[i],matrizY[i],marker="o",color=self.switchSeveridad.get(severidad[i])()) #cada vulnerabilidad se pinta segun su severidad
            plot.xlabel("Numero de vulnerabilidad")
            plot.ylabel("Rango de 0 a 10")
            plot.title("Dispositivo: " + mac + ";" + ip)
            plot.show()
            #en vez de pintarlo, hay que guardarlos para usarlo en el informe de JSON. ESo o guardarlo con el nombre MAC;IP en una carpeta especifica con la fecha
            #plot.savefig("Matriz de riesgos: " + mac + ";" + ip, dpi = 100) #dpi son las pulgadas (probar antes de dejar el numero)
    
    def valoracionRiesgo(self,conjuntoTarget):

        for target in conjuntoTarget:
            if len(target.listaVulnerabilidades) > 0: #Comprobar que ese target tiene al menos una vulnerabilidad en la lista
                numVulnerabilidad = 0
                matrizX = list()
                matrizY = list()
                listaSeveridad = list()
                for vulnerabilidad in target.listaVulnerabilidades:
                    valorVulneravilidad = self.aplicarFormula(vulnerabilidad.impacto) 
                    vulnerabilidad.impacto = valorVulneravilidad #Cambio del impacto como riesgo
                    vulnerabilidad.severidad = self.revaluarSeveridad(float(valorVulneravilidad)) #para saber si ha sido bajo, medio, alto o critico de forma cualitativa tambien
                    matrizX.append(numVulnerabilidad) #Se guarda la coordenada X como el numero de vulnerabilidad
                    matrizY.append(float(valorVulneravilidad)) #Se guarda la coordenada Y como el impacto final
                    listaSeveridad.append(vulnerabilidad.severidad)
                    numVulnerabilidad +=1
                if numVulnerabilidad > 0 and len(target.listaVulnerabilidades) == numVulnerabilidad: #Dibujar la matriz solo de los target que tienen vulnerabilidades
                    self.dibujarMatriz(matrizX,matrizY,target.mac,target.ip,listaSeveridad)
        return conjuntoTarget