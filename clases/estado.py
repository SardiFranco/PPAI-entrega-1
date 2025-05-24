# Estado

class Estado:
    # Constantes de clase
    AMBITOS = ["OrdenInspección", "Sismografo"]

    # Constructor
    def __init__(self, ambito, nombreEstado: str):
        self.ambito = ambito
        self.nombreEstado = nombreEstado
    
    # Métodos de clase para crear instancias de Estado
    @classmethod
    def paraOrdenInspeccion(cls, nombreEstado: str):
        return cls(cls.AMBITOS[0], nombreEstado)
    
    @classmethod
    def paraSismografo(cls, nombreEstado: str):
        return cls(cls.AMBITOS[1], nombreEstado)

    # Metodos de instancia
    def __str__(self):
        return f"Estado(ambito={self.ambito}, nombre='{self.nombreEstado}')"
    
    def esAmbitoOrdenInspeccion(self):
        return self.ambito == "OrdenInspección"
    
    def esAmbitoSismografo(self):
        return self.ambito == "Sismografo"
    
    def esCompletamenteRealizada(self):
        return self.nombreEstado == "CompletamenteRealizada"
    
    def esCerrada(self):
        return self.nombreEstado == "Cerrada"
    
    def esFueraDeServicio(self):
        return self.nombreEstado == "FueraDeServicio"
