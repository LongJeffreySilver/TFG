class Vulnerabilidad:


    def __init__(self,ip,mac,nombreVulnerabiliad,protocoloYpuerto,cvss,severidad,tipoSolucion, descripcionSolucion,resultado,resumen,cves): #asi se hace un constructor
        self.ip = ip
        self.hostname = mac
        self.nombreVulnerabiliad = nombreVulnerabiliad
        self.protocoloYpuerto = protocoloYpuerto
        self.impacto = cvss
        self.severidad = severidad
        self.solucion = tipoSolucion + "\n" + "\t" + descripcionSolucion
        self.resultado = resultado
        self.resumen = resumen
        self.cves = cves