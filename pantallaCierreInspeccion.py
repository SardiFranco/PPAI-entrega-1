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

        # Botón cancelar (siempre visible en la parte inferior derecha)
        self.boton_cancelar = ttk.Button(self.ventana, text="Cancelar", command=self.mostrar_confirmacion_cancelar)
        self.boton_cancelar.pack(side='bottom', anchor='se', padx=10, pady=10)

        self.ventana.mainloop()

    def mostrar_confirmacion_cancelar(self):
        respuesta = messagebox.askyesno("Confirmar Cancelación", 
                                      "¿Deseas cancelar la operación?",
                                      icon='question')
        if respuesta:
            self.ventana.destroy()
            self.__init__(self.gestor)

    def opcionCerrarOrdenInspeccion(self):
        self.habilitarVentana()

    def habilitarVentana(self):
        self.botonCerrarInspeccion.pack_forget()
        ordenes = self.gestor.opcionCerrarOrdenInspeccion()
        self.mostrarSeleccionOrden(ordenes)
        
    def mostrarSeleccionOrden(self, ordenes):
        columnas = ("Nro Orden", "Fecha Finalización", "Estación", " Id. Sismografo")
        self.listaOrdenes = ttk.Treeview(self.ventana, columns=columnas, show='headings', selectmode='browse')
        for col in columnas:
            self.listaOrdenes.heading(col, text=col)
            self.listaOrdenes.column(col, anchor='center', width=100)

        self.listaOrdenes.pack(expand=True, fill='both', padx=10, pady=10)
        for orden in ordenes:
            self.listaOrdenes.insert("", "end", values=(
                orden['numeroOrden'],
                orden['fechaFinalizacion'].strftime("%Y-%m-%d %H:%M:%S") if orden['fechaFinalizacion'] else "N/A",
                orden['nombreEstacion'],
                orden['idSismografo']
            ))
        self.botonSelecOrden = ttk.Button(self.ventana, text="Seleccionar Orden", command=self.tomarSeleccionOrden)
        self.botonSelecOrden.pack(pady=10)

    def tomarSeleccionOrden(self, event=None):
        seleccion = self.listaOrdenes.selection()
        if seleccion:
            valores = self.listaOrdenes.item(seleccion[0], "values")
            nro_orden = int(valores[0])
            id_sismografo = int(valores[3])

            self.ordenSeleccionada = {
                'nroOrden': nro_orden,
                'idSismografo': id_sismografo
            }
            self.gestor.tomarSeleccionOrden(nro_orden, id_sismografo)

            self.botonSelecOrden.pack_forget()
            self.listaOrdenes.pack_forget()
            print(f"Orden seleccionada: Nro Orden {nro_orden}, ID Sismógrafo {id_sismografo}")
            messagebox.showinfo("Orden Seleccionada", f"Has seleccionado la Orden Nro: {nro_orden}")
            self.pedirObservacion()
        else:
            messagebox.showwarning("Sin selección", "Por favor, selecciona una orden de la tabla.")

    def pedirObservacion(self):
        label_observacion = ttk.Label(self.ventana, text="Ingrese una observación para el cierre:")
        label_observacion.pack(pady=10)

        self.campoObservacion = tk.Text(self.ventana, height=5, width=80)
        self.campoObservacion.pack(pady=10)

        boton_observacion = ttk.Button(self.ventana, text="Tomar Observación", command=self.tomarObservacion)
        boton_observacion.pack(pady=10)

    def tomarObservacion(self, event=None):
        observacion = self.campoObservacion.get("1.0", tk.END).strip()
        if not observacion:
            messagebox.showwarning("Observación Vacía", "Por favor ingrese una observación antes de continuar.")
            return
        else:
            estadosSismografo = self.gestor.tomarObservacion(observacion)
            self.mostrarMenuEstadoSismografo(estadosSismografo)

    def mostrarMenuEstadoSismografo(self, estadosSismografo):
        if self.frameEstado is not None and self.frameEstado.winfo_exists():
            self.frameEstado.destroy()

        self.frameEstado = ttk.Frame(self.ventana)
        self.frameEstado.pack(pady=10, padx=10, fill='both', expand=True)

        label_estado = ttk.Label(self.frameEstado, text="Actualizar situación del sismógrafo:")
        label_estado.pack(pady=10)

        self.estadoSismografo = tk.StringVar()
        print(f"Estados disponibles: {self.estadoSismografo}")
        self.comboboxEstado = ttk.Combobox(self.frameEstado, textvariable=self.estadoSismografo, state="readonly")
        self.comboboxEstado['values'] = estadosSismografo
        try:
            idx_online = [estado.lower() for estado in estadosSismografo].index("online")
            self.comboboxEstado.current(idx_online)
        except ValueError:
            self.comboboxEstado.current(0)
        self.comboboxEstado.pack(pady=10)
        self.comboboxEstado.bind("<<ComboboxSelected>>", lambda event: self.tomarEstadoSismografo())

    def tomarEstadoSismografo(self): 
        self.estadoSeleccionado = self.estadoSismografo.get()
        motivos = self.gestor.tomarEstadoSismografo(self.estadoSeleccionado)
        
        print(f"Estado del sismógrafo tomado: {self.estadoSeleccionado}")
        self.mostrarMotivosFueraDeServicioASelec(motivos=motivos)
        
    def mostrarMotivosFueraDeServicioASelec(self, event=None, motivos=None):
        if self.listaMotivos is not None and self.listaMotivos.winfo_exists():
            self.listaMotivos.destroy()

        if self.estadoSismografo.get() == "Fuera de Servicio":
            self.listaMotivos = ttk.Frame(self.frameEstado)
            self.listaMotivos.pack(pady=10, padx=10, fill='both', expand=True)
            self.check_vars.clear()
            self.comentarios_entries.clear()

            label_motivos = ttk.Label(self.listaMotivos, text="Seleccione uno o varios motivos por los que el sismógrafo está fuera de servicio:")
            label_motivos.pack(pady=5)
            for motivo in motivos:
                print(f"Motivo: {motivo}")
                var = tk.BooleanVar()
                check = ttk.Checkbutton(self.listaMotivos, text=motivo, variable=var)
                check.pack(anchor='w')
                self.check_vars[motivo] = var

                label_coment = ttk.Label(self.listaMotivos, text=f"Comentario para '{motivo}':")
                label_coment.pack(anchor='w', padx=20)
                entry_coment = ttk.Entry(self.listaMotivos, width=80, state='disabled')
                entry_coment.pack(padx=20, pady=2)
                self.comentarios_entries[motivo] = entry_coment

                def toggle_entry(var=var, entry=entry_coment):
                    if var.get():
                        entry.config(state='normal')
                        entry.bind("<FocusOut>", lambda event, entry=entry: on_enter(event, entry))
                    else:
                        entry.delete(0, tk.END)
                        entry.config(state='disabled')

                def on_enter(event, entry):
                    contenido = entry.get().strip()
                    if contenido:
                        self.gestor.tomarComentario(contenido)

                var.trace_add('write', lambda *args, var=var, entry=entry_coment: toggle_entry(var, entry))
            
            self.solicitarConfirmacionCierre()
        else:
            if getattr(self, 'listaMotivos', None) is not None and self.listaMotivos.winfo_exists():
                self.listaMotivos.destroy()

    def solicitarConfirmacionCierre(self):
        self.botonConfirmacionCierreOrden = ttk.Button(self.listaMotivos, text="Confirmar Cierre de Orden", command=self.gestor.tomarConfirmacionCierreOrden)
        self.botonConfirmacionCierreOrden.pack(pady=10)
