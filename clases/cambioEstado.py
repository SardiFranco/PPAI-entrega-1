import clases.estado as Estado
import clases.empleado as Empleado

class CambioEstado:

    # Constructor
    def __init__(self, fechaHoraInicio, fechaHoraFin, estado: Estado, motivoFueraServicio, empleado: Empleado):
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin
        self.estado = estado
        self.motivoFueraServicio = motivoFueraServicio
        self.empleado = empleado
    
    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin
     
    def esEstadoActual(self):
        return self.fechaHoraFin is None
    
    def crearMotivoFueraServicio(self, motivoFueraServicio):
        self.motivoFueraServicio = motivoFueraServicio