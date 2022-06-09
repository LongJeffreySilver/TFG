

import subprocess
import time




#ID del target 23642d44-06ba-4baf-9d69-4fde520407c8
#ID del target router de casa: 81190589-10bd-481b-9bd5-a77ced63ff33
#ID de la task: dcab29cd-d486-4be9-8fff-f812b2d32826
#ID de la task al router: 0481b3a1-c945-4d02-ac02-f911fc359c04
#ID de la task al movris: 869cfce7-e707-4e0d-9510-dc7c772ec405
#ID del reporte hecho al router: 3bac7ea9-033d-47d9-91fd-c3d536ddfb0e
#ID del reporte 1 del movris fbc04680-7006-4624-8f83-a7b9f71d50b3

#Crear tarea
proceso = subprocess.run(["find", "/", "-name", "TFG-1"], capture_output=True,text=True) #FIXME "TFG" es como se llame el proyecto de git
rutaScripst = proceso.stdout.splitlines()
rutaScripst=rutaScripst[0].strip()
rutaScripst = rutaScripst +"/Scripts/"
print(rutaScripst)

