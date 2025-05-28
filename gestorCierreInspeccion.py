
from clases.usuario import Usuario
from clases.ordenInspeccion import OrdenInspeccion
from clases.motivoTipo import MotivoTipo
from clases.estado import Estado
from tkinter import messagebox
from datetime import datetime

class GestorCierreInspeccion:
    def __init__(self, usuario: Usuario, ordenes: list, motivos: list, observacion, fechaHoraActual, mail, ordenSeleccionada=None, comentariosfueraServicio=None):
        self.usuario = usuario
        self.ordenes = OrdenInspeccion.listaOrdenesInspeccion
        self.motivos = []
        self.observacion = observacion
        self.fechaHoraActual = fechaHoraActual
        self.mail = mail
        self.ordenSeleccionada = ordenSeleccionada
        self.comentariosfueraServicio = []

    def opcionCerrarOrdenInspeccion(self):
        responsable = self.buscarRILogueado()
        ordenes = self.buscarOrdenes(responsable)
        ordenes_ordenadas = self.ordenarOrdenes(ordenes)
        return ordenes_ordenadas

    def buscarRILogueado(self):
        responsable = self.usuario.getRLlogueado()
        if responsable:
            return responsable
        else:
            raise ValueError("No hay un responsable logueado.")

    def buscarOrdenes(self, responsable):
        ordenes_econtradas = []
        responsable = self.buscarRILogueado()
        for orden in self.ordenes:
            if orden.esDeEmpleado(responsable) and orden.estaCompletamenteRealizada():
                ordenes_econtradas.append(orden)
        return ordenes_econtradas

    def ordenarOrdenes(self, ordenes):
        return sorted(ordenes, key=lambda x: x.fechaHoraFinalizacion)
    
    def buscarMotivos(self):
        self.motivos = []
        for motivo in MotivoTipo.listaMotivos:
            self.motivos.append(motivo.getDescripcion())
        return self.motivos
    
    def tomarSeleccionOrden(self, orden):
        self.ordenSeleccionada = orden
    
    def tomarObservacion(self, observacion):
        self.observacion = observacion

    def tomarComentario(self, comentario):
        print("Tomando comentario fuera de servicio...")
        self.comentariosfueraServicio.append(comentario)

    def tomarConfirmacionCierreOrden(self):
        if self.validarDatosMinimosParaCierre():
            self.cerrarOrdenInspeccion()
        else:
            messagebox.showerror("Error", "Falta ingresar una observación o un comentario en motivos.")

    def validarDatosMinimosParaCierre(self):
        return self.observacion and len(self.comentariosfueraServicio) > 0
    
    def cerrarOrdenInspeccion(self):
        if self.ordenSeleccionada:
            self.ordenSeleccionada.cerrar(self.buscarEstadoCierreDeOI())
            messagebox.showinfo("Cierre de Orden", "La orden de inspección se ha cerrado correctamente.")
            print(f"Orden cerrada: {self.ordenSeleccionada.mostrarDatosDeOrden()}" \
                  f" con observación: {self.observacion} y motivos fuera de servicio: {self.comentariosfueraServicio}")
        else:
            messagebox.showerror("Error", "No se puede cerrar la orden. Verifique los datos ingresados.")
    
    def buscarEstadoCierreDeOI(self):
        for estado in Estado.listaEstados:
            if estado.esAmbitoOrdenInspeccion() and estado.esCerrada():
                return estado

    def buscarEstadoFueraDeServicioSismografo(self):
        for estado in Estado.listaEstados:
            if estado.esAmbitoSismografo() and estado.esFueraDeServicio():
                return estado
            
    def getFechaHoraActual(self):
        self.fechaHoraActual = datetime.now()
    