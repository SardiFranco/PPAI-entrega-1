import PantallaCierreInscripcion as PantallaCierreInscripcion
from clases.usuario import Usuario
from clases.ordenInspeccion import OrdenInspeccion

class GestorCierreInscripcion:
    def __init__(self, usuario: Usuario, ordenes: list, motivos, comentario, fechaHoraActual, mail):
        self.usuario = usuario
        self.ordenes = OrdenInspeccion.listaOrdenesInspeccion
        self.motivos = motivos
        self.comentario = comentario
        self.fechaHoraActual = fechaHoraActual
        self.mail = mail

    def buscarRILogueado(self):
        responsable = self.usuario.getRLlogueado()
        if responsable:
            return responsable
        else:
            raise ValueError("No hay un responsable logueado.")

    def ordenarOrdenes(self, ordenes):
        return sorted(ordenes, key=lambda x: x.fechaHoraFinalizacion)
    
    def buscarOrdenes(self):
        ordenes_econtradas = []
        responsable = self.buscarRILogueado()
        for orden in self.ordenes:
            if orden.esDeEmpleado(responsable) and orden.estaCompletamenteRealizada():
                ordenes_econtradas.append(orden)
        return ordenes_econtradas
    