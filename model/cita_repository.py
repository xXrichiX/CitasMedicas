from typing import List, Optional
from .cita import Cita
from .observer import Subject
from .database_config import DatabaseConfig

class CitaRepository(Subject):
    def __init__(self, db_config: DatabaseConfig = None):
        super().__init__()
        self.db_config = db_config if db_config else DatabaseConfig()
        self._initialize_database()
    
    def _initialize_database(self):
        try:
            self.db_config.create_database_if_not_exists()
            connection = self.db_config.get_connection()
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES LIKE 'pacientes'")
            if not cursor.fetchone():
                raise Exception("La tabla 'pacientes' no existe.")
            cursor.execute("SHOW TABLES LIKE 'medicos'")
            if not cursor.fetchone():
                raise Exception("La tabla 'medicos' no existe.")
            cursor.execute("SHOW TABLES LIKE 'citas'")
            if not cursor.fetchone():
                raise Exception("La tabla 'citas' no existe.")
            cursor.execute("DESCRIBE citas")
            columnas = cursor.fetchall()
            nombres_columnas = [col[0] for col in columnas]
            if 'id_cita' not in nombres_columnas or 'id_paciente' not in nombres_columnas or 'id_medico' not in nombres_columnas:
                raise Exception("La tabla 'citas' no tiene la estructura correcta.")
            cursor.close()
        except Exception as e:
            print(f"Error verificando base de datos: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_all(self) -> List[Cita]:
        query = """
        SELECT 
            c.id_cita,
            c.id_paciente,
            c.id_medico,
            c.fecha,
            c.hora,
            c.estado,
            p.nombre_completo AS nombre_paciente,
            m.nombre_completo AS nombre_medico
        FROM citas c
        INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
        INNER JOIN medicos m ON c.id_medico = m.id_medico
        ORDER BY c.fecha, c.hora
        """
        results = self.db_config.execute_query(query)
        return [Cita.from_dict(cita) for cita in results]
    
    def get_by_id(self, id_cita: int) -> Optional[Cita]:
        query = """
        SELECT 
            c.id_cita,
            c.id_paciente,
            c.id_medico,
            c.fecha,
            c.hora,
            c.estado,
            p.nombre_completo AS nombre_paciente,
            m.nombre_completo AS nombre_medico
        FROM citas c
        INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
        INNER JOIN medicos m ON c.id_medico = m.id_medico
        WHERE c.id_cita = %s
        """
        results = self.db_config.execute_query(query, (id_cita,))
        if results:
            return Cita.from_dict(results[0])
        return None
    
    def add(self, cita: Cita):
        duplicate_medico_query = """
        SELECT COUNT(*) as count FROM citas 
        WHERE fecha = %s AND hora = %s AND id_medico = %s AND estado != 'Cancelada'
        """
        results = self.db_config.execute_query(
            duplicate_medico_query, 
            (cita.fecha, cita.hora, cita.id_medico)
        )
        if results and results[0]['count'] > 0:
            return "medico_ocupado"
        
        duplicate_paciente_query = """
        SELECT COUNT(*) as count FROM citas 
        WHERE fecha = %s AND hora = %s AND id_paciente = %s AND estado != 'Cancelada'
        """
        results = self.db_config.execute_query(
            duplicate_paciente_query,
            (cita.fecha, cita.hora, cita.id_paciente)
        )
        if results and results[0]['count'] > 0:
            return "paciente_ocupado"
        
        insert_query = """
        INSERT INTO citas (id_paciente, id_medico, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            connection = self.db_config.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                insert_query,
                (cita.id_paciente, cita.id_medico, cita.fecha, cita.hora, cita.estado)
            )
            cita.id_cita = cursor.lastrowid
            connection.commit()
            cursor.close()
            self.notify('cita_agregada', cita)
            return True
        except Exception as e:
            print(f"Error agregando cita: {e}")
            return False
    
    def update(self, id_cita: int, cita_actualizada: Cita):
        if not self.get_by_id(id_cita):
            return False
        
        duplicate_medico_query = """
        SELECT COUNT(*) as count FROM citas 
        WHERE fecha = %s AND hora = %s AND id_medico = %s AND id_cita != %s AND estado != 'Cancelada'
        """
        results = self.db_config.execute_query(
            duplicate_medico_query,
            (cita_actualizada.fecha, cita_actualizada.hora, cita_actualizada.id_medico, id_cita)
        )
        if results and results[0]['count'] > 0:
            return "medico_ocupado"
        
        duplicate_paciente_query = """
        SELECT COUNT(*) as count FROM citas 
        WHERE fecha = %s AND hora = %s AND id_paciente = %s AND id_cita != %s AND estado != 'Cancelada'
        """
        results = self.db_config.execute_query(
            duplicate_paciente_query,
            (cita_actualizada.fecha, cita_actualizada.hora, cita_actualizada.id_paciente, id_cita)
        )
        if results and results[0]['count'] > 0:
            return "paciente_ocupado"
        
        update_query = """
        UPDATE citas 
        SET id_paciente = %s, id_medico = %s, fecha = %s, hora = %s, estado = %s
        WHERE id_cita = %s
        """
        try:
            self.db_config.execute_update(
                update_query,
                (cita_actualizada.id_paciente, cita_actualizada.id_medico,
                 cita_actualizada.fecha, cita_actualizada.hora, cita_actualizada.estado, id_cita)
            )
            self.notify('cita_actualizada', cita_actualizada)
            return True
        except Exception as e:
            print(f"Error actualizando cita: {e}")
            return False
    
    def delete(self, id_cita: int) -> bool:
        cita_eliminada = self.get_by_id(id_cita)
        if not cita_eliminada:
            return False
        
        delete_query = "DELETE FROM citas WHERE id_cita = %s"
        try:
            self.db_config.execute_update(delete_query, (id_cita,))
            self.notify('cita_eliminada', cita_eliminada)
            return True
        except Exception as e:
            print(f"Error eliminando cita: {e}")
            return False
    
    def cancel(self, id_cita: int) -> bool:
        cita = self.get_by_id(id_cita)
        if not cita or cita.estado == 'Cancelada':
            return False
        
        update_query = "UPDATE citas SET estado = 'Cancelada' WHERE id_cita = %s"
        try:
            self.db_config.execute_update(update_query, (id_cita,))
            cita.estado = 'Cancelada'
            self.notify('cita_cancelada', cita)
            return True
        except Exception as e:
            print(f"Error cancelando cita: {e}")
            return False
    
    def close(self):
        self.db_config.close_connection()
