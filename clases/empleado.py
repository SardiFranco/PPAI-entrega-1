import clases.rol as Rol
class Empleado:
    listadoEmpleados = []
    def __init__(self, nombre: str, apellido: str, telefono: int, mail: str, rol : Rol):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.mail = mail
        self.rol = rol
        Empleado.listadoEmpleados.append(self)
    
    def obtenerMail(self):
        return self.mail
    
    def esResponsableReparacion(self):
        return self.rol.getNombre() == "ResponsableReparación"
    