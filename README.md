# CRUD Usuarios - Proyecto DevOps

Backend Django + Frontend PyQt para taller de DevOps con Jenkins, SonarQube y Kubernetes.

## Estructura
- `crud_usuarios/` - Backend Django con API REST
- `proyecto_crud/` - Frontend PyQt

## Requisitos
- Python 3.8+
- Django 4.2+
- PyQt5
- Django REST Framework

## Instalación
```bash
# Backend
cd crud_usuarios
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

# Frontend  
cd proyecto_crud
python frontend_usuarios.py
