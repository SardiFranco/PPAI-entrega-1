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
    
    def getNumeroOrden(self):
        return self.nroOrden
    
    def getFechaFinalizacion(self):
        return self.fechaHoraFinalizacion

    def setFechaHoraCierre(self, fechaHoraCierre): 
        self.fechaHoraCierre = fechaHoraCierre
    
    def setEstado(self, nombreEstado):
        self.estado.nombreEstado = nombreEstado
    
    def cerrar(self, nuevoEstado, fechaHoraCierre):
        self.setFechaHoraCierre(fechaHoraCierre)
        self.setEstado(nuevoEstado)

    def estaCompletamenteRealizada(self):
        return self.estado.esCompletamenteRealizada()
    
    def mostrarDatosDeOrden(self):
        return f"Nro Orden: {self.nroOrden}, ID Sismografo: {str(self.estacionSismologica.obtenerIdSismografo())}, " \
            f"Estado: {self.estado.getNombreEstado()}, " \
            f"Fecha Inicio: {self.fechaHoraInicio}, Fecha Finalización: {self.fechaHoraFinalizacion}, " \
            f"Fecha Cierre: {self.fechaHoraCierre}"
    
    def obtenerDatosDeOrden(self):
        nombre = self.estacionSismologica.getNombre()
        idSismografo = self.estacionSismologica.obtenerIdSismografo()
        numeroOrden = self.getNumeroOrden()
        fechaFinalizacion = self.getFechaFinalizacion()
        return {
            "nombreEstacion": nombre,
            "idSismografo": idSismografo,
            "numeroOrden": numeroOrden,
            "fechaFinalizacion": fechaFinalizacion,
            "estado": self.estado.nombreEstado
        }
    
    def esDeEmpleado(self, empleado: Empleado):
        return self.empleado == empleado
    
    def enviarSismografoParaReparacion(self, nuevoEstado, idSismografo, empleado):
        self.estacionSismologica.ponerSismografoFueraServicio(nuevoEstado, idSismografo, empleado)
