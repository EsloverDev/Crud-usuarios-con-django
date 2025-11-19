from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['codigo', 'nombre']
        
    def validate_codigo(self, value):
        """Validar que el código sea único, excluyendo la instancia actual"""
        # Excluir la instancia actual si estamos actualizando
        instance = getattr(self, 'instance', None)
        
        if instance:
            # Si estamos actualizando, excluir este mismo usuario
            if Usuario.objects.filter(codigo=value).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError("Este código ya existe")
        else:
            # Si estamos creando, verificar normalmente
            if Usuario.objects.filter(codigo=value).exists():
                raise serializers.ValidationError("Este código ya existe")
        
        return value
