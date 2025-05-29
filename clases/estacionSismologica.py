
class EstacionSismologica:
    def __init__(self, codigoEstacion, latitud, longitud, nombre: str):
        self.codigoEstacion = codigoEstacion
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud  
    
    def getCodigoEstacion(self):
        return self.codigoEstacion
    
    def getNombre(self):
        return self.nombre
    
    def obtenerIdSismografo(self):
        from clases.sismografo import Sismografo
        for sismografo in Sismografo.listaSismografos():
            if sismografo.sosDeEstacionSismologica(self.nombre):
                return sismografo.getIdSismografo()
    
   # def ponerSismografoFueraServicio(self, nuevoEstado, idSismografo):
    #    from clases.sismografo import Sismografo
        
     #   sismografo = Sismografo.listaSismografos()
     #   for s in sismografo:
    #      if s.getIdSismografo() == idSismografo:
                
    


