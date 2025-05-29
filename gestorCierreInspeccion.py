from clases.usuario import Usuario
from clases.ordenInspeccion import OrdenInspeccion
from clases.motivoTipo import MotivoTipo
from clases.estado import Estado
from tkinter import messagebox
from datetime import datetime
from clases.empleado import Empleado
from interfazNotificacion import InterfazNotificacion
from pantallaCCRS import PantallaCCRS

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
        self.responsable = None
        self.interfazNotificacion = InterfazNotificacion()
        self.pantallaCCRS = PantallaCCRS()
        self.fechaHoraRegistroEstado = None  # Atributo para guardar la fecha y hora del registro del estado

    def opcionCerrarOrdenInspeccion(self):
        responsable = self.buscarRILogueado()
        ordenes = self.buscarOrdenes(responsable)
        ordenes_ordenadas = self.ordenarOrdenes(ordenes)
        return ordenes_ordenadas

    def buscarRILogueado(self):
        self.responsable = self.usuario.getRIlogueado()
        if self.responsable:
            return self.responsable
        else:
            raise ValueError("No hay un responsable logueado.")

    def buscarOrdenes(self, responsable):
        for orden in self.ordenes:
            if orden.esDeEmpleado(responsable) and orden.estaCompletamenteRealizada():
                self.ordenesEncontradas.append(orden.obtenerDatosDeOrden())
        return self.ordenesEncontradas

    def ordenarOrdenes(self, ordenes):
        return sorted(ordenes, key=lambda x: x['fechaFinalizacion'])

    def buscarMotivos(self):
        self.motivos = []
        for motivo in MotivoTipo.listaMotivos:
            self.motivos.append(motivo.getDescripcion())
        return self.motivos

    def tomarSeleccionOrden(self, nroOrden, idSismografo):
        for orden in self.ordenes:
            if orden.getNumeroOrden() == nroOrden:
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
        esCorrecto = self.validarDatosMinimosParaCierre()
        if esCorrecto:
            estado_cerrado = self.buscarEstadoCierreDeOI()
            estado_FueraServicio = self.buscarEstadoFueraDeServicioSismografo()
            fechaActual = self.getFechaHoraActual()
            self.fechaHoraRegistroEstado = fechaActual.strftime("%Y-%m-%d %H:%M:%S")
            resultado = self.cerrarOrdenInspeccion(estado_cerrado, estado_FueraServicio, fechaActual)
            return resultado  # <-- aseguramos retornar el resultado
        else:
            messagebox.showerror("Error", "Debe completar todos los campos requeridos para cerrar la orden de inspección.")
            return False

    def validarDatosMinimosParaCierre(self):
        if self.observacion and len(self.comentariosfueraServicio) > 0:
            return True
        else:
            return False 

    def cerrarOrdenInspeccion(self, estado_cerrado, estado_fuera_servicio, fechaActual):
        if self.ordenSeleccionada:
            self.ordenSeleccionada.cerrar(estado_cerrado, fechaActual)
            messagebox.showinfo("Cierre de Orden", "La orden de inspección se ha cerrado correctamente.")
            self.enviarSismografoParaReparar(estado_fuera_servicio, self.idSismografo)
            return True  # <-- devuelve True si se cerró bien
        else:
            messagebox.showerror("Error", "No se puede cerrar la orden. Verifique los datos ingresados.")
            return False  # <-- devuelve False si algo falló

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
                self.ordenSeleccionada.enviarSismografoParaReparacion(estado_fuera_servicio, id_sismografo, self.responsable)
                self.obtenerMailResponsableReparacion()
                self.publicarEnMonitores()
                print(f"Sismógrafo {self.ordenSeleccionada.estacionSismologica.obtenerIdSismografo()} enviado para reparación.")
            else:
                messagebox.showerror("Error", "No se encontró el estado 'Fuera de Servicio' para el sismógrafo.")  
        else:
            messagebox.showerror("Error", "No hay una orden seleccionada para enviar el sismógrafo a reparación.")

    def tomarEstadoSismografo(self, estado):
        self.estadoSeleccionadoSismografo = estado
        return self.buscarMotivos()

    def obtenerMailResponsableReparacion(self):
        lista_mail = []
        for empleado in Empleado.listadoEmpleados:
            if empleado.esResponsableReparacion():
                lista_mail.append(empleado.obtenerMail())
        self.enviarNotificacionesPorMail(lista_mail)

    def enviarNotificacionesPorMail(self, lista_mail):
        self.interfazNotificacion.enviarMail(lista_mail)

    def publicarEnMonitores(self):
        estado_FueraServicio = self.buscarEstadoFueraDeServicioSismografo()
        self.pantallaCCRS.publicar(self.idSismografo, estado_FueraServicio, self.fechaHoraRegistroEstado, self.comentariosfueraServicio)
