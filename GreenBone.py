import subprocess
import time


class GreenBone:
    #https://python-gvm.readthedocs.io/en/latest/api/gmpv214.html#gvm.protocols.gmpv214.Gmp.send_command 
    #Se pueden hacer uso de scripts previamente creados en python https://github.com/greenbone/gvm-tools/tree/main/scripts
    #Llamar con subprocess a un gvm-script con el script que usa el gmp -> guiarme con https://github.com/greenbone/gvm-tools/blob/main/scripts/create-targets-from-host-list.gmp.py
    '''
    FIXME

    Sacar de alguna forma la contraseña y el usuario de Greenbone
    Hacer una carpeta para los scripts y cambiar la ruta en los comandos
    Pasarle la ruta de donde se va a guardar el reporte
    '''


    def crearTargets(rutaFichero):
        proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket",
        "/home/kali/Desktop/TFG-1/create-targets-from-host-list.gmp.py", rutaFichero],capture_output=True,text=True) #rutaFichero"/home/kali/Desktop/TFG-1/Ficheros_de_Salida/conjunto_IP.txt"       
        idTarget = proceso.stdout.splitlines()        
        return idTarget #Devuelve el id del target que tiene todas las IPs dentro  
    
    def crearTask(idTarget):
        name = f"Automatic task {time.strftime('%Y/%m/%d-%H:%M:%S')}"
        proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/create_task.py", idTarget, name],capture_output=True,text=True)
        idTask = proceso.stdout.splitlines()
        return idTask[0], name

    def lanzarTask(idTask):
        proceso = subprocess.Popen(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/start_task.py", idTask], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        #Espera hasta que se ha lanzado por completo el comando y proporciona el id del reporte asociado a esa task
        idReport,err = proceso.communicate()
        #errcode = proceso.returncode
        return idReport.strip()

    
    def descargarReporte(self,idReport,nombreTask):
        reporteListo = self.comprobarEstadoReporte(nombreTask)

        if reporteListo == True:
            rutaReporte = nombreTask + ".csv" #FIXME Añadir la ruta a la izquierda
            subprocess.Popen(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
            "/home/kali/Desktop/TFG-1/get_report_csv.py", idReport, rutaReporte])
            return rutaReporte

    def comprobarEstadoReporte(nombreTask):
        #Comprueba cada 300 segundos = 5 minutos si la tarea ha concluido. Cuando termina, se devuelve True como comprobante

        proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/check-gmp.gmp.py", "--task" ,nombreTask, "--status"],capture_output=True,text=True)

        salida = proceso.stdout.splitlines()
        while salida[0] == "GMP UNKNOWN: Report is not available":
                time.sleep(300) 
                proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
                "/home/kali/Desktop/TFG-1/check-gmp.gmp.py", "--task" ,nombreTask, "--status"],capture_output=True,text=True)
                salida = proceso.stdout.splitlines()

        return True

    def borrarTargets(idTarget):
        # delete_target(target_id, *, ultimate=True) #Ultimate es para eliminar por completo incluso del cubo de basura
        a