import subprocess
import time


class GreenBone:
    '''
    FIXME
    Hacer una carpeta para los scripts y cambiar la ruta en los comandos
    '''


    def crearTargets(rutaFichero,rutaScripst,user,password):
        rutaScripst = rutaScripst + "create-targets-from-host-list.gmp.py"
        proceso = subprocess.run(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket",
        rutaScripst, rutaFichero],capture_output=True,text=True) #rutaFichero"/home/kali/Desktop/TFG-1/Ficheros_de_Salida/conjunto_IP.txt"       
        idTarget = proceso.stdout.splitlines()        
        return idTarget #Devuelve el id del target que tiene todas las IPs dentro  
    
    def crearTask(idTarget,rutaScripst,user,password):
        rutaScripst = rutaScripst + "create_task.py"
        name = f"Automatic task {time.strftime('%Y/%m/%d-%H:%M:%S')}"
        proceso = subprocess.run(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
        rutaScripst, idTarget, name],capture_output=True,text=True)
        idTask = proceso.stdout.splitlines()
        return idTask[0], name

    def lanzarTask(idTask,rutaScripst,user,password):
        rutaScripst = rutaScripst + "start_task.py"
        proceso = subprocess.Popen(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
        rutaScripst, idTask], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        #Espera hasta que se ha lanzado por completo el comando y proporciona el id del reporte asociado a esa task
        idReport,err = proceso.communicate()
        #errcode = proceso.returncode
        return idReport.strip()

    
    def descargarReporte(self,idReport,nombreTask,rutaScripst,user,password):
        reporteListo = self.comprobarEstadoReporte(nombreTask,rutaScripst,user,password)
        rutaScripst = rutaScripst + "get_report_csv.py"
        if reporteListo == True:
            rutaReporte = nombreTask + ".csv" #FIXME Añadir la ruta a la izquierda
            subprocess.Popen(["gvm-script", "--gmp-username", user, "--gmp-password", password, "socket", 
            rutaScripst, idReport, rutaReporte])
            return rutaReporte

    def comprobarEstadoReporte(nombreTask,rutaScripst,user,password):
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