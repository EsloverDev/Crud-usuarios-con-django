from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    # Personalizar la creación para mejor manejo de errores
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'mensaje': 'Usuario creado exitosamente',
                'usuario': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'Error al crear usuario',
            'detalles': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Personalizar actualización
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'mensaje': 'Usuario actualizado exitosamente',
                'usuario': serializer.data
            })
        return Response({
            'error': 'Error al actualizar usuario',
            'detalles': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Personalizar eliminación
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'mensaje': 'Usuario eliminado exitosamente'
        }, status=status.HTTP_200_OK)
