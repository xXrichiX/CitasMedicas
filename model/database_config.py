import mysql.connector
from mysql.connector import Error
from typing import Optional


class DatabaseConfig:
    def __init__(self, 
                 host: str = 'localhost',
                 database: str = 'citas_medicas',
                 user: str = 'root',
                 password: str = '',
                 port: int = 3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self._connection: Optional[mysql.connector.MySQLConnection] = None
    
    def get_connection(self) -> mysql.connector.MySQLConnection:
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                if self._connection.is_connected():
                    print(f"✓ Conectado a MySQL: {self.database}")
            except Error as e:
                print(f"✗ Error conectando a MySQL: {e}")
                raise
        return self._connection
    
    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Conexión a MySQL cerrada")
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error ejecutando consulta: {e}")
            raise
        finally:
            cursor.close()
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return True
        except Error as e:
            connection.rollback()
            print(f"Error ejecutando actualización: {e}")
            raise
        finally:
            cursor.close()
    
    def create_database_if_not_exists(self):
        try:
            temp_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = temp_connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            temp_connection.close()
            print(f"✓ Base de datos '{self.database}' verificada/creada")
        except Error as e:
            print(f"Error creando base de datos: {e}")
            raise

