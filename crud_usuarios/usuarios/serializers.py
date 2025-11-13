from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['codigo', 'nombre']
        
    def validate_codigo(self, value):
        """Validar que el código sea único"""
        if Usuario.objects.filter(codigo=value).exists():
            raise serializers.ValidationError("Este código ya existe")
        return value
