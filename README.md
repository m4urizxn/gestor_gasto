# Gestor de Gastos Familiares

Sistema de gestión de gastos familiares desarrollado en Django.

## Características

- Gestión de gastos por persona (Mamá, Mauricio, Papá)
- Estados de pago (Falta Pagar, Pagado, No se Pagó)
- Conversión automática de EUR a PEN
- Registro de envíos de dinero
- Gestión de dinero AFP con comprobantes
- Sistema de archivos adjuntos con imágenes

## Tecnologías

- Django 5.1.15
- Python 3.x
- PostgreSQL / SQLite
- Tailwind CSS
- WhiteNoise (archivos estáticos)
- Gunicorn (servidor producción)
- Pillow (procesamiento de imágenes)

## Instalación Local

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Linux/Mac)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Crear variables de entorno (opcional): archivo `.env` con:
   - `SECRET_KEY=tu-clave-secreta`
   - `DEBUG=True`
6. Ejecutar migraciones: `python manage.py migrate`
7. Crear superusuario: `python manage.py createsuperuser`
8. Ejecutar servidor: `python manage.py runserver`

## Despliegue en Render

1. Crear cuenta en [Render](https://render.com)
2. Conectar repositorio de GitHub
3. Crear nuevo Web Service
4. Configurar:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn core.wsgi:application`
5. Variables de entorno en Render:
   - `SECRET_KEY`: Generar clave segura
   - `DEBUG`: `False`
   - `DATABASE_URL`: URL de PostgreSQL (automático si añades DB)
   - `PYTHON_VERSION`: `3.13.0` (o tu versión)

## Estructura del Proyecto

```
gestor_gastos/
├── core/              # Configuración Django
├── gastos/            # App principal
│   ├── models.py      # Modelos (Gasto, DineroEnviado, GastoAFP)
│   ├── views.py       # Vistas
│   ├── templates/     # Plantillas HTML
│   └── migrations/    # Migraciones BD
├── media/             # Archivos subidos (comprobantes)
├── staticfiles/       # Archivos estáticos (generado)
├── manage.py
├── requirements.txt
└── build.sh           # Script despliegue Render
```

## Funcionalidades

### Gastos Generales
- Agregar gastos por persona
- Editar y eliminar gastos
- Gestionar estados de pago
- Visualización por persona con totales

### Dinero Enviado
- Registro de envíos en EUR
- Conversión automática a PEN
- Cálculo de faltante por persona
- Historial de envíos

### Dinero AFP
- Monto inicial: S/ 5,350.00
- Registro de gastos con comprobantes
- Cálculo automático de saldo restante
- Editar y eliminar gastos AFP
- Visualización de comprobantes

## Licencia

Proyecto privado
