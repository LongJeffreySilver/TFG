import subprocess
import time

class GreenBone:

    def crearTargets(self,rutaFichero,rutaScripst,user,password):
        rutaScripst = rutaScripst + "create-targets-from-host-list.gmp.py"
        proceso = subprocess.run(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket",
        rutaScripst, rutaFichero],capture_output=True,text=True) #rutaFichero"/home/kali/Desktop/TFG-1/Ficheros_de_Salida/conjunto_IP.txt"       
        idTarget = proceso.stdout.splitlines()
        print("Target creado")        
        return idTarget[0] #Devuelve el id del target que tiene todas las IPs dentro  
    
    def crearTask(self,idTarget,rutaScripst,user,password):
        rutaScripst = rutaScripst + "create_task.py"
        name = f"Automatic task {time.strftime('%Y/%m/%d-%H:%M:%S')}"
        proceso = subprocess.run(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
        rutaScripst, idTarget, name],capture_output=True,text=True)
        idTask = proceso.stdout.splitlines()
        print("Tarea creada")
        return idTask[0], name

    def lanzarTask(self,idTask,rutaScripst,user,password):
        rutaScripst = rutaScripst + "start_task.py"
        proceso = subprocess.Popen(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
        rutaScripst, idTask], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        #Espera hasta que se ha lanzado por completo el comando y proporciona el id del reporte asociado a esa task
        idReport,err = proceso.communicate()
        print("Tarea lanzada")
        return idReport.strip()

    
    def descargarReporte(self,idReport,nombreTask,rutaScripst,user,password,carpetaEntrada):
        reporteListo = self.comprobarEstadoReporte(nombreTask,rutaScripst,user,password)
        rutaScripst = rutaScripst + "get_report_csv.py"
        if reporteListo == True:
            print("Descargando el reporte de Greenbone")
            nombreReporte = "Reporte_greenbone"
            rutaReporte = carpetaEntrada + "/" + nombreReporte + ".csv"
            subprocess.Popen(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
            rutaScripst, idReport, rutaReporte])
            print("Reporte descargado con exito")
            return rutaReporte

    def comprobarEstadoReporte(self,nombreTask,rutaScripst,user,password):
        #Comprueba cada 300 segundos = 5 minutos si la tarea ha concluido. Cuando termina, se devuelve True como comprobante
        rutaScripst = rutaScripst + "check-gmp.gmp.py"
        proceso = subprocess.run(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
        rutaScripst, "--task" ,nombreTask, "--status"],capture_output=True,text=True)

        salida = proceso.stdout.splitlines()
        while salida[0] == "GMP UNKNOWN: Report is not available":
                time.sleep(300) 
                proceso = subprocess.run(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
                rutaScripst, "--task" ,nombreTask, "--status"],capture_output=True,text=True)
                salida = proceso.stdout.splitlines()

        return True