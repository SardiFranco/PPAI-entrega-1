class Empleado:
    def __init__(self, nombre: str, apellido: str, telefono: int, mail: str):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.mail = mail
    
    def obtenerMail(self):
        return self.mail
    