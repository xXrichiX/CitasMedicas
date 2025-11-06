import os
import sys

if sys.platform == 'darwin':
    os.environ['PYTHON_CONNECT_TO_APP'] = '1'

import tkinter as tk

root = tk.Tk()
root.withdraw()

from model.cita_repository import CitaRepository
from model.paciente_repository import PacienteRepository
from model.medico_repository import MedicoRepository
from model.database_config import DatabaseConfig
from model.config import DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD, DB_PORT
from viewmodel.cita_viewmodel import CitaViewModel
from view.cita_view import CitaView


def main():
    try:
        db_config = DatabaseConfig(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        repository = CitaRepository(db_config)
        paciente_repo = PacienteRepository(db_config)
        medico_repo = MedicoRepository(db_config)
        
        viewmodel = CitaViewModel(repository, paciente_repo, medico_repo)
        
        view = CitaView(root, viewmodel)
        
        def on_closing():
            repository.close()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        root.deiconify()
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error iniciando la aplicación: {e}")
        print("\nPor favor verifique:")
        print("1. MySQL está instalado y ejecutándose")
        print("2. La configuración en model/config.py es correcta")
        print("3. Las credenciales de MySQL son válidas")
        if root.winfo_exists():
            root.destroy()


if __name__ == "__main__":
    main()
