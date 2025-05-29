# Estado

class Estado:
    # Constantes de clase
    AMBITOS = ["OrdenInspección", "Sismografo"]
    listaEstados = []

    # Constructor
    def __init__(self, ambito, nombreEstado: str):
        self.ambito = ambito
        self.nombreEstado = nombreEstado
        Estado.listaEstados.append(self)
    

    def esAmbitoOrdenInspeccion(self):
        return self.ambito == Estado.AMBITOS[0]
    
    def esAmbitoSismografo(self):
        return self.ambito == Estado.AMBITOS[1]
    
    def esCompletamenteRealizada(self):
        return self.nombreEstado == "CompletamenteRealizada"
    
    def esCerrada(self):
        return self.nombreEstado == "Cerrada"
    
    def esFueraDeServicio(self):
        return self.nombreEstado == "FueraDeServicio"

    def getNombreEstado(self):
        return self.nombreEstado