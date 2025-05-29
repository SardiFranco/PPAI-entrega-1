from clases.usuario import Usuario
from clases.ordenInspeccion import OrdenInspeccion
from clases.motivoTipo import MotivoTipo
from clases.estado import Estado
from tkinter import messagebox
from datetime import datetime

class GestorCierreInspeccion:
    def __init__(self, usuario: Usuario, ordenes: list, motivos: list, observacion, fechaHoraActual, mail, ordenSeleccionada=None, comentariosfueraServicio=None, idSismografo=None, ordenesEncontradas=None):
        self.usuario = usuario
        self.ordenes = OrdenInspeccion.listaOrdenesInspeccion
        self.motivos = []
        self.observacion = observacion
        self.fechaHoraActual = datetime.now()
        self.mail = mail
        self.ordenSeleccionada = ordenSeleccionada
        self.idSismografo = idSismografo
        self.ordenesEncontradas = []
        self.comentariosfueraServicio = []
        self.estadoSeleccionadoSismografo = None  # nuevo atributo para guardar el estado seleccionado

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
        for orden in self.ordenes:
            if orden.esDeEmpleado(responsable) and orden.estaCompletamenteRealizada():
                self.ordenesEncontradas.append(orden.obtenerDatosDeOrden())
                print(f"Orden encontrada: {orden.obtenerDatosDeOrden()}")
        return self.ordenesEncontradas

    def ordenarOrdenes(self, ordenes):
        return sorted(ordenes, key=lambda x: x['fechaFinalizacion'])

    def buscarMotivos(self):
        self.motivos = []
        for motivo in MotivoTipo.listaMotivos:
            self.motivos.append(motivo.getDescripcion())
        return self.motivos

    def tomarSeleccionOrden(self, orden, idSismografo):
        self.ordenSeleccionada = orden
        self.idSismografo = idSismografo

    def tomarObservacion(self, observacion):
        self.observacion = observacion
        estadosSismografo = self.buscarEstadosSismografo()
        return estadosSismografo

    def buscarEstadosSismografo(self):
        estados = []
        for estado in Estado.listaEstados:
            if estado.esAmbitoSismografo():
                estados.append(estado.getNombreEstado())
        return estados

    def tomarComentario(self, comentario):
        self.comentariosfueraServicio.append(comentario)

    def tomarConfirmacionCierreOrden(self):
        self.validarDatosMinimosParaCierre()

    def validarDatosMinimosParaCierre(self):
        if self.observacion and len(self.comentariosfueraServicio) > 0:
            estado_cerrado = self.buscarEstadoCierreDeOI()
            estado_FueraServicio = self.buscarEstadoFueraDeServicioSismografo()
            fechaActual = self.getFechaHoraActual()
            self.cerrarOrdenInspeccion(estado_cerrado, estado_FueraServicio, fechaActual)
        else:
            messagebox.showerror("Error", "Debe completar la observación y al menos un motivo fuera de servicio para cerrar la orden.")

    def cerrarOrdenInspeccion(self, estado_cerrado, estado_fuera_servicio, fechaActual):
        if self.ordenSeleccionada:
            self.ordenSeleccionada.cerrar(estado_cerrado, fechaActual)
            messagebox.showinfo("Cierre de Orden", "La orden de inspección se ha cerrado correctamente.")
            print(f"Orden cerrada: {self.ordenSeleccionada.mostrarDatosDeOrden()}" \
                  f" con observación: {self.observacion} y motivos fuera de servicio: {self.comentariosfueraServicio}")
            self.enviarSismografoParaReparar(estado_fuera_servicio, self.idSismografo)
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
        return self.fechaHoraActual

    def enviarSismografoParaReparar(self, estado_fuera_servicio, id_sismografo):
        if self.ordenSeleccionada:
            if estado_fuera_servicio:
                self.ordenSeleccionada.enviarSismografoParaReparacion(estado_fuera_servicio, id_sismografo)
                print(f"Sismógrafo {self.ordenSeleccionada.estacionSismologica.obtenerIdSismografo()} enviado para reparación.")
            else:
                messagebox.showerror("Error", "No se encontró el estado 'Fuera de Servicio' para el sismógrafo.")
        else:
            messagebox.showerror("Error", "No hay una orden seleccionada para enviar el sismógrafo a reparación.")

    def tomarEstadoSismografo(self, estado):
        self.estadoSeleccionadoSismografo = estado
        return self.buscarMotivos()
