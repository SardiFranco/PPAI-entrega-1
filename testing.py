# ...existing code...

if __name__ == "__main__":
    # Importa las clases
    from clases.estado import Estado
    from clases.ordenInspeccion import OrdenInspeccion
    from clases.empleado import Empleado
    from clases.usuario import Usuario
    from clases.motivoTipo import MotivoTipo
    from clases.sismografo import Sismografo
    from clases.estacionSismologica import EstacionSismologica
    from pantallaCierreInspeccion import PantallaCierreInspeccion
    from gestorCierreInspeccion import GestorCierreInspeccion
    from clases.cambioEstado import CambioEstado
    from datetime import datetime
    from clases.rol import Rol

    # Instancias de Estado
    estado_pendiente = Estado("OrdenInspección", "Pendiente")
    estado_pendiente = Estado("OrdenInspección", "Cerrada")
    estado_completa = Estado("OrdenInspección", "CompletamenteRealizada")
    estado_FueraServicio = Estado("Sismografo", "Fuera de Servicio")
    estado_Online = Estado("Sismografo", "Online")

    responsable_inspeccion = Rol("Responsable de Inspección de Sismógrafos","ResponsableInspección")
    responsable_reparacion = Rol("Responsable de Reparación de Sismógrafos","ResponsableReparación")

    # Crea empleado predefinido
    empleado_logueado = Empleado(
        nombre="Juan",
        apellido="Pérez",
        telefono=123456789,
        mail="juan.perez@email.com",
        rol=responsable_inspeccion
    )

        

    # Instancias Cambio de Estado
    cambio_estado = CambioEstado(
        fechaHoraInicio=datetime.now(),
        fechaHoraFin=None,
        estado=estado_Online,
        motivoFueraServicio=None,
        empleado=empleado_logueado
    )

    # Estaciones de prueba
    estacion1 = EstacionSismologica(102, -34.6, -58.4, "Estación Central")
    estacion2 = EstacionSismologica(35, -34.7, -58.5, "Estación Norte")
    estacion3 = EstacionSismologica(2434, -34.8, -58.6, "Estación Sur")
    estacion4 = EstacionSismologica(1000, -34.9, -58.7, "Estación Oeste")
    estacion5 = EstacionSismologica(5000, -35.0, -58.8, "Estación Este")

    # Sismografos
    sismografo1 = Sismografo(datetime(2025, 1, 1), 12345, 65, estado_Online, [], estacion1)
    sismografo2 = Sismografo(datetime(2025, 1, 2), 67890, 24, estado_FueraServicio, [], estacion2)
    sismografo3 = Sismografo(datetime(2025, 1, 3), 54321, 122, estado_FueraServicio, [], estacion3)
    sismografo4 = Sismografo(datetime(2025, 1, 4), 98765, 6, estado_Online, [], estacion4)
    sismografo5 = Sismografo(datetime(2025, 1, 5), 11223, 99, estado_Online, [], estacion5)

    sismografo2.cambiosEstado.append(cambio_estado)
    

    # Tipos de motivos
    motivo1 = MotivoTipo("Falla Técnica")
    motivo2 = MotivoTipo("Daño en el Equipo")
    motivo3 = MotivoTipo("Condiciones Ambientales")
    motivo4 = MotivoTipo("Problemas de Conectividad")

    # Lista de órdenes de inspección para testeo
    ordenes_test = [
        OrdenInspeccion(
            nroOrden=1,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 1, 9, 0),
            fechaHoraFinalizacion=None,
            observacion=None,
            estado=estado_pendiente,
            estacionSismologica=estacion1,
            empleado=Empleado(
                nombre="Ana",
                apellido="Gómez",
                telefono=987654321,
                mail="ana.gomez@gmail.com",
                rol=responsable_inspeccion) 
        ),
        OrdenInspeccion(
            nroOrden=2,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 2, 10, 0),
            fechaHoraFinalizacion=datetime(2025, 5, 2, 12, 0),
            observacion=None,
            estado=estado_completa,
            estacionSismologica=estacion2,
            empleado=empleado_logueado
        ),
        OrdenInspeccion(
            nroOrden=3,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 3, 8, 30),
            fechaHoraFinalizacion=None,
            observacion=None,
            estado=estado_pendiente,
            estacionSismologica=estacion3,
            empleado=Empleado(
                nombre="Ana",
                apellido="Gómez",
                telefono=987654321,
                mail="ana.gomez@gmail.com",
                rol=responsable_inspeccion) 
        ),
        OrdenInspeccion(
            nroOrden=4,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 4, 14, 0),
            fechaHoraFinalizacion=datetime(2025, 5, 4, 16, 0),
            observacion=None,
            estado=estado_completa,
            estacionSismologica=estacion4,
            empleado=empleado_logueado
        ),
        OrdenInspeccion(
            nroOrden=25,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 4, 14, 0),
            fechaHoraFinalizacion=datetime(2023, 5, 7, 13, 30),
            observacion=None,
            estado=estado_pendiente,
            estacionSismologica=estacion5,
            empleado=empleado_logueado
        ),
    ]

    empleado = Empleado(
        nombre="Pepe",
        apellido="Perez",
        telefono=123456789,
        mail="juanp@gmail.com",
        rol=responsable_reparacion
        )


    # Crear un usuario predefinido asociado al empleado
    usuario_test = Usuario(
        nombreusuario="juanp",
        contrasena="1234",
        empleado=empleado_logueado
    )

    gestor = GestorCierreInspeccion(usuario_test, None, None, None, None, None)
    pantalla = PantallaCierreInspeccion(gestor=gestor)