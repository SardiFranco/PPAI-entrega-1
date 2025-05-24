# Modulos

from datetime import datetime, date, time
import clases.estado as Estado

# Orden de Inspección
class OrdenInspeccion:
    def __init__(self, nroOrden: int, fechaHoraCierre, fechaHoraInicio, fechaHoraFinalizacion, observacion: str, estado: Estado):
        self.nroOrden = nroOrden
        self.fechaHoraCierre = fechaHoraCierre
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFinalizacion = fechaHoraFinalizacion
        self.observacion = observacion
        self.estado = estado
        self.estado.ambito = "OrdenInspección"
    
    def getNumeroOrden(self):
        return self.nroOrden
    
    def getFechaFinalizacion(self):
        return self.fechaHoraFinalizacion
    
    def setFechaHoraCierre(self, fechaHoraCierre):
        self.fechaHoraCierre = fechaHoraCierre
    
    def setEstado(self, estado):
        self.estado.nombreEstado = estado.nombreEstado
    
    def cerrar(self):
        self.setFechaHoraCierre(datetime.now())
        self.setEstado(Estado.paraOrdenInspeccion("Cerrada"))