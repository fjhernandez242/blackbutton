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
from datetime import timedelta, date

from .forms import CatalogoForm
from django.db.models import Q, F, Count
import calendar

@api_view(['POST'])
def productos(request):
    # if isinstance(request, list):
    # Optiene el tipo de entrega
    # 0 - debe regresar todos
    # 1 - Regresa los de entrega inmediata
    # 2 - Regresa lo de sobre pedido
    data = request.data
    if data.get('search'):
        search = data['search']
        get_productos = catalogo_model.objects.filter(
            Q(producto__icontains=search) |
            Q(precio__icontains=search) |
            ~Q(estado='D')
        ).distinct()
    else :
        if data['cambioTipo'] == 0:
            # se obienen todos los productos
            filtros = {}
            if not data.get('todos'):
                filtros['estado'] = 'D'
            # Pasamos los filtros usando **
            # Si filtramos está vacío, equivale a .all()
            get_productos = catalogo_model.objects.filter(**filtros)
        else:
            # Se obtienen solo los productos del tipo indicado
            get_productos = catalogo_model.objects.filter(tipo_entrega=data['cambioTipo'], estado='D')
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
    exist_producto = catalogo_model.objects.filter(id=form['id'])
    if not exist_producto.exists():
        return Response({ "warning": "No existe el producto" }, status=status.HTTP_404_NOT_FOUND)
    # Verifica que no exista un duplicado con la misma colocación y formato
    duplicado = catalogo_model.objects.filter(producto=form['producto']).exclude(id=form['id'])  # Excluye el actual registro para permitir la actualización

    if duplicado.exists():
        return Response({ "warning": "¡Ya existe un amigurimi con ese nombre!" }, status=status.HTTP_200_OK)
    try:
        producto = catalogo_model.objects.get(id=form['id'])
        producto.producto = form['producto']
        producto.precio = form['precio']
        producto.dimensiones = form['dimensiones']
        if form.get('imagen'): ## Se garda la imagen solo si viene una
            producto.imagen = form['imagen']
        producto.tipo_entrega = form['tipo_entrega']
        producto.comentario = form['comentario']
        producto.inventario = form['inventario']
        producto.estado = form['estado']
        producto.save()

        return Response({ "success": "Producto editado" }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": "No fue posible actualizar el producto" }, status=status.HTTP_400_BAD_REQUEST)

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPedidoByClave(request):
    data = request.data
    get_pedido = None
    if data.get('tipo') == 'cve':
        # Validamos que exista el pedido con base a la clave
        get_pedido = pedidos_model.objects.filter(codigo_venta=data['dato'])
    elif data.get('tipo') == 'fecha':
        if not data.get('filtro'):
            if not data.get('dato')['fini']:
                get_pedido = pedidos_model.objects.filter(fecha_venta=data['dato']).order_by('-id')
            else:
                get_pedido = pedidos_model.objects.filter(fecha_venta__range=(data.get('dato')['fini'], data.get('dato')['ffin'])).order_by('-id')
        elif data.get('filtro'):
            hoy = timezone.localdate()
            anio = hoy.year
            mes = hoy.month
            if data.get('dato') == 'h':
                get_pedido = pedidos_model.objects.filter(fecha_venta=hoy).order_by('-id')
            elif data.get('dato') == 'e':
                _, ultimo_dia = calendar.monthrange(anio, mes)
                mes_inicio = hoy.replace(day=1)
                mes_ultimo = hoy.replace(day=ultimo_dia)
                get_pedido = pedidos_model.objects.filter(fecha_venta__range=(mes_inicio, mes_ultimo)).order_by('-id')
            elif data.get('dato') == 'a':
                primer_dia_mes_actual = hoy.replace(day=1)
                fecha_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
                anio_anterior = fecha_mes_anterior.year
                mes_anterior = fecha_mes_anterior.month
                _, ultimo_dia = calendar.monthrange(anio_anterior, mes_anterior)
                primer_dia_final = fecha_mes_anterior.replace(day=1)
                ultimo_dia_final = fecha_mes_anterior.replace(day=ultimo_dia)

                get_pedido = pedidos_model.objects.filter(fecha_venta__range=(primer_dia_final, ultimo_dia_final)).order_by('-id')

    if get_pedido is None:
        return Response({"error": "No se proporciono una clave o fecha valida para la búsqueda"}, status=status.HTTP_200_OK)
    if not get_pedido.exists():
        return Response({"info": "No se encontraron pedidos"}, status=status.HTTP_200_OK)
    # Se recorre cada pedido

    recopilado = {}
    for pedido in get_pedido:
        producto = catalogo_model.objects.filter(id=pedido.id_producto).first()
        if producto is not None:
            url_imagen = None
            if producto.imagen:
                url_imagen = request.build_absolute_uri(producto.imagen.url)

            periodo = pedido.fecha_venta.strftime('%d/%m/%Y')
            cve_venta = pedido.codigo_venta

            precio_actual = float(producto.precio)
            cantidad_actual = int(pedido.cantidad_vendida)
            subtotal_actual = precio_actual * cantidad_actual

            if periodo not in recopilado:
                recopilado[periodo] = {}

            if cve_venta not in recopilado[periodo]:
                recopilado[periodo][cve_venta] = {
                    'productos': [],
                    'total_productos': 0,
                    'total_costo': 0.0
                }

            # Suma de cantidades
            recopilado[periodo][cve_venta]['total_productos'] += cantidad_actual
            recopilado[periodo][cve_venta]['total_costo'] += subtotal_actual

            # Se agregan producto
            recopilado[periodo][cve_venta]['productos'].append({
                'nombre': producto.producto,
                'precio': float(producto.precio),
                'tipo_entrega': producto.tipo_entrega,
                'estado': pedido.estado,
                'imagen': url_imagen,
                'cantidad': pedido.cantidad_vendida,
                'codigo_temp': pedido.codigo_temp,
                'estado_pedido': pedido.estado,
            })
        else:
            return Response({ "info": 'No se encontró el producto en cátalogo' }, status=status.HTTP_200_OK)
    return Response({ "pedido": recopilado }, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cambioEstadoVenta(request):
    data = request.data
    exist_pedido = pedidos_model.objects.filter(codigo_venta=data['cve'])
    if not exist_pedido.exists():
        return Response({'error': 'No se encontró el pedido'}, status=status.HTTP_404_NOT_FOUND)
    try:
        # Cambia a estado Completado todos los registros con el codigo de venta indicado
        if data['estado'] == 'completar':
            # Se indica el estado para cambio en el pedido
            estadoNumero = 2
        else:
            # Acciones en secuencia para cuando es cancelado un pedido
            for pedido in exist_pedido:
                if pedido.codigo_temp != '':
                    # Buscamos la información de los productos apartados
                    apartados_body = cookietem_body_model.objects.filter(id_codigo=pedido.codigo_temp)
                    for apartado in apartados_body:
                        producto = catalogo_model.objects.filter(id=apartado.producto_id).first()
                        if not producto:
                            return Response({'error': 'No se logró cancelar el peddido; no se encontró el producto'}, status=status.HTTP_400_BAD_REQUEST)
                        # Si se encuentra el producto que cambio de tipo, se regreda a tipo "Entrega inmediata"
                        if producto.tipo_entrega == 2 and producto.inventario == 0:
                            producto.tipo_entrega = 1
                        # Le suma la cantidad de productos que habían sido aparatados
                        producto.inventario = producto.inventario + apartado.cantidad_prod
                        producto.save()
            # Se indica el estado para cambio en el pedido
            estadoNumero = 3
        # Acciones en secuencia para completar el pedido
        # Si hay un código temporal, se rastrea y se elimina
        try:
            for pedido in exist_pedido:
                if pedido.codigo_temp != '':
                    # Elimina el código temporal de la cabecera
                    cookietem_header_model.objects.filter(codigo_temp=pedido.codigo_temp).delete()
                    # Elimina los códigos temporales que puedan haber en el body
                    apartados_body = cookietem_body_model.objects.filter(id_codigo=pedido.codigo_temp)
                    for apartado in apartados_body:
                        apartado.delete()
        except Exception as e:
            return Response({'error': 'No se logró completar el pedido: ' + e}, status=status.HTTP_400_BAD_REQUEST)
        # Realiza el cambio de estadi en el pedido
        exist_pedido.update(estado=estadoNumero)
    except:
        return Response({'error': 'No se pudo completar la venta'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'Correcto': 'Estado cambiado'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def calculoMovimientos(request):
    data = request.data
    # Buscamos todos las ventas completadas
    existen_registros = pedidos_model.objects.exists()
    if not existen_registros:
        return Response({
        'ventas_proceso': 0,
        'ventas_completas': 0,
        'ventas_canceladas': 0
    })
    # Obtenemos la fecha actual
    ahora = timezone.localtime(timezone.now()).date()
    # Manejo de periodo segun filtro
    inicio_mes_actual = ahora.replace(day=1)
    if data['periodo'] == 'H': # Filtra para el día actual
        # Reliza el filtrado
        filtrado_periodo = pedidos_model.objects.filter(fecha_venta__gte=ahora)
    elif data['periodo'] == 'E': # Filtra para este mes
        if inicio_mes_actual.month == 12:
            fini_mes_siguiente = date(inicio_mes_actual.year + 1, 1, 1)
        else:
            fini_mes_siguiente = inicio_mes_actual.replace(month=inicio_mes_actual.month + 1, day=1)
        fin_mes_actual = fini_mes_siguiente - timedelta(days=1)

        # Reliza el filtrado
        filtrado_periodo = pedidos_model.objects.filter(fecha_venta__range=[inicio_mes_actual, fin_mes_actual])

    elif data['periodo'] == 'A': # Filtra para mes anterior
        ffin_mes_anterior = inicio_mes_actual - timedelta(days=1)

        fini_mes_anterior = ffin_mes_anterior.replace(day=1)

        # Reliza el filtrado
        filtrado_periodo = pedidos_model.objects.filter(fecha_venta__range=[fini_mes_anterior, ffin_mes_anterior])
    elif data['periodo'] == 'T': # Muestra todos los registros
        filtrado_periodo = pedidos_model.objects.all()

    # Con la información filtrada, se realiza el conteo de ventas
    estadisticas_ventas = filtrado_periodo.aggregate(
        # Cuenta los 'codigo_venta' unicos donde el estado es 2
        completas = Count('codigo_venta',filter=Q(estado=2),distinct=True),
        # Cuenta los 'codigo_venta' unicos donde el estado es 3
        canceladas = Count('codigo_venta',filter=Q(estado=3),distinct=True)
    )

    # Calcula todas los procesos en estado 1
    estadisticas_en_proceso = pedidos_model.objects.aggregate(
        # Cuenta los 'codigo_venta' unicos donde el estado es 1
        proceso = Count('codigo_venta',filter=Q(estado=1),distinct=True),
    )

    return Response({
        'ventas_proceso': estadisticas_en_proceso['proceso'],
        'ventas_completas': estadisticas_ventas['completas'],
        'ventas_canceladas': estadisticas_ventas['canceladas']
    })

@api_view(['POST'])
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
    try:
        # Revisa que no venga un codigo de pedido
        if data['pedido'] == '':
            # Se crea el código de venta si no viene uno
            code_pedido = genera_codigo_venta()
        else:
            # Se agrega el código de venta si viene
            code_pedido = data['pedido']
        for pedido in data.get('datos'):
            existe_producto = catalogo_model.objects.get(id=pedido['id'])
            if not existe_producto:
                return Response({"error", "No se encontró el producto" }, status=status.HTTP_404_NOT_FOUND)

            # | MÉTODO DE SEGURIDAD | Si no es posible generar el código, termina el proceso
            if not code_pedido:
                return Response({"error", "No fue posible agregar el pedido"}, status=status.HTTP_400_BAD_REQUEST)
            if pedido['tipo_entrega'] == 1:
                dato_temp = data['codigo_temp']
            else:
                dato_temp = ''
            pedidos_model.objects.create(
                codigo_venta = code_pedido,
                codigo_temp = dato_temp,
                id_producto = pedido['id'],
                cantidad_vendida = pedido['quantity'],
                tipo_entrega = pedido['tipo_entrega'],
                estado = 1,
                fecha_venta = timezone.localdate()
            )
        return Response({ "success": "Pedido cargado", "code": code_pedido }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({ "error": "Algo salio mal al cargar el pedido: " })

@api_view(['POST'])
def setterProducto(request):
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
            # Al terminar con el stock disponible, el prouducto pasará a tipo de entrega "Sobre pedido"
            if nueva_cantidad == 0:
                producto.inventario = nueva_cantidad
                producto.tipo_entrega = 2
            else:
                producto.inventario = nueva_cantidad
            producto.save()
        except:
            return Response({"error": "No se pudo cambiar estado del producto"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Busca el apartado relacionado al codigo temporal
        apartados = cookietem_body_model.objects.filter(id_codigo=data['codigo_temp'])
        if not apartados.exists():
            return Response({"error": "No se encontró el apartado"}, status=status.HTTP_400_BAD_REQUEST)
        # Revisa que no se haya completado el pedido aún
        existe_pedido = pedidos_model.objects.filter(codigo_temp=data['codigo_temp']).first()
        if not existe_pedido or existe_pedido.estado != '1':
            for apartado in apartados:
                catalogo = catalogo_model.objects.filter(id=apartado.producto_id).first()
                if not data.get('id_prod'):
                    suma = apartado.cantidad_prod
                else:
                    suma = 1
                nueva_cantidad = catalogo.inventario + suma
                try:
                    # Actualiza catalogo
                    # Revisa el tipo de entrega
                    if catalogo.tipo_entrega == 2:
                        # Valida si aún productos en apartados
                        existe_ref_apartado = cookietem_body_model.objects.filter(id_codigo=data['codigo_temp'])
                        if existe_ref_apartado.exists():
                            # Si ya no hay apartados, y estos son regresados, se actualiza el tipo de entrega
                            catalogo.tipo_entrega = 1
                    catalogo.inventario = nueva_cantidad
                    catalogo.save()
                    # Actualiza apartado
                    if not data.get('id_prod'):
                        apartado.delete()
                    else:
                        if (apartado.producto_id == data['id_prod']):
                            if apartado.cantidad_prod == 1:
                                # apartado.cantidad_prod = apartado.cantidad_prod - 1
                                apartado.delete()
                            else:
                                apartado.cantidad_prod = apartado.cantidad_prod - 1
                                apartado.save()
                except:
                    return Response({"error": "No fue posible actualiar el producto"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Al vaciarse la tabla de body, se borrará el encabezado
                apartados_body = cookietem_body_model.objects.filter(id_codigo=data['codigo_temp'])
                if not apartados_body.exists():
                    # Realiza borrado del registro en tabla header
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
            timeexpired = timezone.now() + timedelta(minutes=15) # Se asigna tiempo del temporizador en minutos
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

@api_view(['GET'])
def codigo_venta(request):
    codigo = genera_codigo_venta()
    return Response({ 'codigoVenta': codigo }, status=status.HTTP_200_OK)

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
