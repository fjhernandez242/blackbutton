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
from .models import codigo_recuperacion_model
from django.utils import timezone
from datetime import timedelta

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
def get_users(request):
    usuarios = User.objects.all()

    serializador = UserSerializer(instance=usuarios, many=True)

    return Response({ "usuarios": serializador.data }, status=status.HTTP_200_OK)

@api_view(['POST'])
def enviar_codigo(request):
    ahora = timezone.localtime(timezone.now()).date()

    # Contar cuántos códigos se han generado en un lapso de 24 horas
    codigos_enviados = codigo_recuperacion_model.objects.filter(periodo=ahora).count()
    # Validar el límite
    if codigos_enviados >= 2:
        return Response(
            {
                'error': 'Has superado el límite de 3 intentos de recuperación por día. Intentalo mañana.',
                'mensaje': 'limite'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    # De define una ventana de tiempo de 24 horas
    # Verificamos que no haya otros códigos activos
    exist_code_active = codigo_recuperacion_model.objects.filter(estado='D')
    if exist_code_active.exists():
        # Si existen códigos activos, los desactiva antes de crear uno nuevo
        exist_code_active.update(estado='U')

    # Inicia el proceso de creación y envio del nuevo código
    import smtplib, secrets, os
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from django.conf import settings

    # Genera codigo de verificación
    code = str(secrets.randbelow(900000) + 100000)
    # Se crea el contenedor
    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = 'Código de recuperación de contraseña - BlackButton'
    mensaje['From'] = settings.EMAIL_USER
    mensaje['To'] = settings.EMAIL_DESTINO

    # 3. Diseño en HTML del correo
    html = f"""
    <html>
      <body style="font-family: 'Montserrat', sans-serif; color: #333; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
          <h2 style="color: #c0392b; text-align: center;">BlackButton</h2>
          <hr style="border: 0; border-top: 1px solid #eee;">
          <p>Hola,</p>
          <p>Has solicitado restablecer tu contraseña. Utiliza el siguiente código de seguridad para continuar con el proceso:</p>
          <div style="text-align: center; margin: 30px 0;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #c0392b; background: #fdf2f2; padding: 10px 20px; border-radius: 5px; border: 1px dashed #c0392b;">
              {code}
            </span>
          </div>
          <p style="font-size: 12px; color: #777;">Este código es de un solo uso. Si tú no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
        </div>
      </body>
    </html>
    """

    parte_html = MIMEText(html, 'html')
    mensaje.attach(parte_html)

    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls() # Cifrado seguro TLS
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_USER, settings.EMAIL_DESTINO, mensaje.as_string())
        server.quit()

        # Se guarda el código para consulta
        codigo_recuperacion_model.objects.create(
            codigo = code,
            estado = 'D',
            periodo = timezone.localtime(timezone.now()).date(),
            fecha_registro = timezone.now()
        )

        return Response({ 'correcto': 'Código de verificación enviado' }, status=status.HTTP_200_OK)
    except Exception as e:
        # 🌟 Esto imprimirá el error real en tu terminal de Django (Ej: Bad credentials, Connection timed out, etc.)
        print("ERROR REAL SMTP:", str(e))

        # También lo mandamos en la respuesta para que lo veas desde Postman o Vue
        return Response({
            'error': 'No fue posible enviar el correo de recuperación',
            'detalle_tecnico': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def validar_codigo(request):
    data = request.data
    try:
        # Validación 1: Verifica que exista el código
        registro_codigo = codigo_recuperacion_model.objects.filter(
            codigo=data['codigo'],
            estado='D').first()
        if not registro_codigo:
            return Response({ 'error': 'No existe el código de recuperación', 'mensaje': 'inexistente' }, status=status.HTTP_404_NOT_FOUND)
        # Validación 2:  Verifica el tiempo de expiración
        # Obtenemos la hora actual
        hoy = timezone.now()
        # Calculamos el punto en el tiempo hace 5 minutos (nuestro umbral de expiración)
        tiempo_limite = hoy - timedelta(minutes=5)
        if registro_codigo.fecha_registro <= tiempo_limite:
            # El código existia pero ya pasaron los 5 minutosl, así que lo quemamos
            registro_codigo.estado = 'E'
            registro_codigo.save()

            return Response({ 'error': 'El código de recuperación ha expirado.', 'mensaje': 'expirado' }, status=status.HTTP_404_NOT_FOUND)
        # Si todo avanza sin problemas, se realiza el cambio del estado a "USADO"
        # Se cambia el estado a USADO
        registro_codigo.estado = 'U'
        registro_codigo.save()

        return Response({ 'Correcto': 'Código valido' }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ 'error': 'No fue posible usar el código de recuperación' }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cambiar_contrasena(request):
    data = request.data
    try:
        # Valida que las contraseñas sean iguales
        if data['password1'] != data['password2']:
            return Response({ 'error': 'Contraseñas no coinciden' }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username='weya')
        if user:
            user.set_password(data['password2'])
            user.save()

            return Response({ 'correcto': 'Contraseña cambiada con exito' }, status=status.HTTP_200_OK)
        else:
            return Response({ 'error': 'Usuario no encontrado' }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({ 'error': 'No fue posible cambiar la contraseña' }, status=status.HTTP_400_BAD_REQUEST)