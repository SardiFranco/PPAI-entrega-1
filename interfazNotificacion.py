class InterfazNotificacion:
    def __init__(self):
        """
        Constructor de la clase InterfazNotificacion.
        Esta clase define una interfaz para enviar notificaciones.
        """
        pass

    def enviarMail(self, lista_mail):
        for mail in lista_mail:
            print(f"Enviando correo a: {mail}")
            