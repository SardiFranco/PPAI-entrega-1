
from clases.usuario import Usuario
from clases.ordenInspeccion import OrdenInspeccion
from clases.motivoTipo import MotivoTipo


class GestorCierreInspeccion:
    def __init__(self, usuario: Usuario, ordenes: list, motivos: list, observacion, fechaHoraActual, mail, ordenSeleccionada=None):
        self.usuario = usuario
        self.ordenes = OrdenInspeccion.listaOrdenesInspeccion
        self.motivos = []
        self.observacion = observacion
        self.fechaHoraActual = fechaHoraActual
        self.mail = mail
        self.ordenSeleccionada = ordenSeleccionada

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
    
    def buscarMotivos(self):
        for motivo in MotivoTipo.listaMotivos:
            self.motivos.append(motivo.getDescripcion())
        return self.motivos
    
    def tomarSeleccionOrden(self, ordenSeleccionada):
        if ordenSeleccionada:
            self.ordenSeleccionada = ordenSeleccionada
            return self.ordenSeleccionada
        else:
            raise ValueError("No se ha seleccionado ninguna orden.")
    
    def tomarObservacion(self, observacion):
        if observacion:
            self.observacion = observacion
            return self.observacion
        else:
            raise ValueError("No se ha ingresado ninguna observación.")