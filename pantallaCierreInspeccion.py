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
                    self.ordenSeleccionada = orden
                    self.botonSelecOrden.pack_forget()  # Ocultar el botón de selección de orden
                    self.listaOrdenes.pack_forget()  # Ocultar la lista de órdenes
                    print(f"Orden seleccionada: {orden.mostrarDatosDeOrden()}")
                    messagebox.showinfo("Orden Seleccionada", f"Has seleccionado la Orden Nro: {nro_orden}")
                    break
        else:
            messagebox.showwarning("Sin selección", "Por favor, selecciona una orden de la tabla.")
    
