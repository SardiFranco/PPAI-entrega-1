class Empleado:
    ROLES = ["ResponsableInspección", "ResponsableReparación"]

    def __init__(self, nombre: str, apellido: str, telefono: int, mail: str, rol : str):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.mail = mail
        self.rol = rol
    
    def obtenerMail(self):
        return self.mail
    
    def esResponsableReparacion(self):
        return self.rol == "ResponsableReparación"
    