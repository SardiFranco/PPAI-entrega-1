import clases.empleado as Empleado

class Usuario:
    def __init__(self, nombreusuario: str, contrasena: str, empleado: Empleado):
        self.nombreusuario = nombreusuario
        self.contrasena = contrasena
        self.empleado = empleado

    def getRLlogueado(self):
        return self.empleado 