from clases.estado import Estado

class CambioEstado:

    # Constructor
    def __init__(self, fechaHoraInicio, fechaHoraFin, estado: Estado, motivoFueraServicio):
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin
        self.estado = estado
        self.motivoFueraServicio = motivoFueraServicio
    
    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin
     
    def esEstadoActual(self):
        return self.fechaHoraFin is None
    
    def crearMotivoFueraServicio(self, motivoFueraServicio):
        self.motivoFueraServicio = motivoFueraServicio