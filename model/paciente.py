from typing import Optional


class Paciente:
    def __init__(self, nombre_completo: str, telefono: str = "", email: str = "", id_paciente: Optional[int] = None):
        self.id_paciente = id_paciente
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.email = email
    
    def __str__(self):
        return f"{self.nombre_completo} (ID: {self.id_paciente})" if self.id_paciente else self.nombre_completo
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            'id_paciente': self.id_paciente,
            'nombre_completo': self.nombre_completo,
            'telefono': self.telefono,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nombre_completo=data['nombre_completo'],
            telefono=data.get('telefono', ''),
            email=data.get('email', ''),
            id_paciente=data.get('id_paciente')
        )

