

import subprocess
import time




#ID del target 23642d44-06ba-4baf-9d69-4fde520407c8
#ID de la task: dcab29cd-d486-4be9-8fff-f812b2d32826
#ID de la task al router: 0481b3a1-c945-4d02-ac02-f911fc359c04
#ID de la task al movris: 869cfce7-e707-4e0d-9510-dc7c772ec405
#ID del reporte hecho al router: 3bac7ea9-033d-47d9-91fd-c3d536ddfb0e
#ID del reporte 1 del movris fbc04680-7006-4624-8f83-a7b9f71d50b3

#Crear tarea
idTarget="0481b3a1-c945-4d02-ac02-f911fc359c04"
name = f"Automatic task {time.strftime('%Y/%m/%d-%H:%M:%S')}"
proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
"/home/kali/Desktop/TFG-1/create_task.py", idTarget, name],capture_output=True,text=True)
salida = proceso.stdout.splitlines()
idTask=salida[0]
print ("Tarea " + name + " creada con exito, su ID es:" + idTask)

#Lanzarla
proceso = subprocess.Popen(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/start_task.py", idTask], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
idReport,err = proceso.communicate()
print ("Tarea " + name + " lanzada con exito, el ID de su reporte es:" + idReport)

#Ver su estado
proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/check-gmp.gmp.py", "--task" ,name, "--status"],capture_output=True,text=True)

salida = proceso.stdout.splitlines()
while salida[0] == "GMP UNKNOWN: Report is not available":
        time.sleep(120)
        proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
        "/home/kali/Desktop/TFG-1/check-gmp.gmp.py", "--task" ,name, "--status"],capture_output=True,text=True)
        salida = proceso.stdout.splitlines()
        #print (salida)
print ("Se termina de comprobar el estado")

#Descargar reporte
idReportArreglado = idReport.strip()
subprocess.Popen(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", 
            "/home/kali/Desktop/TFG-1/get_report_csv.py", idReportArreglado, "Reporte_greenbone.csv"])

print("El reporte con ID: " + idReportArreglado + "ha sido descargado")

