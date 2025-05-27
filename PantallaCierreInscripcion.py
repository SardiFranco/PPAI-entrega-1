import tkinter as tk
from tkinter import ttk, messagebox
import clases.usuario as Usuario
from gestorCierreInscripcion import GestorCierreInscripcion

class PantallaCierreInscripcion:
 
    def __init__(self,gestor, listaOrdenes=None, listaMotivos=None, botonCerrarInspeccion=None, 
                 botonConfirmacionCierreOrden=None, seleccionOrden=None, campoObservacion=None):
        
        self.gestor = gestor
        self.listaOrdenes = listaOrdenes
        self.listaMotivos = listaMotivos
        self.botonCerrarInspeccion = botonCerrarInspeccion
        self.botonConfirmacionCierreOrden = botonConfirmacionCierreOrden
        self.seleccionOrden = seleccionOrden
        self.campoObservacion = campoObservacion

        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Pantalla de Cierre de Inscripción")
        self.ventana.geometry("1200x600")

        # Botón para cerrar inscripción
        self.botonCerrarInspeccion = ttk.Button(self.ventana, text="Cerrar Inscripción", command=self.opcionCerrarOrdenInspeccion)
        self.botonCerrarInspeccion.pack(pady=10)

        self.ventana.mainloop()


    # Métodos de pantalla
    def opcionCerrarOrdenInspeccion(self):
        self.botonCerrarInspeccion.config(state=tk.DISABLED)
        self.mostrarListaOrdenes()


    def mostrarListaOrdenes(self):
        columnas = ("Nro Orden", "Fecha Finalización", "Estación", "Sismografo")
        self.listaOrdenes = ttk.Treeview(self.ventana, columns=columnas, show='headings')
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
