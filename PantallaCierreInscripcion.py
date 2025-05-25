import tkinter as tk
from tkinter import ttk, messagebox
import gestorCierreInscripcion as gestorCierreInscripcion

class PantallaCierreInscripcion:

    def _init_(self, listaOrdenes=None, listaMotivos=None, botonCerrarInspeccion=None, botonConfirmacionCierreOrden=None, seleccionOrden=None, campoObservacion=None):

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

        # Mostrar solo el botón de cerrar inscripción primero
        self.botonCerrarInspeccion = ttk.Button(self.ventana, text="Cerrar Inscripción", command=self.mostrarListaOrdenes)
        self.botonCerrarInspeccion.pack(pady=10)

        # Iniciar loop de ventana
        self.ventana.mainloop()

    def mostrarListaOrdenes(self):
        # Deshabilitar el botón luego de presionarlo
        self.botonCerrarInspeccion.config(state=tk.DISABLED)

        # Crear y mostrar Treeview
        columnas = ("Nro Orden", "ID Sismógrafo", "Estado", "Fecha Inicio", "Fecha Finalización", "Fecha Cierre")
        self.listaOrdenes = ttk.Treeview(self.ventana, columns=columnas, show='headings')
        for col in columnas:
            self.listaOrdenes.heading(col, text=col)
            self.listaOrdenes.column(col, anchor='center', width=100)

        self.listaOrdenes.pack(expand=True, fill='both', padx=10, pady=10)

    def opcionCerrarOrdenInspeccion(self):
        self.botonCerrarInspeccion.config(state=tk.DISABLED)

    def habilitarVentana(self):
        self.botonCerrarInspeccion.config(state=tk.NORMAL)

# Crear instancia para mostrar la ventana
PantallaCierreInscripcion()