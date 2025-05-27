import tkinter as tk
from tkinter import ttk, messagebox
import clases.usuario as Usuario
from gestorCierreInspeccion import GestorCierreInspeccion

class PantallaCierreInspeccion:
 
    def __init__(self,gestor, listaOrdenes=None, listaMotivos=None, botonCerrarInspeccion=None, 
                 botonConfirmacionCierreOrden=None, seleccionOrden=None, campoObservacion=None, botonSelecOrden=None):
        
        self.gestor = gestor
        self.listaOrdenes = listaOrdenes
        self.listaMotivos = listaMotivos
        self.botonCerrarInspeccion = botonCerrarInspeccion
        self.botonConfirmacionCierreOrden = botonConfirmacionCierreOrden
        self.seleccionOrden = seleccionOrden
        self.campoObservacion = campoObservacion
        self.botonSelecOrden = botonSelecOrden

        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Pantalla de Cierre de Orden de Inspección")
        self.ventana.geometry("1200x600")

        # Botón para cerrar inscripción
        self.botonCerrarInspeccion = ttk.Button(self.ventana, text="Cerrar Orden de Inspección", command=self.opcionCerrarOrdenInspeccion)
        self.botonCerrarInspeccion.pack(pady=10)

        self.ventana.mainloop()


    # Métodos de pantalla
    def opcionCerrarOrdenInspeccion(self):
        self.botonCerrarInspeccion.pack_forget()  # Ocultar el botón de cerrar inscripción
        self.mostrarListaOrdenes()
        self.botonSelecOrden = ttk.Button(self.ventana, text="Seleccionar Orden", command=self.tomarSeleccionOrden)
        self.botonSelecOrden.pack(pady=10)


    def mostrarListaOrdenes(self):
        # Crea un label que muestra el nombre del responsable logueado
        responsable = self.gestor.buscarRILogueado()
        label_responsable = ttk.Label(self.ventana, text=f"Responsable Logueado: {responsable.nombre} {responsable.apellido}")
        label_responsable.pack(pady=10)

        # Crea la estructura de la tabla y rellena con las órdenes de inspección
        columnas = ("Nro Orden", "Fecha Finalización", "Estación", " Id. Sismografo")
        self.listaOrdenes = ttk.Treeview(self.ventana, columns=columnas, show='headings', selectmode='browse')
        for col in columnas:
            self.listaOrdenes.heading(col, text=col)
            self.listaOrdenes.column(col, anchor='center', width=100)

        self.listaOrdenes.pack(expand=True, fill='both', padx=10, pady=10)

        ordenes_filtradas = self.gestor.buscarOrdenes()
        ordenes_ordenadas = self.gestor.ordenarOrdenes(ordenes_filtradas)

        for orden in ordenes_ordenadas:
            self.listaOrdenes.insert("", "end", values=(
                orden.nroOrden,
                orden.fechaHoraFinalizacion.strftime("%Y-%m-%d %H:%M:%S") if orden.fechaHoraFinalizacion else "N/A",
                orden.estacionSismologica.nombre,
                orden.estacionSismologica.obtenerIdSismografo(),
            ))

    def tomarSeleccionOrden(self, event=None):
        seleccion = self.listaOrdenes.selection()
        if seleccion:
            valores = self.listaOrdenes.item(seleccion[0], "values")
            nro_orden = valores[0]
            for orden in self.gestor.ordenes:
                if orden.nroOrden == int(nro_orden):
                    self.gestor.ordenSeleccionada = orden
                    self.gestor.tomarSeleccionOrden(orden)

                    self.botonSelecOrden.pack_forget()  # Ocultar el botón de selección de orden
                    self.listaOrdenes.pack_forget()  # Ocultar la lista de órdenes
                    print(f"Orden seleccionada: {orden.mostrarDatosDeOrden()}")

                    self.pedirObservacion()
        else:
            messagebox.showwarning("Sin selección", "Por favor, selecciona una orden de la tabla.")
    
    def pedirObservacion(self):
        label_observacion = ttk.Label(self.ventana, text="Ingrese una observación para el cierre:")
        label_observacion.pack(pady=10)

        self.campoObservacion = tk.Text(self.ventana, height=5, width=80)
        self.campoObservacion.pack(pady=10)

        botonConfObservacion = ttk.Button(self.ventana, text="Confirmar Observación", command=lambda: self.tomarObservacion(botonConfObservacion))
        botonConfObservacion.pack(pady=10)

    def tomarObservacion(self,botonConfObservacion, event=None):
        observacion = self.campoObservacion.get("1.0", tk.END).strip()
        if not observacion:
            messagebox.showwarning("Observación Vacía", "Por favor ingrese una observación antes de continuar.")
            return
        self.gestor.observacion = observacion
        print(f"Observación ingresada: {self.gestor.observacion}")
        self.campoObservacion.pack_forget()
        botonConfObservacion.pack_forget()
        self.mostrarMotivosFueraDeServicioASelec()

    def mostrarMotivosFueraDeServicioASelec(self, event=None):
        # Limpiar cualquier motivo previo
        if hasattr(self, 'ListaMotivos'):
            self.ListaMotivos.destroy()
       
        self.ListaMotivos = ttk.Frame(self.ventana)
        self.ListaMotivos.pack(pady=10)
       
        label_motivos = ttk.Label(self.ListaMotivos, text="Seleccione los motivos para poner el sismógrafo fuera de servicio:")
        label_motivos.pack(pady=5)

        # Crear un diccionario para almacenar las variables de los checkboxes
        self.check_vars = {}
        self.comentarios = {}
        # Iterar sobre la lista de motivos y crear un checkbox para cada uno
        for motivo in self.gestor.buscarMotivos():
            var = tk.BooleanVar()
            self.check_vars[motivo] = var

            frame_motivo = ttk.Frame(self.ListaMotivos)
            frame_motivo.pack(anchor='w', padx=10, pady=5, fill='x')

            # Crear un campo de texto para el comentario del motivo
            entry = ttk.Entry(frame_motivo, width=50)
            self.comentarios[motivo] = entry

            check = ttk.Checkbutton(frame_motivo, text=motivo, variable=var, command=lambda v=var, e=entry: self.solicitarComentarioMotivo(v, e))
            check.pack(anchor='w', padx=10)
    
    def solicitarComentarioMotivo(self, v, e):
                if v.get():
                    e.pack(pady=5)
                    print("ok")
                else:
                    e.delete(0, tk.END)  # Limpiar el campo de texto
                    e.pack_forget()

    def confirmarCierreOrden(self):
        observacion = self.campoObservacion.get("1.0", tk.END).strip()
        if not observacion:
            messagebox.showwarning("Observación Vacía", "Por favor ingrese una observación antes de confirmar.")
            return

        estado = self.estadoSismografo.get()
        motivos_seleccionados = []
        comentarios_motivos = {}

        if estado == "Fuera de servicio":
            for motivo, var in self.check_vars.items():
                if var.get():
                    comentario = self.comentarios[motivo].get().strip()
                    if not comentario:
                        messagebox.showwarning("Comentario Faltante", f"Por favor ingrese un comentario para el motivo '{motivo}'.")
                        return
                    motivos_seleccionados.append(motivo)
                    comentarios_motivos[motivo] = comentario

            if not motivos_seleccionados:
                messagebox.showwarning("Motivos Faltantes", "Por favor seleccione al menos un motivo para poner el sismógrafo fuera de servicio.")
                return

        # Aquí llamarías al gestor para registrar el cierre
        print("Observación:", observacion)
        print("Estado:", estado)
        print("Motivos seleccionados:", motivos_seleccionados)
        print("Comentarios por motivo:", comentarios_motivos)

        messagebox.showinfo("Cierre Confirmado", "La orden de inspección ha sido cerrada exitosamente.")
