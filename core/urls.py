"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gastos.views import (
    gastos_view, agregar_gasto_view, gestionar_gasto_view, 
    editar_gasto_view, eliminar_gasto_view, dinero_enviado_view, 
    agregar_envio_view, vaciar_historial_view, gestionar_estado_view,
    dinero_afp_view, agregar_gasto_afp_view, editar_gasto_afp_view, eliminar_gasto_afp_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gastos_view, name='gastos'),
    path('agregar/', agregar_gasto_view, name='agregar_gasto'),
    path('gestionar/', gestionar_gasto_view, name='gestionar_gasto'),
    path('editar/<int:gasto_id>/', editar_gasto_view, name='editar_gasto'),
    path('eliminar/<int:gasto_id>/', eliminar_gasto_view, name='eliminar_gasto'),
    path('dinero-enviado/', dinero_enviado_view, name='dinero_enviado'),
    path('agregar-envio/', agregar_envio_view, name='agregar_envio'),
    path('vaciar-historial/', vaciar_historial_view, name='vaciar_historial'),
    path('gestionar-estado/<str:persona>/', gestionar_estado_view, name='gestionar_estado'),
    path('dinero-afp/', dinero_afp_view, name='dinero_afp'),
    path('agregar-gasto-afp/', agregar_gasto_afp_view, name='agregar_gasto_afp'),
    path('editar-gasto-afp/<int:gasto_id>/', editar_gasto_afp_view, name='editar_gasto_afp'),
    path('eliminar-gasto-afp/<int:gasto_id>/', eliminar_gasto_afp_view, name='eliminar_gasto_afp'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
