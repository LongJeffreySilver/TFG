import subprocess


class GreenBone:
    #https://python-gvm.readthedocs.io/en/latest/api/gmpv214.html#gvm.protocols.gmpv214.Gmp.send_command 
    #Se pueden hacer uso de scripts previamente creados en python https://github.com/greenbone/gvm-tools/tree/main/scripts
    #Llamar con subprocess a un gvm-script con el script que usa el gmp -> guiarme con https://github.com/greenbone/gvm-tools/blob/main/scripts/create-targets-from-host-list.gmp.py
    
    '''gvm-pyshell \
    --gmp-username webadmin --gmp-password kennwort'''
    
    def borrarTargets(idTarget):
        # delete_target(target_id, *, ultimate=True) #Ultimate es para eliminar por completo incluso del cubo de basura
        a

    def crearTargets(rutaFichero):
        proceso = subprocess.run(["gvm-script", "--gmp-username", "admin", "--gmp-password", "8e3898cc-8bce-4506-898f-e5904b317c55", "socket", "/home/kali/Desktop/TFG-1/create-targets-from-host-list.gmp.py", "127.0.0.1:9392", rutaFichero],capture_output=True,text=True) #rutaFichero"/home/kali/Desktop/TFG-1/Ficheros_de_Salida/conjunto_IP.txt"       
        listaIDs = proceso.stdout.splitlines()        
        return listaIDs #Devuelve la lista con los IDs de los targets creados    
    
    def crearTask(idTargets):

        '''
        Segun la documentacion hay que sacar el id de la configuracion
        res = gmp.get_configs()
        >>> for i, conf in enumerate(res.xpath('config')):
        configuracion_id = conf.xpath('@id')[0]
        name = conf.xpath('name/text()')[0]
        print('\n({0}) {1}: ({2})'.format(i, name, id))
        
        Con esto se sacaria el id de la configuracion

        Como solo se va a utilizar por el momento el escaner basico de OpenVas, nos podemos aprovechar de que su id es fijo
        OpenVAS scanner: 08b69003-5fc2-4037-a479-93b440211c73


        Por ultimo se puede crear la task

        res=gmp.create_task(name="Scan Suspect Host",config_id=configuracion_id ,scanner_id="08b69003-5fc2-4037-a479-93b440211c73", target_id=idTargets)
        >>> idTask = res.xpath('@id')[0]


        '''
        return idTask

    def lanzarTask(idTask):
        #gmp.start_task(idTask)
        a
    def descargarReporte():
        #hay una funcion get_report
        a