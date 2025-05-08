from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),  # Página inicial
    # path('feriados/', views.listar_feriados, name='listar_feriados'),
    # path('feriados/novo/', views.criar_feriado, name='criar_feriado'),
    path('', views.agenda, name='agenda'),
    # path('configurar-email/', views.configurar_email, name='configurar_email'),
    # path('emails/', views.listar_emails, name='listar_emails'),
]
