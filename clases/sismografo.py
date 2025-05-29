from clases.estado import Estado
from clases.cambioEstado import CambioEstado
from clases.estacionSismologica import EstacionSismologica
from datetime import datetime

class Sismografo:
    # Constantes de clase
    lista_Sismografos = []

    # Constructor
    def __init__(self, fechaAdquisicion, nroSerie: int, idSismografo: int, estado: Estado, cambiosEstado: list, estacionSismologica: EstacionSismologica):
        self.fechaAdquisicion = fechaAdquisicion
        self.nroSerie = nroSerie
        self.idSismografo = idSismografo
        self.estado = estado
        self.estado.ambito = "Sismografo"
        self.cambiosEstado = cambiosEstado
        self.estacionSismologica = estacionSismologica
        Sismografo.lista_Sismografos.append(self)
    
    @classmethod
    def listaSismografos(cls):
        return cls.lista_Sismografos

    # Metodos de instancia
    def crearCambioEstado(self, nuevoEstado, empleado):
        newCambio = CambioEstado(datetime.now(), None, nuevoEstado, None, empleado)
        self.cambiosEstado.append(newCambio) 
        return newCambio

    def obtenerEstadoActual(self):
        for cambio in self.cambiosEstado: 
            if cambio.esEstadoActual():
                return cambio
        return None

    def setEstadoActual(self, estado):
        self.estado = estado

    def getIdSismografo(self):
        return self.idSismografo
    
    def sosDeEstacionSismologica(self, nombreEstacion):
        if self.estacionSismologica.nombre ==  nombreEstacion:
            return self
    
    def enviarAReparar(self, nuevoEstado, empleado):
        self.obtenerEstadoActual().setFechaHoraFin(datetime.now())
        nuevoCambioEstado = self.crearCambioEstado(nuevoEstado, empleado)
        self.cambiosEstado.append(nuevoCambioEstado)