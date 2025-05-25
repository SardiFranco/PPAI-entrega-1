import clases.sismografo as Sismografo

class EstacionSismologica:
    def __init__(self, codigoEstacion, latitud, longitud, nombre):
        self.codigoEstacion = codigoEstacion
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud  
    
    def getCodigoEstacion(self):
        return self.codigoEstacion
    
    def getNombre(self):
        return self.nombre
    
    def obtenerIdSismografo(self):
        for sismografo in Sismografo.listaSismografos:
            if sismografo.sosDeEstacionSismologica(self.nombre):
                return sismografo.getIdSismografo()
    