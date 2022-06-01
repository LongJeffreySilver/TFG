class GreenBone:
    #https://python-gvm.readthedocs.io/en/latest/api/gmpv214.html#gvm.protocols.gmpv214.Gmp.send_command 
    #Se pueden hacer uso de scripts previamente creados en python https://github.com/greenbone/gvm-tools/tree/main/scripts
    
    '''gvm-pyshell \
    --gmp-username webadmin --gmp-password kennwort'''
    
    def borrarTargets(idTarget):
        # delete_target(target_id, *, ultimate=True) #Ultimate es para eliminar por completo incluso del cubo de basura
        a

    def crearTargets(rutaFichero):
        ficheroEntrada = open(rutaFichero,"r")
        linea = ficheroEntrada.readline()
        listaTarget = list()
        while linea != "": #recorre hasta el final del fichero txt
            listaTarget.append(linea)
            linea = ficheroEntrada.readline()

            '''
            Ejemplo de como se lanza
            >>> resp = gmp.create_target(name="TARGETNAME3", make_unique=True, hosts=listaTarget)
            >> from gvm.xml import pretty_print
            >>> pretty_print(resp)
            <create_target_response status="201" status_text="OK, resource created" id="70b6b00c-88a4-410a-9f50-94c5ac0946a4"/>
            
            Tratando esta linea tienes que idTargets = 70b6b00c-88a4-410a-9f50-94c5ac0946a4

            Otra forma de hacerlo segun la documentacion

            res=gmp.create_target("Suspect Host", make_unique=True,hosts=listaTarget)
            >>> target_id = res.xpath('@id')[0]


            '''
            

        return idTargets
    
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
        a