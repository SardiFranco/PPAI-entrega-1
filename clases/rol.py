class Rol:
    def __init__(self, descripcionRol: str, nombre: str):
        self.descripcionRol = descripcionRol
        self.nombre = nombre

    def getNombre(self):
        return self.nombre