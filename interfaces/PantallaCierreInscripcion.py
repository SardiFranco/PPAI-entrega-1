import tkinter as tk
from tkinter import ttk, messagebox
from gestorCierreInscripcion import GestorCierreInscripcion

class PantallaCierreInscripcion:

    #### Elementos de la interfaz
    # Ventana principal
    ventana = tk.Tk()
    ventana.title("Pantalla de Cierre de Inscripción") 
    ventana.geometry("1200x600")

    # Boton de cierre de inspeccion
    botonCerrarInspeccion = ttk.Button(ventana, text="Cerrar Inscripción", command=lambda: messagebox.showinfo("Cierre de Inscripción", "Inscripción cerrada exitosamente."))
    botonCerrarInspeccion.pack(pady=10)

    # Lista

    def __init__(self, listaOrdenes, listaMotivos, botonCerrarInspeccion, botonConfirmacionCierreOrden, seleccionOrden, campoObservacion):
        self.listaOrdenes = listaOrdenes
        self.listaMotivos = listaMotivos
        self.botonCerrarInspeccion = botonCerrarInspeccion
        self.botonConfirmacionCierreOrden = botonConfirmacionCierreOrden
        self.seleccionOrden = seleccionOrden
        self.campoObservacion = campoObservacion

    def opcionCerrarOrdenInspeccion(self):
        self.botonCerrarInspeccion.config(state=tk.DISABLED)


    def habilitarVentana(self):
        # Habilita la ventana de cierre de inscripción
        self.botonCerrarInspeccion.config(state=tk.NORMAL)
 

    columnas = ("Nro Orden", "ID Sismógrafo", "Estado", "Fecha Inicio", "Fecha Finalización", "Fecha Cierre")
    listaOrdenes = ttk.Treeview(ventana, columns=columnas, show='headings')
    for col in columnas:
        listaOrdenes.heading(col, text=col)
        listaOrdenes.column(col, anchor='center', width=100)

    listaOrdenes.pack(expand=True, fill='both', padx=10, pady=10)

    ventana.mainloop()
    opcionCerrarOrdenInspeccion()
    # Esta es una pantalla de cierre de inscripción para una aplicación de gestión de órdenes de inspección.