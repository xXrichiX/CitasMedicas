from typing import Optional


class Medico:
    def __init__(self, nombre_completo: str, especialidad: str = "", telefono: str = "", id_medico: Optional[int] = None):
        self.id_medico = id_medico
        self.nombre_completo = nombre_completo
        self.especialidad = especialidad
        self.telefono = telefono
    
    def __str__(self):
        return f"Dr./Dra. {self.nombre_completo} - {self.especialidad}" if self.especialidad else f"Dr./Dra. {self.nombre_completo}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            'id_medico': self.id_medico,
            'nombre_completo': self.nombre_completo,
            'especialidad': self.especialidad,
            'telefono': self.telefono
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nombre_completo=data['nombre_completo'],
            especialidad=data.get('especialidad', ''),
            telefono=data.get('telefono', ''),
            id_medico=data.get('id_medico')
        )

