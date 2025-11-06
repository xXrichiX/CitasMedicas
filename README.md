
---

# 🩺 Sistema de Gestión de Citas Médicas – *Salud Integral*

## 📘 Descripción

Aplicación de escritorio en **Python** para gestionar las citas médicas de la clínica *Salud Integral*.
El sistema está desarrollado bajo la arquitectura **MVVM (Model-View-ViewModel)** e implementa el **patrón Observer** para mantener sincronizados los datos con la interfaz en tiempo real.

## 🚀 Funcionalidades principales

* Crear, editar, cancelar y eliminar citas médicas.
* Validar duplicados (mismo médico, fecha y hora).
* Actualización automática de la interfaz (Observer).
* Interfaz sencilla con **Tkinter**.
* Persistencia en **MySQL**.
* Gestión de estados: *Programada*, *Completada* o *Cancelada*.

---

## 🧱 Estructura del proyecto

```
CitasMedicas/
├── model/              # Manejo de los datos
│   ├── __init__.py
│   ├── cita.py
│   ├── cita_repository.py
│   ├── paciente.py
│   ├── paciente_repository.py
│   ├── medico.py
│   ├── medico_repository.py
│   ├── observer.py
│   ├── database_config.py
│   └── config.py
├── view/               # Interfaz visual (Tkinter)
│   ├── __init__.py
│   └── cita_view.py
├── viewmodel/          # Lógica de presentación
│   ├── __init__.py
│   └── cita_viewmodel.py
├── main.py             # Punto de entrada
├── Script.sql          # Script SQL para base de datos
└── README.md
```

---

## 🧩 Arquitectura MVVM + Observer

* **Model:** Maneja los datos y la lógica de negocio (`Cita`, `CitaRepository`).
* **ViewModel:** Conecta la vista con el modelo y aplica validaciones.
* **View:** Interfaz gráfica, actualiza la información automáticamente al recibir notificaciones.

### Flujo de datos

```
Model ↔ ViewModel ↔ View
(Subject) → (Observer/Subject) → (Observer)
```

---

## 🧠 Tecnologías

* Python 
* Tkinter
* MySQL / MariaDB


---

## 👤 Autor

**Ricardo Méndez**
**Pablo Montero**
Proyecto académico – *Clínica Salud Integral*

---

## 📝 Licencia

Uso académico / educativo.
---

