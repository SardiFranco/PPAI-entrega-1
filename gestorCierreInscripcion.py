import PantallaCierreInscripcion as PantallaCierreInscripcion

class GestorCierreInscripcion:
    def __init__(self, ordenes, motivos, comentario, fechaHoraActual, mail):
        self.ordenes = ordenes
        self.motivos = motivos
        self.comentario = comentario
        self.fechaHoraActual = fechaHoraActual
        self.mail = mail
    
    