from django.db import models

class Usuario(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
