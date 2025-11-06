from typing import List, Optional
from datetime import datetime
from model.cita import Cita
from model.cita_repository import CitaRepository
from model.paciente_repository import PacienteRepository
from model.medico_repository import MedicoRepository
from model.observer import Observer


class CitaViewModel(Observer):
    def __init__(self, repository: CitaRepository, 
                 paciente_repo: PacienteRepository = None,
                 medico_repo: MedicoRepository = None):
        self.repository = repository
        self.paciente_repo = paciente_repo
        self.medico_repo = medico_repo
        self.repository.attach(self)
        self._view_observers: List[Observer] = []
    
    def attach_view(self, observer: Observer):
        if observer not in self._view_observers:
            self._view_observers.append(observer)
    
    def detach_view(self, observer: Observer):
        if observer in self._view_observers:
            self._view_observers.remove(observer)
    
    def _notify_views(self, message: str, data=None):
        for observer in self._view_observers:
            observer.update(message, data)
    
    def update(self, message: str, data=None):
        self._notify_views(message, data)
    
    def get_all_citas(self) -> List[Cita]:
        return self.repository.get_all()
    
    def get_cita_by_id(self, id_cita: int) -> Optional[Cita]:
        return self.repository.get_by_id(id_cita)
    
    def get_all_pacientes(self):
        if self.paciente_repo:
            return self.paciente_repo.get_all()
        return []
    
    def get_all_medicos(self):
        if self.medico_repo:
            return self.medico_repo.get_all()
        return []
    
    def agregar_cita(self, id_paciente: int, id_medico: int, fecha: str, 
                     hora: str, estado: str = 'Programada') -> tuple[bool, str]:
        if not id_paciente:
            return False, "Debe seleccionar un paciente"
        
        if not id_medico:
            return False, "Debe seleccionar un médico"
        
        if self.paciente_repo:
            paciente = self.paciente_repo.get_by_id(id_paciente)
            if not paciente:
                return False, "El paciente seleccionado no existe"
        
        if self.medico_repo:
            medico = self.medico_repo.get_by_id(id_medico)
            if not medico:
                return False, "El médico seleccionado no existe"
        
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"
        
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            return False, "Formato de hora inválido. Use HH:MM"
        
        nueva_cita = Cita(id_paciente, id_medico, fecha, hora, estado)
        
        resultado = self.repository.add(nueva_cita)
        if resultado is True:
            id_cita = nueva_cita.id_cita or "nueva"
            return True, f"Cita #{id_cita} agregada exitosamente"
        elif resultado == "medico_ocupado":
            return False, "El médico ya tiene una cita programada a esa fecha y hora"
        elif resultado == "paciente_ocupado":
            return False, "El paciente ya tiene una cita programada a esa fecha y hora"
        else:
            return False, "No se pudo agregar la cita. Verifique que no haya duplicados"
    
    def actualizar_cita(self, id_cita: int, id_paciente: int, id_medico: int,
                        fecha: str, hora: str, estado: str) -> tuple[bool, str]:
        cita_existente = self.repository.get_by_id(id_cita)
        if not cita_existente:
            return False, "La cita no existe"
        
        if not id_paciente:
            return False, "Debe seleccionar un paciente"
        
        if not id_medico:
            return False, "Debe seleccionar un médico"
        
        if self.paciente_repo:
            paciente = self.paciente_repo.get_by_id(id_paciente)
            if not paciente:
                return False, "El paciente seleccionado no existe"
        
        if self.medico_repo:
            medico = self.medico_repo.get_by_id(id_medico)
            if not medico:
                return False, "El médico seleccionado no existe"
        
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"
        
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            return False, "Formato de hora inválido. Use HH:MM"
        
        cita_actualizada = Cita(id_paciente, id_medico, fecha, hora, estado, id_cita=id_cita)
        
        resultado = self.repository.update(id_cita, cita_actualizada)
        if resultado is True:
            return True, f"Cita #{id_cita} actualizada exitosamente"
        elif resultado == "medico_ocupado":
            return False, "El médico ya tiene otra cita programada a esa fecha y hora"
        elif resultado == "paciente_ocupado":
            return False, "El paciente ya tiene otra cita programada a esa fecha y hora"
        else:
            return False, "No se pudo actualizar la cita. Verifique que no haya duplicados"
    
    def eliminar_cita(self, id_cita: int) -> tuple[bool, str]:
        if self.repository.delete(id_cita):
            return True, f"Cita #{id_cita} eliminada exitosamente"
        else:
            return False, "La cita no existe"
    
    def cancelar_cita(self, id_cita: int) -> tuple[bool, str]:
        if self.repository.cancel(id_cita):
            return True, f"Cita #{id_cita} cancelada exitosamente"
        else:
            return False, "La cita no existe o ya está cancelada"

