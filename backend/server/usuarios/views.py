from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.models import User

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Se elimina el token anterior
            Token.objects.filter(user=user).delete()
            # Se crea un nuevo token
            token = Token.objects.create(user=user)
            return Response({ "token": token.key, 'user': user.username }, status=status.HTTP_200_OK)
        else:
            return Response({ "error": "Cuenta desactivada" }, status=status.HTTP_200_OK)

    return Response({"error": "Usuario o contraseña invalidos"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Token.objects.filter(user=data['user']).delete()
        request.user.auth_token.delete()
        return Response({ 'correcto': 'Token eliminado'}, status=status.HTTP_200_OK)
    except:
        return Response({ 'error': 'No se pudo cerrar sesión'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return Response({ "token": token.key, "user": serializer.data }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUsers(request):
    usuarios = User.objects.all()

    serializador = UserSerializer(instance=usuarios, many=True)

    return Response({ "usuarios": serializador.data }, status=status.HTTP_200_OK)