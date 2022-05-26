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


    def extraerCVS(self,controladorFicheros,conjuntoTarget):
        return self.extractor_csv.extraerCVS(controladorFicheros,conjuntoTarget)
    
    def rellenarListaTargetEttercap(self,controladorFicheros,listaIPPrivadas):
        return self.extractor_ettercap.rellenarListaTargetEttercap(controladorFicheros,listaIPPrivadas)
    
    def rellenarListaTargetTCPdump(self,controladorFicheros,listaIPPrivadas,conjuntoTarget):
        return self.extractor_tcpdump.rellenarListaTargetTCPdump(controladorFicheros,listaIPPrivadas,conjuntoTarget)

    def valoracionRiesgo(self,conjuntoTarget):
        return self.valoradorRiesgo.valoracionRiesgo(conjuntoTarget)