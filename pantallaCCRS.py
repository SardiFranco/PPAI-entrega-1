class PantallaCCRS:
    def publicar(self, idSismografo, estado_FueraServicio, fechaHoraRegistroEstado, comentariosfueraServicio):
        print(f"Publicando estado del sismógrafo {idSismografo}:")
        print(f"Estado: {estado_FueraServicio.getNombreEstado()}")
        print(f"Fecha y Hora de Registro: {fechaHoraRegistroEstado}")
        print(f"Comentarios por motivos: {comentariosfueraServicio}")
