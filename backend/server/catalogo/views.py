from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import CatalogoSerializer, PedidoSerializer, HeaderApartadosSerializer, BodyApartadosSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import catalogo_model, pedidos_model, cookietem_header_model, cookietem_body_model
from django.utils import timezone
from datetime import timedelta

from .forms import CatalogoForm
from django.db.models import Q

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def productos(request):
    # if isinstance(request, list):
    # Optiene el tipo de entrega
    # 0 - debe regresar todos
    # 1 - Regresa los de entrega inmediata
    # 2 - Regresa lo de sobre pedido
    data = request.data
    if 'search' in data:
        search = data['search']
        get_productos = catalogo_model.objects.filter(
            Q(producto__icontains=search) |
            Q(precio__icontains=search) |
            ~Q(estado='R')
        ).distinct()
    else :
        if data['cambioTipo'] == 0:
            # se obienen todos los productos
            get_productos = catalogo_model.objects.exclude(estado='R')
        else:
            # Se obtienen solo los productos del tipo indicado
            get_productos = catalogo_model.objects.filter(tipo_entrega=data['cambioTipo'])
    # Se envian a serializar el objeto
    serializer = CatalogoSerializer(instance=get_productos, many=True)
    return Response({ "productos": serializer.data }, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agregar_producto(request):
    form = CatalogoForm(request.POST, request.FILES)
    # form = request.data
    if form.is_valid():
        exist_producto = catalogo_model.objects.filter(producto=form.cleaned_data['producto'])
        # exist_trabajo = catalogo_model.objects.filter(guia=form['guia'])
        if exist_producto.exists():
            return Response({ "error": "Ya existe un producto con este nombre" })
        try:

            catalogo_model.objects.create(
                    producto = form.cleaned_data['producto'],
                    precio = form.cleaned_data['precio'],
                    dimensiones = form.cleaned_data['dimensiones'],
                    imagen = form.cleaned_data['imagen'],
                    fecha_registro = timezone.now(),
                    tipo_entrega = form.cleaned_data['tipo_entrega'],
                    inventario = form.cleaned_data['inventario'],
                    comentario = form.cleaned_data['comentario'],
                    estado = 'D'
                )
        except Exception as e:
            print(e)
            return Response({ "error": "Algo salio mal" })

        return Response({ "success": "Producto cargado" }, status=status.HTTP_200_OK)
    else:
        return Response({ "error": "Formulario invalido" })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editar_producto(request):
    form = request.data
    exist_producto = catalogo_model.objects.filter(guia=form['guia'])
    if not exist_producto.exists():
        return Response({ "warning": "No existe el producto" }, status=status.HTTP_404_NOT_FOUND)
    # Verifica que no exista un duplicado con la misma colocación y formato
    duplicado = catalogo_model.objects.filter(producto=form['producto']).exclude(id=form['id'])  # Excluye el actual registro para permitir la actualización

    if duplicado.exists():
        return Response({ "warning": "¡Ya existe un registro con esa colocación y formato!" }, status=status.HTTP_304_NOT_MODIFIED)

    producto = catalogo_model.objects.get(guia=form['guia'])
    producto.producto = form['producto']
    producto.precio = form['precio']
    producto.dimensiones = form['dimensiones']
    producto.imagen = form['imagen']
    producto.tipo_entrega = form['tipo_entrega']
    producto.inventario = form['inventario']
    producto.comentario = form['comentario']
    producto.estado = form['estado']
    producto.save()

    return Response({ "success": "Producto editado" }, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_producto(request):
    form = request.data

    exist_producto = catalogo_model.objects.filter(guia=form['guia'])
    if not exist_producto.exists():
        return Response({ "warning": "No existe el producto" }, status=status.HTTP_404_NOT_FOUND)

    producto = catalogo_model.objects.get(guia=form['guia'])
    producto.delete()

    return Response({ "success": "Producto borrado" }, status=status.HTTP_200_OK)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def getProductoById(request):
    data = request.data

    exist_producto = catalogo_model.objects.filter(id=data['id'])

    if not exist_producto.exists():
        return Response({ "error": "No existe el producto" }, status=status.HTTP_404_NOT_FOUND)
    producto = catalogo_model.objects.get(id=data['id'])

    serializer = CatalogoSerializer(instance=producto)
    return Response({ "producto": serializer.data }, status=status.HTTP_200_OK)

@api_view(['POST'])
def agregar_pedido(request):
    data = request.data
    existe_producto = catalogo_model.objects.get(id=data['id'])
    if not existe_producto:
        return Response({"error", "No se encontró el producto" }, status=status.HTTP_404_NOT_FOUND)
    # Se crea el código de venta
    code_pedido = genera_codigo_venta()
    # | MÉTODO DE SEGURIDAD | Si no es posible generar el código, termina el proceso
    if not code_pedido:
        return Response({"error", "No fue posible agregar el pedido"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        pedidos_model.objects.create(
            codigo_venta = code_pedido,
            codigo_temp = data['codigo_temp'],
            id_producto = data['id'],
            cantidad_vendida = data['cantidad'],
            tipo_entrega = data['tipo_entrega'],
            estado = 1,
            fecha_venta = timezone.now()
        )
    except:
            return Response({ "error": "Algo salio mal al cargar el pedido" })
    return Response({ "success": "Pedido cargado", "code": code_pedido }, status=status.HTTP_200_OK)

@api_view(['POST'])
def setterProduto(request):
    data = request.data

    if not data.get('codigo_temp'):
        producto = catalogo_model.objects.get(id=data['id'])
        if not producto:
            return Response({"error": "No se pudo encontrar el producto"}, status=status.HTTP_404_NOT_FOUND)
        # Revisa si hay sufiente stock
        if producto.inventario < int(data['cantidad']):
            return Response({"error": "No hay suficiente stock"}, status=status.HTTP_426_UPGRADE_REQUIRED)
        # Se obtiene la resta de productos
        nueva_cantidad = producto.inventario - int(data['cantidad'])
        try:
            if nueva_cantidad == 0:
                producto.inventario = nueva_cantidad
                producto.estado = 'R'
            else:
                producto.inventario = nueva_cantidad
            producto.save()
        except:
            return Response({"error": "No se pudo cambiar estado del producto"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        apartados = cookietem_body_model.objects.filter(id_codigo=data['codigo_temp'])
        if not apartados.exists():
            return Response({"error": "No se encontró el apartado"}, status=status.HTTP_400_BAD_REQUEST)
        existe_pedido = pedidos_model.objects.filter(codigo_temp=data['codigo_temp'])
        if not existe_pedido.exists():
            for apartado in apartados:
                catalogo = catalogo_model.objects.filter(id=apartado.producto_id).first()
                nueva_cantidad = catalogo.inventario + apartado.cantidad_prod
                try:
                    catalogo.inventario = nueva_cantidad
                    catalogo.estado = 'D'
                    catalogo.save()
                except:
                    return Response({"error": "No fue posible actualiar el producto"}, status=status.HTTP_400_BAD_REQUEST)
                apartado.delete()
            try:
                cookietem_header_model.objects.filter(codigo_temp=data['codigo_temp']).delete()
            except:
                return Response({"error": "No fue el borrado de registro temporal"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"success": "Producto actualizado"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def apartados(request):
    data = request.data
    actualizar = False

    producto = catalogo_model.objects.get(id=data['id_prod'])
    if not producto:
        return Response({"error": "No se pudo encontrar el producto"}, status=status.HTTP_404_NOT_FOUND)
    # Si no viene un codigo temporal, lo genera
    if data['codigo_temp'] == "":
        # Genera y valida codigo temporal
        codigo = genera_codigo_venta()
        if not codigo:
            return Response({"error": "No fue posible apartar el producto"}, status=status.HTTP_404_NOT_FOUND)
    else:
        codigo = data['codigo_temp']
        actualizar = True
    try:
        if not actualizar:
            # Agrega nuevo registro
            timeexpired = timezone.now() + timedelta(minutes=2)
            cookietem_header_model.objects.create(
                codigo_temp = codigo,
                fecha_expiracion = timeexpired,
                fecha_registro = timezone.now()
            )
            cookietem_body_model.objects.create(
                id_codigo = codigo,
                producto_id = data['id_prod'],
                cantidad_prod = data['cantidad']
            )
            return Response({ "success": "Producto apartado", "cod_tem": codigo, "time_expired": timeexpired.isoformat() }, status=status.HTTP_200_OK)
        else:
            temporal = cookietem_header_model.objects.get(codigo_temp=codigo)
            if not temporal:
                return Response({"error": "No se pudo encontrar la información temporal"}, status=status.HTTP_404_NOT_FOUND)
            # Actualiza la información
            temporal_producto = cookietem_body_model.objects.filter(id_codigo=codigo, producto_id=data['id_prod']).first()
            if not temporal_producto:
                cookietem_body_model.objects.create(
                    id_codigo = codigo,
                    producto_id = data['id_prod'],
                    cantidad_prod = data['cantidad']
                )
            else:
                temporal_producto.cantidad_prod = temporal_producto.cantidad_prod + int(data['cantidad'])
                temporal_producto.save()

            return Response({ "success": "Producto actualizado", "cod_tem": codigo, "time_expired": temporal.fecha_expiracion.isoformat() }, status=status.HTTP_200_OK)
    except:
        return Response({"error": "Algo salio mal al apartar produto"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_expiracion(request):
    data = request.data

    expiracion = cookietem_header_model.objects.get(codigo_temp=data['codigo'])
    if not expiracion:
        return Response({"error": "No hay registro de expiración"}, status=status.HTTP_404_NOT_FOUND)

    serializer = HeaderApartadosSerializer(instance=expiracion)
    return Response({ "productos": serializer.data }, status=status.HTTP_200_OK)

def genera_codigo_venta(limit=6):
    import random, string

    MiCadena = string.ascii_letters + string.digits
    # code1 = "".join(random.choice(MiCadena) for j in range(random.randint(2,2)))
    contador = 0
    contension = False
    while True:
        contador+=1
        if contador > 10:
            limit+=1
        code = "".join(random.choice(MiCadena) for j in range(random.randint(4,limit)))
        exist_pedido = pedidos_model.objects.filter(codigo_temp='BK_' + code, estado=1)
        exist_cookie = cookietem_header_model.objects.filter(codigo_temp='BK_' + code)
        if exist_pedido.exists() or exist_cookie.exists():
            if contador > 20:
                contension = True
                break
            continue
        break
    if contension:
        codigo = False
    else:
        codigo = 'BK_' + code
    return codigo