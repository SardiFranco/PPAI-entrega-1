# ...existing code...

if __name__ == "__main__":
    # Importa la clase Estado correctamente
    from clases.estado import Estado
    from clases.ordenInspeccion import OrdenInspeccion
    from datetime import datetime

    # Instancias de Estado
    estado_pendiente = Estado.paraOrdenInspeccion("Pendiente")
    estado_completa = Estado.paraOrdenInspeccion("CompletamenteRealizada")

    # Lista de órdenes de inspección para testeo
    ordenes_test = [
        OrdenInspeccion(
            nroOrden=1,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 1, 9, 0),
            fechaHoraFinalizacion=None,
            observacion=None,
            estado=estado_pendiente
        ),
        OrdenInspeccion(
            nroOrden=2,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 2, 10, 0),
            fechaHoraFinalizacion=datetime(2025, 5, 2, 12, 0),
            observacion=None,
            estado=estado_completa
        ),
        OrdenInspeccion(
            nroOrden=3,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 3, 8, 30),
            fechaHoraFinalizacion=None,
            observacion=None,
            estado=estado_pendiente
        ),
        OrdenInspeccion(
            nroOrden=4,
            fechaHoraCierre=None,
            fechaHoraInicio=datetime(2025, 5, 4, 14, 0),
            fechaHoraFinalizacion=datetime(2025, 5, 4, 16, 0),
            observacion=None,
            estado=estado_completa
        ),
    ]

    # Imprime las órdenes para verificar
    for orden in ordenes_test:
        print(f"Nro: {orden.nroOrden}, Estado: {orden.estado.nombreEstado}, "
              f"Inicio: {orden.fechaHoraInicio}, Finalización: {orden.fechaHoraFinalizacion}, "
              f"Cierre: {orden.fechaHoraCierre}, Observación: {orden.observacion}")