from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('feriados/', views.listar_feriados, name='listar_feriados'),
    path('feriados/novo/', views.criar_feriado, name='criar_feriado'),
    path('agenda/', views.agenda, name='agenda'),
    # path('responder-email/<int:email_id>/', views.responder_email, name='responder_email'),

]
