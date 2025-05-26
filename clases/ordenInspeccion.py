from datetime import datetime, date, time
import clases.estado as Estado
import clases.estacionSismologica as EstacionSismologica
import clases.empleado as Empleado

# Orden de Inspección
class OrdenInspeccion:
    listaOrdenesInspeccion = []

    def __init__(self, nroOrden: int, fechaHoraCierre, fechaHoraInicio, fechaHoraFinalizacion, observacion: str, estado: Estado, estacionSismologica: EstacionSismologica, empleado: Empleado):
        self.nroOrden = nroOrden
        self.fechaHoraCierre = fechaHoraCierre
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFinalizacion = fechaHoraFinalizacion
        self.observacion = observacion
        self.estado = estado
        self.estado.ambito = "OrdenInspección"
        self.estacionSismologica = estacionSismologica
        self.empleado = empleado
        OrdenInspeccion.listaOrdenesInspeccion.append(self)

    def setFechaHoraCierre(self, fechaHoraCierre): 
        self.fechaHoraCierre = fechaHoraCierre
    
    def setEstado(self, estado):
        self.estado.nombreEstado = estado.nombreEstado
    
    def cerrar(self):
        self.setFechaHoraCierre(datetime.now())
        self.setEstado(Estado.paraOrdenInspeccion("Cerrada"))

    def estaCompletamenteRealizada(self):
        return self.estado.esCompletamenteRealizada()
    
    def mostrarDatosDeOrden(self):
        return f"Nro Orden: {self.nroOrden}, ID Sismografo: {str(self.estacionSismologica.obtenerIdSismografo)}, " \
               f"Estado: {self.estado.nombreEstado}, " \
               f"Fecha Inicio: {self.fechaHoraInicio}, Fecha Finalización: {self.fechaHoraFinalizacion}, " \
               f"Fecha Cierre: {self.fechaHoraCierre}"
    
    def esDeEmpleado(self, empleado: Empleado):
        return self.empleado == empleado