# models.py
from django.db import models
import datetime

class FeriadoPersonalizado(models.Model):
    TIPOS = [
        ("nacional", "Nacional"),
        ("estadual", "Estadual"),
        ("municipal", "Municipal"),
        ("facultativo", "Ponto Facultativo"),
    ]


    nome = models.CharField(max_length=100)
    data = models.DateField(default=datetime.date.today)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="nacional")
    estado = models.CharField(max_length=2, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.data.strftime('%d/%m/%Y')} ({self.tipo})"
