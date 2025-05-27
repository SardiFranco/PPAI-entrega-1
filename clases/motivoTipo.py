class MotivoTipo:
    listaMotivos = []

    def __init__(self, desc: str):
        self.descripcion = desc
        MotivoTipo.listaMotivos.append(self)

    def getDescripcion(self):
        return(self.descripcion)