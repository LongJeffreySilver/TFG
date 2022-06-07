

import subprocess




    #usuario
proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", "/home/kali/Desktop/TFG-1/create-targets-from-host-list.gmp.py", "127.0.0.1:9392", "/home/kali/Desktop/mierdero.txt"],capture_output=True,text=True)
id_targets = proceso.stdout.splitlines()
for id in id_targets:
    print(id)
#resp = gmp.create_target(name="TARGETNAME3", make_unique=True, hosts=listaTarget)