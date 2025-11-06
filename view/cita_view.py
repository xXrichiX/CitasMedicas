import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime, date
from model.cita import Cita
from model.observer import Observer
from viewmodel.cita_viewmodel import CitaViewModel


class CitaView(Observer):
    def __init__(self, root: tk.Tk, viewmodel: CitaViewModel):
        self.root = root
        self.viewmodel = viewmodel
        self.viewmodel.attach_view(self)
        self.cita_seleccionada: Optional[Cita] = None
        self._cita_map: dict[int, Cita] = {}
        self._medicos_dict: dict[str, int] = {}
        self._setup_ui()
        self._cargar_citas()
    
    def _setup_ui(self):
        self.root.title("Sistema de Gestión de Citas Médicas - Salud Integral")
        self.root.geometry("1000x700")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.map('Treeview', background=[('selected', '#4A90E2')])
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        form_frame = ttk.LabelFrame(main_frame, text="Formulario de Cita", padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Paciente:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.paciente_entry = ttk.Entry(form_frame, width=25)
        self.paciente_entry.grid(row=0, column=1, pady=5, padx=5, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Médico:").grid(row=0, column=3, sticky=tk.W, pady=5, padx=(20, 5))
        self.medico_combo = ttk.Combobox(form_frame, width=25, state='readonly')
        self.medico_combo.grid(row=0, column=4, pady=5, padx=5, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Fecha:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.fecha_entry = ttk.Entry(form_frame, width=15)
        self.fecha_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Label(form_frame, text="(YYYY-MM-DD)", font=('Arial', 8), foreground='gray').grid(row=1, column=2, sticky=tk.W, padx=2)
        
        ttk.Label(form_frame, text="Hora:").grid(row=1, column=3, sticky=tk.W, pady=5, padx=(20, 5))
        self.hora_entry = ttk.Entry(form_frame, width=10)
        self.hora_entry.grid(row=1, column=4, pady=5, padx=5, sticky=tk.W)
        ttk.Label(form_frame, text="(HH:MM)", font=('Arial', 8), foreground='gray').grid(row=1, column=5, sticky=tk.W, padx=2)
        
        self.id_label = ttk.Label(form_frame, text="ID Cita:")
        self.id_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.id_entry = ttk.Entry(form_frame, width=15, state='readonly')
        self.id_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.id_entry.config(foreground='gray')
        self.id_label.grid_remove()
        self.id_entry.grid_remove()
        
        self.estado_label = ttk.Label(form_frame, text="Estado:")
        self.estado_label.grid(row=2, column=3, sticky=tk.W, pady=5, padx=(20, 5))
        self.estado_combo = ttk.Combobox(form_frame, values=Cita.ESTADOS, width=17, state='readonly')
        self.estado_combo.set('Programada')
        self.estado_combo.grid(row=2, column=4, pady=5, padx=5, sticky=tk.W)
        self.estado_label.grid_remove()
        self.estado_combo.grid_remove()
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=6, pady=15)
        
        self.btn_guardar = ttk.Button(button_frame, text="Guardar Nueva Cita", command=self._guardar_cita)
        self.btn_guardar.pack(side=tk.LEFT, padx=5)
        
        self.btn_cancelar_form = ttk.Button(button_frame, text="Limpiar", command=self._limpiar_formulario)
        self.btn_cancelar_form.pack(side=tk.LEFT, padx=5)
        
        self.mensaje_label = ttk.Label(form_frame, text="", font=('Arial', 9))
        self.mensaje_label.grid(row=4, column=0, columnspan=6, pady=(5, 0))
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(4, weight=1)
        
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Citas", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ('Fecha', 'Hora', 'Paciente', 'Médico', 'Estado', 'ID')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Hora', text='Hora')
        self.tree.heading('Paciente', text='Paciente')
        self.tree.heading('Médico', text='Médico')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('ID', text='ID')
        self.tree.column('Fecha', width=100)
        self.tree.column('Hora', width=80)
        self.tree.column('Paciente', width=200)
        self.tree.column('Médico', width=200)
        self.tree.column('Estado', width=100)
        self.tree.column('ID', width=50)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X)
        
        self.btn_editar = ttk.Button(action_frame, text="Editar", command=self._editar_cita_seleccionada, state='disabled')
        self.btn_editar.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(action_frame, text="Eliminar", command=self._eliminar_cita_seleccionada, state='disabled')
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_cancelar_estado = ttk.Button(action_frame, text="Cancelar", command=self._marcar_cancelada, state='disabled')
        self.btn_cancelar_estado.pack(side=tk.LEFT, padx=5)
        
        self.btn_completar = ttk.Button(action_frame, text="Marcar Completada", command=self._marcar_completada, state='disabled')
        self.btn_completar.pack(side=tk.LEFT, padx=5)
        
        self._cargar_comboboxes()
    
    def _cargar_comboboxes(self):
        medicos = self.viewmodel.get_all_medicos()
        nombres_medicos = [m.nombre_completo for m in medicos]
        self.medico_combo['values'] = nombres_medicos
        self._medicos_dict = {m.nombre_completo: m.id_medico for m in medicos}
    
    def _limpiar_formulario(self):
        self.id_label.grid_remove()
        self.id_entry.grid_remove()
        self.estado_label.grid_remove()
        self.estado_combo.grid_remove()
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.paciente_entry.delete(0, tk.END)
        self.medico_combo.set('')
        self.fecha_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)
        self.estado_combo.set('Programada')
        self.cita_seleccionada = None
        self.btn_guardar.config(state='normal', text="Guardar Nueva Cita", command=self._guardar_cita)
        self.btn_cancelar_form.config(state='normal')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')
        self.btn_cancelar_estado.config(state='disabled')
        self.btn_completar.config(state='disabled')
        self._mostrar_mensaje("", "")
    
    def _validar_fecha_hora(self, fecha: str, hora: str) -> bool:
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            self._mostrar_mensaje("Formato de fecha inválido. Use YYYY-MM-DD (ejemplo: 2024-12-25)", "error")
            return False
        
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            self._mostrar_mensaje("Formato de hora inválido. Use HH:MM (ejemplo: 14:30)", "error")
            return False
        
        return True
    
    def _obtener_o_crear_paciente(self, nombre: str) -> Optional[int]:
        if not self.viewmodel.paciente_repo:
            return None
        from model.paciente import Paciente
        pacientes = self.viewmodel.paciente_repo.get_all()
        for p in pacientes:
            if p.nombre_completo.lower() == nombre.lower():
                return p.id_paciente
        nueva_paciente = Paciente(nombre)
        if self.viewmodel.paciente_repo.add(nueva_paciente):
            return nueva_paciente.id_paciente
        return None
    
    def _guardar_cita(self):
        self.btn_guardar.config(state='disabled')
        self.root.after(500, lambda: self.btn_guardar.config(state='normal'))
        
        nombre_paciente = self.paciente_entry.get().strip()
        nombre_medico = self.medico_combo.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        estado = 'Programada'
        
        if not nombre_paciente:
            self._mostrar_mensaje("El nombre del paciente es obligatorio", "error")
            return
        
        if not nombre_medico:
            self._mostrar_mensaje("Debe seleccionar un médico", "error")
            return
        
        id_medico = self._medicos_dict.get(nombre_medico)
        if not id_medico:
            self._mostrar_mensaje("Médico no válido. Por favor seleccione uno de la lista", "error")
            return
        
        id_paciente = self._obtener_o_crear_paciente(nombre_paciente)
        if not id_paciente:
            self._mostrar_mensaje("No se pudo crear el paciente", "error")
            return
        
        if not self._validar_fecha_hora(fecha, hora):
            return
        
        exito, mensaje = self.viewmodel.agregar_cita(id_paciente, id_medico, fecha, hora, estado)
        
        if exito:
            self._mostrar_mensaje(f"✓ {mensaje}", "info")
            self.root.after(1500, self._limpiar_formulario)
        else:
            self._mostrar_mensaje(f"✗ {mensaje}", "error")
    
    def _actualizar_cita(self):
        if not self.cita_seleccionada:
            self._mostrar_mensaje("Por favor seleccione una cita", "warning")
            return
        
        self.btn_guardar.config(state='disabled')
        self.root.after(500, lambda: self.btn_guardar.config(state='normal'))
        
        nombre_paciente = self.paciente_entry.get().strip()
        nombre_medico = self.medico_combo.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()
        estado = self.estado_combo.get()
        
        if not nombre_paciente:
            self._mostrar_mensaje("El nombre del paciente es obligatorio", "error")
            return
        
        if not nombre_medico:
            self._mostrar_mensaje("Debe seleccionar un médico", "error")
            return
        
        id_medico = self._medicos_dict.get(nombre_medico)
        if not id_medico:
            self._mostrar_mensaje("Médico no válido. Por favor seleccione uno de la lista", "error")
            return
        
        id_paciente = self._obtener_o_crear_paciente(nombre_paciente)
        if not id_paciente:
            self._mostrar_mensaje("No se pudo crear el paciente", "error")
            return
        
        if not self._validar_fecha_hora(fecha, hora):
            return
        
        exito, mensaje = self.viewmodel.actualizar_cita(
            self.cita_seleccionada.id_cita,
            id_paciente, id_medico, fecha, hora, estado
        )
        
        if exito:
            self._mostrar_mensaje(f"✓ {mensaje}", "info")
            self.root.after(1500, self._limpiar_formulario)
        else:
            self._mostrar_mensaje(f"✗ {mensaje}", "error")
    
    def _editar_cita_seleccionada(self):
        if not self.cita_seleccionada:
            self._mostrar_mensaje("Por favor seleccione una cita", "warning")
            return
        
        self._cargar_cita_en_formulario(self.cita_seleccionada)
        self.btn_guardar.config(state='normal', text="Actualizar", command=self._actualizar_cita)
        self.btn_cancelar_form.config(text="Cancelar", command=self._limpiar_formulario)
    
    def _eliminar_cita_seleccionada(self):
        if not self.cita_seleccionada:
            self._mostrar_mensaje("Por favor seleccione una cita de la lista", "warning")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de ELIMINAR permanentemente la cita {self.cita_seleccionada.id_cita}?\n\nEsta acción no se puede deshacer."
        )
        
        if confirmar:
            exito, mensaje = self.viewmodel.eliminar_cita(self.cita_seleccionada.id_cita)
            if exito:
                self._mostrar_mensaje(f"✓ {mensaje}", "info")
                self._limpiar_formulario()
            else:
                self._mostrar_mensaje(f"✗ {mensaje}", "error")
    
    def _marcar_cancelada(self):
        if not self.cita_seleccionada:
            self._mostrar_mensaje("Por favor seleccione una cita", "warning")
            return
        
        if self.cita_seleccionada.estado == 'Cancelada':
            self._mostrar_mensaje("La cita ya está cancelada", "warning")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Desea marcar la cita {self.cita_seleccionada.id_cita} como Cancelada?"
        )
        if confirmar:
            exito, mensaje = self.viewmodel.actualizar_cita(
                self.cita_seleccionada.id_cita,
                self.cita_seleccionada.id_paciente,
                self.cita_seleccionada.id_medico,
                self.cita_seleccionada.fecha,
                self.cita_seleccionada.hora,
                'Cancelada'
            )
            if exito:
                self._mostrar_mensaje(f"✓ {mensaje}", "info")
                self._limpiar_formulario()
            else:
                self._mostrar_mensaje(f"✗ {mensaje}", "error")
    
    def _marcar_completada(self):
        if not self.cita_seleccionada:
            self._mostrar_mensaje("Por favor seleccione una cita", "warning")
            return
        
        if self.cita_seleccionada.estado == 'Completada':
            self._mostrar_mensaje("La cita ya está completada", "warning")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Desea marcar la cita {self.cita_seleccionada.id_cita} como Completada?"
        )
        if confirmar:
            exito, mensaje = self.viewmodel.actualizar_cita(
                self.cita_seleccionada.id_cita,
                self.cita_seleccionada.id_paciente,
                self.cita_seleccionada.id_medico,
                self.cita_seleccionada.fecha,
                self.cita_seleccionada.hora,
                'Completada'
            )
            if exito:
                self._mostrar_mensaje(f"✓ {mensaje}", "info")
                self._limpiar_formulario()
            else:
                self._mostrar_mensaje(f"✗ {mensaje}", "error")
    
    def _on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            id_cita = item['values'][5]
            cita = self._cita_map.get(id_cita)
            if not cita:
                cita = self.viewmodel.get_cita_by_id(id_cita)
                if cita:
                    self._cita_map[id_cita] = cita
            if cita:
                self.cita_seleccionada = cita
                self.btn_editar.config(state='normal')
                self.btn_eliminar.config(state='normal')
                self.btn_cancelar_estado.config(state='normal')
                self.btn_completar.config(state='normal')
        else:
            self.cita_seleccionada = None
            self.btn_editar.config(state='disabled')
            self.btn_eliminar.config(state='disabled')
            self.btn_cancelar_estado.config(state='disabled')
            self.btn_completar.config(state='disabled')
    
    def _cargar_cita_en_formulario(self, cita: Cita):
        self.id_label.grid()
        self.id_entry.grid()
        self.estado_label.grid()
        self.estado_combo.grid()
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, str(cita.id_cita))
        self.id_entry.config(state='readonly', foreground='gray')
        self._cargar_comboboxes()
        nombre_paciente = cita.nombre_paciente or ''
        self.paciente_entry.delete(0, tk.END)
        self.paciente_entry.insert(0, nombre_paciente)
        nombre_medico = cita.nombre_medico
        if nombre_medico and nombre_medico in self._medicos_dict:
            self.medico_combo.set(nombre_medico)
        else:
            self.medico_combo.set('')
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, cita.fecha)
        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, cita.hora)
        self.estado_combo.set(cita.estado)
    
    def _cargar_citas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._cita_map.clear()
        citas = self.viewmodel.get_all_citas()
        citas.sort(key=lambda c: (c.fecha, c.hora))
        for cita in citas:
            self._cita_map[cita.id_cita] = cita
            nombre_paciente = cita.nombre_paciente or f"Paciente {cita.id_paciente}"
            nombre_medico = cita.nombre_medico or f"Médico {cita.id_medico}"
            self.tree.insert('', tk.END, values=(
                cita.fecha,
                cita.hora,
                nombre_paciente,
                nombre_medico,
                cita.estado,
                cita.id_cita
            ), tags=(cita.estado,))
        self.tree.tag_configure('Cancelada', foreground='red')
        self.tree.tag_configure('Completada', foreground='green')
    
    def _mostrar_mensaje(self, mensaje: str, tipo: str = "info"):
        self.mensaje_label.config(text=mensaje)
        if tipo == "error":
            self.mensaje_label.config(foreground='red')
        elif tipo == "warning":
            self.mensaje_label.config(foreground='orange')
        elif tipo == "info":
            self.mensaje_label.config(foreground='green')
        else:
            self.mensaje_label.config(foreground='black')
    
    def update(self, message: str, data=None):
        self._cargar_citas()
        self._cargar_comboboxes()
        print(f"Vista notificada: {message}")

