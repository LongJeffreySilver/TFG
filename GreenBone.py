import subprocess


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

        proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/create_task.py", idTarget],capture_output=True,text=True)
        idTask = proceso.stdout.splitlines()
        return idTask

    def lanzarTask(idTask): #FIXME Tengo que ver si suelta algun error para capturarlo
        proceso = subprocess.Popen(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/start_task.py", idTask])
    
    def descargarReporte():
        #Sacar primero el id del unico reporte que este disponible (el actual)
        idReport = ""
        subprocess.Popen(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/get_report_csv.py", idReport, "Reporte_greenbone.csv"])
        #borrar reporte con el id del reporte
    
    
    def borrarTargets(idTarget):
        # delete_target(target_id, *, ultimate=True) #Ultimate es para eliminar por completo incluso del cubo de basura
        a