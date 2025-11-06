from typing import List, Optional
from .medico import Medico
from .database_config import DatabaseConfig


class MedicoRepository:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def get_all(self) -> List[Medico]:
        query = "SELECT * FROM medicos ORDER BY nombre_completo"
        results = self.db_config.execute_query(query)
        return [Medico.from_dict(m) for m in results]
    
    def get_by_id(self, id_medico: int) -> Optional[Medico]:
        query = "SELECT * FROM medicos WHERE id_medico = %s"
        results = self.db_config.execute_query(query, (id_medico,))
        if results:
            return Medico.from_dict(results[0])
        return None
    
    def add(self, medico: Medico) -> bool:
        query = """
        INSERT INTO medicos (nombre_completo, especialidad, telefono)
        VALUES (%s, %s, %s)
        """
        try:
            connection = self.db_config.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (medico.nombre_completo, medico.especialidad, medico.telefono))
            medico.id_medico = cursor.lastrowid
            connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error agregando médico: {e}")
            return False
    
    def update(self, id_medico: int, medico: Medico) -> bool:
        query = """
        UPDATE medicos 
        SET nombre_completo = %s, especialidad = %s, telefono = %s
        WHERE id_medico = %s
        """
        try:
            self.db_config.execute_update(
                query,
                (medico.nombre_completo, medico.especialidad, 
                 medico.telefono, id_medico)
            )
            return True
        except Exception as e:
            print(f"Error actualizando médico: {e}")
            return False
    
    def delete(self, id_medico: int) -> bool:
        check_query = "SELECT COUNT(*) as count FROM citas WHERE id_medico = %s"
        results = self.db_config.execute_query(check_query, (id_medico,))
        if results and results[0]['count'] > 0:
            return False
        
        query = "DELETE FROM medicos WHERE id_medico = %s"
        try:
            self.db_config.execute_update(query, (id_medico,))
            return True
        except Exception as e:
            print(f"Error eliminando médico: {e}")
            return False
    
    def get_citas_by_medico(self, id_medico: int):
        query = """
        SELECT c.*, p.nombre_completo as nombre_paciente, m.nombre_completo as nombre_medico
        FROM citas c
        JOIN pacientes p ON c.id_paciente = p.id_paciente
        JOIN medicos m ON c.id_medico = m.id_medico
        WHERE c.id_medico = %s
        ORDER BY c.fecha, c.hora
        """
        return self.db_config.execute_query(query, (id_medico,))

