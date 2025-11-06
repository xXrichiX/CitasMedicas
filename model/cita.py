from datetime import datetime
from typing import Optional


class Cita:
    ESTADOS = ['Programada', 'Completada', 'Cancelada']
    
    def __init__(self, id_paciente: int, id_medico: int,
                 fecha: str, hora: str, estado: str = 'Programada',
                 id_cita: Optional[int] = None,
                 nombre_paciente: str = None, nombre_medico: str = None):
        self.id_cita = id_cita
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha = fecha
        self.hora = hora
        self.estado = estado if estado in self.ESTADOS else 'Programada'
        self.nombre_paciente = nombre_paciente
        self.nombre_medico = nombre_medico
    
    def __str__(self):
        paciente = self.nombre_paciente or f"Paciente {self.id_paciente}"
        medico = self.nombre_medico or f"Médico {self.id_medico}"
        cita_id = self.id_cita or "Nueva"
        return f"Cita {cita_id}: {paciente} - {medico} - {self.fecha} {self.hora}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            'id_cita': self.id_cita,
            'id_paciente': self.id_paciente,
            'id_medico': self.id_medico,
            'fecha': self.fecha,
            'hora': self.hora,
            'estado': self.estado,
            'nombre_paciente': self.nombre_paciente,
            'nombre_medico': self.nombre_medico
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        fecha = data['fecha']
        if hasattr(fecha, 'strftime'):
            fecha = fecha.strftime('%Y-%m-%d')
        elif not isinstance(fecha, str):
            fecha = str(fecha)
        
        hora = data['hora']
        if hasattr(hora, 'strftime'):
            hora = hora.strftime('%H:%M')
        elif not isinstance(hora, str):
            hora = str(hora)
            if ':' in hora and hora.count(':') == 2:
                hora = ':'.join(hora.split(':')[:2])
        
        return cls(
            id_paciente=data.get('id_paciente'),
            id_medico=data.get('id_medico'),
            fecha=fecha,
            hora=hora,
            estado=data.get('estado', 'Programada'),
            id_cita=data.get('id_cita'),
            nombre_paciente=data.get('nombre_paciente'),
            nombre_medico=data.get('nombre_medico')
        )
    
    def get_datetime(self):
        try:
            return datetime.strptime(f"{self.fecha} {self.hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    
    def is_duplicate_of(self, other: 'Cita') -> bool:
        return (self.fecha == other.fecha and 
                self.hora == other.hora and 
                self.id_medico == other.id_medico and
                self.id_cita != other.id_cita)

