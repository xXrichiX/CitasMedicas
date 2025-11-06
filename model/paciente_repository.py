from typing import List, Optional
from .paciente import Paciente
from .database_config import DatabaseConfig


class PacienteRepository:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    def get_all(self) -> List[Paciente]:
        query = "SELECT * FROM pacientes ORDER BY nombre_completo"
        results = self.db_config.execute_query(query)
        return [Paciente.from_dict(p) for p in results]
    
    def get_by_id(self, id_paciente: int) -> Optional[Paciente]:
        query = "SELECT * FROM pacientes WHERE id_paciente = %s"
        results = self.db_config.execute_query(query, (id_paciente,))
        if results:
            return Paciente.from_dict(results[0])
        return None
    
    def add(self, paciente: Paciente) -> bool:
        query = """
        INSERT INTO pacientes (nombre_completo, telefono, email)
        VALUES (%s, %s, %s)
        """
        try:
            connection = self.db_config.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (paciente.nombre_completo, paciente.telefono, paciente.email))
            paciente.id_paciente = cursor.lastrowid
            connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error agregando paciente: {e}")
            return False
    
    def update(self, id_paciente: int, paciente: Paciente) -> bool:
        query = """
        UPDATE pacientes 
        SET nombre_completo = %s, telefono = %s, email = %s
        WHERE id_paciente = %s
        """
        try:
            self.db_config.execute_update(
                query,
                (paciente.nombre_completo, paciente.telefono, 
                 paciente.email, id_paciente)
            )
            return True
        except Exception as e:
            print(f"Error actualizando paciente: {e}")
            return False
    
    def delete(self, id_paciente: int) -> bool:
        check_query = "SELECT COUNT(*) as count FROM citas WHERE id_paciente = %s"
        results = self.db_config.execute_query(check_query, (id_paciente,))
        if results and results[0]['count'] > 0:
            return False
        
        query = "DELETE FROM pacientes WHERE id_paciente = %s"
        try:
            self.db_config.execute_update(query, (id_paciente,))
            return True
        except Exception as e:
            print(f"Error eliminando paciente: {e}")
            return False

