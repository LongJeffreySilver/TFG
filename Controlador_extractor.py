from Extractor_csv import Extractor_csv
from Extractor_ettercap import Extractor_ettercap
from Extractor_tcpdump import Extractor_tcpdump
from Valorador_riesgo import Valorador_riesgo

class Controlador_extractor:
    
    def __init__(self): #Hacer un patron singleton
        self.extractor_csv = Extractor_csv()
        self.extractor_ettercap = Extractor_ettercap()
        self.extractor_tcpdump = Extractor_tcpdump()
        self.valoradorRiesgo = Valorador_riesgo()


    def extraerCVS(self,conjuntoTarget,rutaInforme):
        return self.extractor_csv.extraerCVS(conjuntoTarget,rutaInforme)
    
    def rellenarListaTargetEttercap(self,listaIPPrivadas, rutaFicherosEntrada):
        return self.extractor_ettercap.rellenarListaTargetEttercap(listaIPPrivadas, rutaFicherosEntrada)
    
    def rellenarListaTargetTCPdump(self,listaIPPrivadas,conjuntoTarget,rutaFicherosEntrada):
        return self.extractor_tcpdump.rellenarListaTargetTCPdump(listaIPPrivadas,conjuntoTarget,rutaFicherosEntrada)

    def valoracionRiesgo(self,conjuntoTarget,rutaMatrizRiesgos,rutaRegistros):
        return self.valoradorRiesgo.valoracionRiesgo(conjuntoTarget,rutaMatrizRiesgos,rutaRegistros)