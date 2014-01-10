# -*- encoding: utf-8 -*-
from __builtin__ import type
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from boru.settings import PAGINADO_PRODUCTOS
from .forms import modificarMesa
from django.core.urlresolvers import reverse
from gestiones.Salon.altamesa.models import Mesa


@permission_required('Administrador.is_admin', login_url="login")
def modificarmesa(request, id_mesa=None):

    mesas_lista = Mesa.objects.all().order_by('sector')
    paginator = Paginator(mesas_lista, PAGINADO_PRODUCTOS)
    mesas = paginator.page(1)

    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaMesa = Mesa.objects.get(pk=id_mesa)

        #creo diccionario con los datos del mozo para mostrarlos ne el formulario
        datosMesa = {'id': unaMesa.id, 'tipo': unaMesa.tipo, 'capacidad': unaMesa.capacidad,
                     'ocupada': unaMesa.ocupada, 'activo': unaMesa.activo, 'sector': unaMesa.sector}
        mesa_id = unaMesa.id
    except:
        datosMesa = ''
        unaMesa = None
        mesa_id = 0

    #si se apreto el boton de modificar
    if request.method == 'POST' and unaMesa != None:

        #le indico al form que tome los datos del request y le paso la instancia de user que obtuve mas arriba
        formulario = modificarMesa(request.POST, instance=unaMesa)

        #si el formulario es valido
        if formulario.is_valid():
            #rescato los datos de cada cmapo y los limpio
            tipo = formulario.cleaned_data['tipo']
            capacidad = formulario.cleaned_data['capacidad']
            ocupada = formulario.cleaned_data['ocupada']
            activo = formulario.cleaned_data['activo']
            sector = formulario.cleaned_data['sector']

            #seteo los nuevos datos en el objeto usuarioMozo que obtuvimos al principio
            unaMesa.tipo = tipo
            unaMesa.capacidad = capacidad
            unaMesa.ocupada = ocupada
            unaMesa.activo = activo
            unaMesa.sector = sector
            unaMesa.save()

            #mostramos que la operacion fue exitosa
            return render_to_response('Salon/modificarmesa/modificarmesaexito.html',
                                      {'formulario': formulario, 'mesas': mesas},
                                      context_instance=RequestContext(request))

        #si no es valido el formulario lo vuelvo a mostrar con los datos ingresados
        return render_to_response('Salon/modificarmesa/modificarmesa.html',
                                  {'formulario': formulario, 'mesas': mesas, 'id_mesa': mesa_id},
                                  context_instance=RequestContext(request))

    else:
        #si no paretamos el boton modificar mozo y seleccionamos algun mozo mostramos sus datos, sino mostramos el form vacio
        formulario = modificarMesa(initial=datosMesa)
        return render_to_response('Salon/modificarmesa/modificarmesa.html',
                                  {'formulario': formulario, 'mesas': mesas, 'id_mesa': mesa_id},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def modificarmesadel(request, id_mesa):
    try:
        #obtengo en el caso de que venga el id por GET, al usuario
        unaMesa = Mesa.objects.get(pk=id_mesa)
    except:
        unaMesa = None

    #si se apreto el boton de modificar
    if request.method == 'GET' and unaMesa != None:

        unaMesa.cambiarEstado()
        unaMesa.save()

    return HttpResponseRedirect(reverse('modificarmesa'))




@permission_required('Administrador.is_admin', login_url="login")
def buscarmesasajax(request):
    if request.method == 'GET':
        q = request.GET['q']
        print(type(q))
        listado = Mesa.objects.filter( id=q ).order_by('sector')[:30]
        print("listado mesas ajax")
        print(listado)
        return render_to_response('Salon/modificarmesa/busquedaresultados.html', {'listado': listado},
                                  context_instance=RequestContext(request))


@permission_required('Administrador.is_admin', login_url="login")
def buscarmesasajaxResultados(request):
    if request.method == 'GET':
        q = request.GET['q']
        print(type(q))
        if q != "":
            mesas = Mesa.objects.filter( id=q ).order_by('sector')
        else:
            mesas_lista = Mesa.objects.all().order_by("sector")
            paginator = Paginator(mesas_lista, PAGINADO_PRODUCTOS)
            mesas = paginator.page(1)

        return render_to_response('Salon/modificarmesa/busquedaresultados_items.html', {'mesas': mesas},
                                  context_instance=RequestContext(request))





@permission_required('Administrador.is_admin', login_url="login")
def paginadorajaxResultados(request):

    if request.method == 'GET':

        pagina = request.GET['pagina']
        mesas_lista = Mesa.objects.all().order_by('sector')
        paginator = Paginator(mesas_lista, PAGINADO_PRODUCTOS)

        try:
            mesas = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            mesas = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            mesas = paginator.page(paginator.num_pages)

        return render_to_response('Salon/modificarmesa/busquedaresultados_items.html', {'mesas': mesas},
                                  context_instance=RequestContext(request))



