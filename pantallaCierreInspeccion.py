import tkinter as tk
from tkinter import ttk, messagebox
import clases.usuario as Usuario
from gestorCierreInspeccion import GestorCierreInspeccion

class PantallaCierreInspeccion:

    def __init__(self, gestor, listaOrdenes=None, listaMotivos=None, botonCerrarInspeccion=None,
        botonConfirmacionCierreOrden=None, campoObservacion=None, botonSelecOrden=None, frameEstado=None):
        
        self.gestor = gestor
        self.listaOrdenes = listaOrdenes
        self.listaMotivos = None
        self.botonCerrarInspeccion = botonCerrarInspeccion
        self.botonConfirmacionCierreOrden = botonConfirmacionCierreOrden
        self.campoObservacion = campoObservacion
        self.botonSelecOrden = botonSelecOrden
        self.frameEstado = frameEstado

        self.ordenSeleccionada = None
        self.check_vars = {}
        self.comentarios_entries = {}

        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Pantalla de Cierre de Orden de Inspección")
        self.ventana.geometry("1200x700")

        # Botón para cerrar inscripción
        self.botonCerrarInspeccion = ttk.Button(self.ventana, text="Cerrar Orden de Inspección", command=self.opcionCerrarOrdenInspeccion)
        self.botonCerrarInspeccion.pack(pady=10)

        self.ventana.mainloop()


    # Métodos de pantalla

    def opcionCerrarOrdenInspeccion(self):
        self.habilitarVentana()

    def habilitarVentana(self):
        self.botonCerrarInspeccion.pack_forget()
        ordenes = self.gestor.opcionCerrarOrdenInspeccion()
        self.mostrarSeleccionOrden(ordenes)
        
        
    def mostrarSeleccionOrden(self, ordenes):
        #label_responsable = ttk.Label(self.ventana, text=f"Responsable Logueado: {responsable.nombre} {responsable.apellido}")
        #label_responsable.pack(pady=10)

        # Crea la estructura de la tabla y rellena con las órdenes de inspección
        columnas = ("Nro Orden", "Fecha Finalización", "Estación", " Id. Sismografo")
        self.listaOrdenes = ttk.Treeview(self.ventana, columns=columnas, show='headings', selectmode='browse')
        for col in columnas:
            self.listaOrdenes.heading(col, text=col)
            self.listaOrdenes.column(col, anchor='center', width=100)

        self.listaOrdenes.pack(expand=True, fill='both', padx=10, pady=10)
        for orden in ordenes:
            self.listaOrdenes.insert("", "end", values=(
                orden.nroOrden,
                orden.fechaHoraFinalizacion.strftime("%Y-%m-%d %H:%M:%S") if orden.fechaHoraFinalizacion else "N/A",
                orden.estacionSismologica.nombre,
                orden.estacionSismologica.obtenerIdSismografo(),
            ))
        self.botonSelecOrden = ttk.Button(self.ventana, text="Seleccionar Orden", command=self.tomarSeleccionOrden)
        self.botonSelecOrden.pack(pady=10)

    def tomarSeleccionOrden(self, event=None):
        seleccion = self.listaOrdenes.selection()
        if seleccion:
            valores = self.listaOrdenes.item(seleccion[0], "values")
            nro_orden = valores[0]
            for orden in self.gestor.ordenes:
                if orden.nroOrden == int(nro_orden):
                    self.ordenSeleccionada = orden
                    self.gestor.tomarSeleccionOrden(orden)
                    self.botonSelecOrden.pack_forget()
                    self.listaOrdenes.pack_forget()
                    print(f"Orden seleccionada: {orden.mostrarDatosDeOrden()}")
                    messagebox.showinfo("Orden Seleccionada", f"Has seleccionado la Orden Nro: {nro_orden}")
                    self.pedirObservacion()
                    break
        else:
            messagebox.showwarning("Sin selección", "Por favor, selecciona una orden de la tabla.")
        

    def pedirObservacion(self):
        label_observacion = ttk.Label(self.ventana, text="Ingrese una observación para el cierre:")
        label_observacion.pack(pady=10)

        self.campoObservacion = tk.Text(self.ventana, height=5, width=80)
        self.campoObservacion.pack(pady=10)  # Permitir tomar observación con Enter

        boton_observacion = ttk.Button(self.ventana, text="Tomar Observación", command=self.tomarObservacion)
        boton_observacion.pack(pady=10)

    def tomarObservacion(self, event=None):
        observacion = self.campoObservacion.get("1.0", tk.END).strip()
        if not observacion:
            messagebox.showwarning("Observación Vacía", "Por favor ingrese una observación antes de continuar.")
            return
        else:
            self.gestor.tomarObservacion(observacion)
            self.gestor.buscarMotivos()
            self.mostrarMenuEstadoSismografo()

    def mostrarMenuEstadoSismografo(self):
        # MENÚ DESPLEGABLE para estado del sismógrafo
        if self.frameEstado is not None and self.frameEstado.winfo_exists():
            self.frameEstado.destroy()

        self.frameEstado = ttk.Frame(self.ventana)
        self.frameEstado.pack(pady=10, padx=10, fill='both', expand=True)

        label_estado = ttk.Label(self.frameEstado, text="Actualizar situación del sismógrafo:")
        label_estado.pack(pady=10)

        self.estadoSismografo = tk.StringVar()
        self.comboboxEstado = ttk.Combobox(self.frameEstado, textvariable=self.estadoSismografo, state="readonly")
        self.comboboxEstado['values'] = ("On-line", "Fuera de servicio")
        self.comboboxEstado.current(0)
        self.comboboxEstado.pack(pady=10)
        self.comboboxEstado.bind("<<ComboboxSelected>>", self.mostrarMotivosFueraDeServicioSelec)


    def mostrarMotivosFueraDeServicioSelec(self, event=None):
        motivos = self.gestor.motivos
        if self.listaMotivos is not None and self.listaMotivos.winfo_exists():
            self.listaMotivos.destroy()

        # Mostrar motivos solo si el estado es "Fuera de servicio"
        if self.estadoSismografo.get() == "Fuera de servicio":
            self.listaMotivos = ttk.Frame(self.frameEstado)
            self.listaMotivos.pack(pady=10, padx=10, fill='both', expand=True)
            self.check_vars.clear()
            self.comentarios_entries.clear()

            label_motivos = ttk.Label(self.listaMotivos, text="Seleccione uno o varios motivos por los que el sismógrafo está fuera de servicio:")
            label_motivos.pack(pady=5)

            for motivo in motivos:
                var = tk.BooleanVar()
                check = ttk.Checkbutton(self.listaMotivos, text=motivo, variable=var)
                check.pack(anchor='w')
                self.check_vars[motivo] = var

                label_coment = ttk.Label(self.listaMotivos, text=f"Comentario para '{motivo}':")
                label_coment.pack(anchor='w', padx=20)
                entry_coment = ttk.Entry(self.listaMotivos, width=80, state='disabled')  # inicialmente deshabilitado
                entry_coment.pack(padx=20, pady=2)
                self.comentarios_entries[motivo] = entry_coment

                # Asociar callback para habilitar/deshabilitar el Entry
                def toggle_entry(var=var, entry=entry_coment):
                    if var.get():
                        entry.config(state='normal')
                        entry.bind("<FocusOut>", lambda event, entry=entry: on_enter(event, entry))  # Permitir tomar comentario con Enter
                    else:
                        entry.delete(0, tk.END)
                        entry.config(state='disabled')

                def on_enter(event, entry):
                    contenido = entry.get().strip()
                    if contenido:
                        self.gestor.tomarComentario(contenido)

                var.trace_add('write', lambda *args, var=var, entry=entry_coment: toggle_entry(var, entry))
            
            # boton de confirmación para cerrar la orden
            self.solicitarConfirmacionCierre()

        else:
            if hasattr(self, 'listaMotivos') and self.listaMotivos.winfo_exists():
                self.listaMotivos.destroy()

    def solicitarConfirmacionCierre(self):
            self.botonConfirmacionCierreOrden = ttk.Button(self.listaMotivos, text="Confirmar Cierre de Orden", command=self.gestor.tomarConfirmacionCierreOrden)
            self.botonConfirmacionCierreOrden.pack(pady=10)

    