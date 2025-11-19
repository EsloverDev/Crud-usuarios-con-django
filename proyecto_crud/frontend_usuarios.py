import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QPushButton, 
                             QVBoxLayout, QWidget, QMessageBox, QHeaderView,
                             QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
import json

class UsuarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_url = "http://localhost:8000/api/usuarios/"
        self.usuario_editando = None  # Para controlar si estamos editando
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("CRUD Usuarios - Django + PyQt")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Sistema de Gestión de Usuarios")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(titulo)
        
        # Formulario
        form_layout = QHBoxLayout()
        
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Código (número único)")
        self.codigo_input.setMaximumWidth(150)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        self.nombre_input.setMinimumWidth(200)
        
        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setStyleSheet("background-color: #28a745; color: white;")
        
        self.btn_editar = QPushButton("Guardar Edición")
        self.btn_editar.setStyleSheet("background-color: #ffc107; color: black;")
        self.btn_editar.setVisible(False)  # Oculto inicialmente
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setStyleSheet("background-color: #6c757d; color: white;")
        self.btn_cancelar.setVisible(False)  # Oculto inicialmente
        
        form_layout.addWidget(QLabel("Código:"))
        form_layout.addWidget(self.codigo_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.btn_agregar)
        form_layout.addWidget(self.btn_editar)
        form_layout.addWidget(self.btn_cancelar)
        form_layout.addStretch()
        
        layout.addLayout(form_layout)
        
        # Tabla de usuarios
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(3)
        self.tabla_usuarios.setHorizontalHeaderLabels(["Código", "Nombre", "Acciones"])
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.tabla_usuarios)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        
        self.btn_actualizar = QPushButton("Actualizar Lista")
        self.btn_actualizar.setStyleSheet("background-color: #17a2b8; color: white;")
        
        self.btn_limpiar = QPushButton("Limpiar Formulario")
        self.btn_limpiar.setStyleSheet("background-color: #6c757d; color: white;")
        
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_limpiar)
        botones_layout.addStretch()
        
        layout.addLayout(botones_layout)
        
        # Conectar señales
        self.btn_agregar.clicked.connect(self.agregar_usuario)
        self.btn_editar.clicked.connect(self.guardar_edicion)
        self.btn_cancelar.clicked.connect(self.cancelar_edicion)
        self.btn_actualizar.clicked.connect(self.cargar_usuarios)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        
        central_widget.setLayout(layout)
        
        # Cargar usuarios al iniciar
        self.cargar_usuarios()
    
    def cargar_usuarios(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                usuarios = response.json()
                self.mostrar_usuarios(usuarios)
            else:
                QMessageBox.warning(self, "Error", f"Error al cargar usuarios: {response.status_code}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Error de Conexión", 
                               "No se puede conectar al servidor Django.\n"
                               "Asegúrate de que el servidor esté corriendo en:\n"
                               "http://localhost:8000")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
    
    def mostrar_usuarios(self, usuarios):
        self.tabla_usuarios.setRowCount(len(usuarios))
        
        for row, usuario in enumerate(usuarios):
            # Columna Código
            self.tabla_usuarios.setItem(row, 0, QTableWidgetItem(str(usuario['codigo'])))
            
            # Columna Nombre
            self.tabla_usuarios.setItem(row, 1, QTableWidgetItem(usuario['nombre']))
            
            # Columna Acciones
            widget_acciones = QWidget()
            layout_acciones = QHBoxLayout()
            layout_acciones.setContentsMargins(2, 2, 2, 2)
            
            btn_editar = QPushButton("Editar")
            btn_editar.setStyleSheet("background-color: #ffc107; color: black; font-size: 10px;")
            btn_editar.clicked.connect(lambda checked, r=row: self.preparar_edicion(r))
            
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setStyleSheet("background-color: #dc3545; color: white; font-size: 10px;")
            btn_eliminar.clicked.connect(lambda checked, r=row: self.eliminar_usuario(r))
            
            layout_acciones.addWidget(btn_editar)
            layout_acciones.addWidget(btn_eliminar)
            widget_acciones.setLayout(layout_acciones)
            
            self.tabla_usuarios.setCellWidget(row, 2, widget_acciones)
    
    def agregar_usuario(self):
        codigo = self.codigo_input.text().strip()
        nombre = self.nombre_input.text().strip()
        
        if not codigo or not nombre:
            QMessageBox.warning(self, "Datos incompletos", "Por favor ingresa código y nombre")
            return
        
        try:
            codigo_int = int(codigo)
        except ValueError:
            QMessageBox.warning(self, "Código inválido", "El código debe ser un número")
            return
        
        try:
            data = {"codigo": codigo_int, "nombre": nombre}
            response = requests.post(self.api_url, json=data)
            
            if response.status_code == 201:
                self.cargar_usuarios()
                self.limpiar_formulario()
                QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
            else:
                error_data = response.json()
                mensaje_error = error_data.get('detalles', {}).get('codigo', ['Error desconocido'])[0]
                QMessageBox.warning(self, "Error", f"No se pudo agregar el usuario: {mensaje_error}")
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Error de Conexión", "No se puede conectar al servidor")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar usuario: {str(e)}")
    
    def preparar_edicion(self, fila):
        codigo = self.tabla_usuarios.item(fila, 0).text()
        nombre = self.tabla_usuarios.item(fila, 1).text()
        
        self.codigo_input.setText(codigo)
        self.nombre_input.setText(nombre)
        
        # Guardar referencia del usuario que editamos
        self.usuario_editando = int(codigo)
        
        # Cambiar interfaz a modo edición
        self.btn_agregar.setVisible(False)
        self.btn_editar.setVisible(True)
        self.btn_cancelar.setVisible(True)
        
        # Deshabilitar código (no se puede cambiar la PK)
        self.codigo_input.setEnabled(False)
    
    """def guardar_edicion(self):
        if self.usuario_editando is None:
            return
        
        nuevo_nombre = self.nombre_input.text().strip()
        
        if not nuevo_nombre:
            QMessageBox.warning(self, "Nombre vacío", "El nombre no puede estar vacío")
            return
        
        try:
            data = {"codigo": self.usuario_editando, "nombre": nuevo_nombre}
            response = requests.put(f"{self.api_url}/{self.usuario_editando}/", json=data)
            
            if response.status_code == 200:
                self.cargar_usuarios()
                self.cancelar_edicion()
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
            else:
                error_data = response.json()
                mensaje_error = error_data.get('detalles', 'Error desconocido')
                QMessageBox.warning(self, "Error", f"No se pudo actualizar: {mensaje_error}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {str(e)}")"""
            
    def guardar_edicion(self):
        if self.usuario_editando is None:
            return
        
        nuevo_nombre = self.nombre_input.text().strip()
        
        if not nuevo_nombre:
            QMessageBox.warning(self, "Nombre vacío", "El nombre no puede estar vacío")
            return
        
        try:
            data = {"codigo": self.usuario_editando, "nombre": nuevo_nombre}
            print(f"🔄 DEBUG: Intentando actualizar usuario {self.usuario_editando}")
            print(f"📦 DEBUG: Datos enviados: {data}")
            
            response = requests.put(f"{self.api_url}{self.usuario_editando}/", json=data)
            
            print(f"📡 DEBUG: Status code: {response.status_code}")
            print(f"📄 DEBUG: Response headers: {response.headers}")
            print(f"🔍 DEBUG: Response content: {response.text}")
            print(f"🔍 DEBUG: Response encoding: {response.encoding}")
            
            # Verificar si la respuesta es JSON válido
            try:
                response_json = response.json()
                print(f"✅ DEBUG: JSON parseado: {response_json}")
            except:
                print(f"❌ DEBUG: NO se pudo parsear JSON. Contenido: {response.text}")
            
            if response.status_code == 200:
                self.cargar_usuarios()
                self.cancelar_edicion()
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
            else:
                # Mostrar el error real
                error_text = response.text if response.text else "Error sin mensaje"
                QMessageBox.warning(self, f"Error {response.status_code}", f"Detalles: {error_text}")
                
        except Exception as e:
            print(f"💥 DEBUG: Excepción: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {str(e)}")
    
    def eliminar_usuario(self, fila):
        codigo = self.tabla_usuarios.item(fila, 0).text()
        nombre = self.tabla_usuarios.item(fila, 1).text()
        
        confirmacion = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Estás seguro de que quieres eliminar al usuario?\nCódigo: {codigo}\nNombre: {nombre}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            try:
                response = requests.delete(f"{self.api_url}/{codigo}/")
                
                if response.status_code == 200:
                    self.cargar_usuarios()
                    QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {str(e)}")
    
    def cancelar_edicion(self):
        self.limpiar_formulario()
        self.usuario_editando = None
        self.btn_agregar.setVisible(True)
        self.btn_editar.setVisible(False)
        self.btn_cancelar.setVisible(False)
        self.codigo_input.setEnabled(True)
    
    def limpiar_formulario(self):
        self.codigo_input.clear()
        self.nombre_input.clear()
        self.codigo_input.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:8000/api/usuarios/", timeout=2)
    except:
        QMessageBox.critical(None, "Servidor no disponible", 
                           "El servidor Django no está corriendo.\n\n"
                           "Ejecuta en una terminal:\n"
                           "cd ~/crud_usuarios\n"
                           "python manage.py runserver\n\n"
                           "Luego vuelve a ejecutar este programa.")
        sys.exit(1)
    
    window = UsuarioApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
