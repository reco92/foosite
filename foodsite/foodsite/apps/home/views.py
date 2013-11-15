# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from foodsite.apps.ventas.models import Restaurante,Platillo,Registro_reservacion,Registro_pedido,Cliente
from foodsite.apps.home.forms import RegistroForm,LoginForm,Reservacion_registroForm, Pedido_registroForm
from django.contrib.auth.models import User

from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
import datetime 
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


def index_view(request):
	return render_to_response('home/index.html',context_instance =RequestContext(request)) # si kiero jalar de otra carpeta foodsite/templates/home/index.html

def about_view(request):
	mensaje = 'Url en mantenimiento'
	ctx = {'msg':mensaje}
	return render_to_response('home/about.html',ctx,context_instance =RequestContext(request))
def platos_view(request):
	#print >>sys.stderr, 'Goodbye, cruel world!'
	if request.user.is_authenticated(): 
		ya_compro = False
		hay_platos = False
		mensaje = ''
		if request.method == "POST":
			formulario = Pedido_registroForm(request.POST)
			if formulario.is_valid():
				platillof = formulario.cleaned_data['platillo_id']
				session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
				session = Session.objects.get(session_key=session_key)
				id_usuario = session.get_decoded().get('_auth_user_id')
				nuevo_registro = Registro_pedido(id_cliente_id=id_usuario,id_platillo_id=platillof,status='p')
				nuevo_registro.save()
				ya_compro = True
				mensaje = 'Gracias por realizar su pedido, en unos instantes le confirmaremos su pedido'
				ctx = {'ya_compro':ya_compro,'mensaje':mensaje}
				return render_to_response('home/lista_platos.html',ctx,context_instance =RequestContext(request))
		else:	
			formulario = Pedido_registroForm()
			platos = Platillo.objects.filter()
			if len(platos) > 0:
				hay_platos = True
			restau = Restaurante.objects.filter()
			ctx = {'formulario':formulario,'platos':platos,'ya_compro':ya_compro,'restaurantes':restau,'hay_platos':hay_platos}
			return render_to_response('home/lista_platos.html',ctx,context_instance =RequestContext(request))	
	else:
		return render_to_response('home/wine_list.html',context_instance =RequestContext(request))

def nosotros_view(request):
	return render_to_response('home/nosotros.html',context_instance =RequestContext(request))
	

def restaurantes_view(request):
	if request.user.is_authenticated():
		ya_reservo = False
		mensaje = ''
		if request.method == "POST":
			formulario = Reservacion_registroForm(request.POST)
			if formulario.is_valid():
				restaurantef = formulario.cleaned_data['restaurante']
				horaf = formulario.cleaned_data['hora']
				diaf = formulario.cleaned_data['dia']
				session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
				session = Session.objects.get(session_key=session_key)
				id_usuario = session.get_decoded().get('_auth_user_id')		
				obj_restaurante = Restaurante.objects.filter(nombre=restaurantef)
				for obj in obj_restaurante: 
					id_rest = obj.id
				nuevo_registro = Registro_reservacion(id_restaurante_id=id_rest,id_cliente_id=id_usuario,hora=horaf,dia=diaf,status='p')
				nuevo_registro.save()				 
				ya_reservo = True
				mensaje = 'Gracias por hacer su reservacion, le confirmaremos su reserva pronto'			
				ctx = {'ya_reservo':ya_reservo,'mensaje':mensaje}
				return render_to_response('home/reservaciones.html',ctx,context_instance =RequestContext(request))
		else:
			formulario = Reservacion_registroForm()
			restau = Restaurante.objects.filter() 
			ctx = {'formulario':formulario,'restaurantes':restau,'ya_reservo':ya_reservo}
			return render_to_response('home/reservaciones.html',ctx,context_instance =RequestContext(request))
	else:
		return HttpResponseRedirect('/')
	
def registro_view(request):
	
	pass_correcto = False
	registro_nuevo = True
	username_repetido = False
	linkea_a_login = False
	if request.method == 'POST':
		formulario =RegistroForm(request.POST)
		if formulario.is_valid():
			usuariof = formulario.cleaned_data['usuario']
			emailf = formulario.cleaned_data['email']
			nombref = formulario.cleaned_data['nombre']
			apellidof = formulario.cleaned_data['apellidos']
			password_1f = formulario.cleaned_data['password_1']
			password_2f = formulario.cleaned_data['password_2']
			usuarios = User.objects.filter(username=usuariof)
			if len(usuarios) > 0:
				username_repetido = True
				ctx = {'formulario_reg':formulario,'pass_correcto':pass_correcto,'registro_nuevo':registro_nuevo,'username_repetido':username_repetido}
				return render_to_response('home/registro.html',ctx,context_instance =RequestContext(request))				
			if password_1f == password_2f:
				usuario_nuevo = User.objects.create_user(username=usuariof,email=emailf,password=password_1f)
				usuario_nuevo.first_name=nombref
				usuario_nuevo.last_name=apellidof
				usuario_nuevo.save()
				linkea_a_login = True
				#ctx = {'usuario':nombref}
				formulario = LoginForm()
				ctx = {'formulario':formulario,'linkea_a_login':linkea_a_login}
				return render_to_response('home/registro.html',ctx,context_instance =RequestContext(request))
			else:
				registro_nuevo = False
				formulario = RegistroForm()
				ctx = {'formulario_reg':formulario,'pass_correcto':pass_correcto,'registro_nuevo':registro_nuevo,'username_repetido':username_repetido,'linkea_a_login':linkea_a_login}
				return render_to_response('home/registro.html',ctx,context_instance =RequestContext(request))			 
	formulario = RegistroForm()
	ctx = {'formulario_reg':formulario,'reg_nuevo':registro_nuevo,'username_repetido':username_repetido,'linkea_a_login':linkea_a_login}
	return render_to_response('home/registro.html',ctx,context_instance =RequestContext(request))		 


def login_view(request):
	mensaje = ''
	usuariof = ''
	if request.user.is_authenticated():
		#session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
		#session = Session.objects.get(session_key=session_key)
		#usuariof = session.get_decoded().get('_auth_user_id')
		ctx = {'usuario':usuariof}
		return render_to_response('home/opciones_cliente.html',ctx,context_instance =RequestContext(request))
		#return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			formulario = LoginForm(request.POST)
			if formulario.is_valid():
				usuariof = formulario.cleaned_data['usuario']
				passwordf = formulario.cleaned_data['password']
				usuario_auth = authenticate(username=usuariof,password=passwordf)
				if usuario_auth is not None and usuario_auth.is_active:
					login(request,usuario_auth)			
					ctx = {'usuario':usuariof}
					return render_to_response('home/opciones_cliente.html',ctx,context_instance =RequestContext(request))
				else:
					mensaje = 'usuario y/o password incorrecto'
		#else:			
		formulario = LoginForm()
		ctx = {'formulario':formulario,'mensaje':mensaje}
		return render_to_response('home/login.html',ctx,context_instance =RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


def opciones_cliente_view(request):
	usuariof = ''
	if request.user.is_authenticated():	
		ctx = {'usuario':usuariof}
		return render_to_response('home/opciones_cliente.html',ctx,context_instance =RequestContext(request))
	else:
		return HttpResponseRedirect('/')
def menu_view(request):
	if request.user.is_authenticated(): #mostrar la lista de menus para comprar
		ya_compro = False
		hay_platos = False
		mensaje = ''
		if request.method == "POST":
			formulario = Pedido_registroForm(request.POST)
			if formulario.is_valid():
				platillof = formulario.cleaned_data['platillo_id']
				session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
				session = Session.objects.get(session_key=session_key)
				id_usuario = session.get_decoded().get('_auth_user_id')
				nuevo_registro = Registro_pedido(id_cliente_id=id_usuario,id_platillo_id=platillof,status='p')
				nuevo_registro.save()
				ya_compro = True
				mensaje = 'Gracias por realizar su pedido, en unos instantes le confirmaremos su pedido'
				ctx = {'ya_compro':ya_compro,'mensaje':mensaje}
				return render_to_response('home/lista_platos.html',ctx,context_instance =RequestContext(request))
		else:	
			formulario = Pedido_registroForm()
			platos = Platillo.objects.filter()
			if len(platos) > 0:
				hay_platos = True
				print hay_platos
			restau = Restaurante.objects.filter()
			ctx = {'formulario':formulario,'platos':platos,'ya_compro':ya_compro,'restaurantes':restau,'hay_platos':hay_platos}
			return render_to_response('home/lista_platos.html',ctx,context_instance =RequestContext(request))	
	else:
		return render_to_response('home/wine_list.html',context_instance =RequestContext(request))


def reservacion_view(request):
	if request.user.is_authenticated():
		ya_reservo = False
		mensaje = ''
		if request.method == "POST":
			formulario = Reservacion_registroForm(request.POST)
			if formulario.is_valid():
				restaurantef = formulario.cleaned_data['restaurante']
				horaf = formulario.cleaned_data['hora']
				diaf = formulario.cleaned_data['dia']
				session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
				session = Session.objects.get(session_key=session_key)
				id_usuario = session.get_decoded().get('_auth_user_id')		
				obj_restaurante = Restaurante.objects.filter(nombre=restaurantef)
				for obj in obj_restaurante: 
					id_rest = obj.id
				nuevo_registro = Registro_reservacion(id_restaurante_id=id_rest,id_cliente_id=id_usuario,hora=horaf,dia=diaf,status='p')
				nuevo_registro.save()				 
				ya_reservo = True
				mensaje = 'Gracias por hacer su reservacion, le confirmaremos su reserva pronto'			
				ctx = {'ya_reservo':ya_reservo,'mensaje':mensaje}
				return render_to_response('home/reservaciones.html',ctx,context_instance =RequestContext(request))
		else:
			formulario = Reservacion_registroForm()
			restau = Restaurante.objects.filter() 
			ctx = {'formulario':formulario,'restaurantes':restau,'ya_reservo':ya_reservo}
			return render_to_response('home/reservaciones.html',ctx,context_instance =RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def listado_reservaciones_view(request):
	if request.user.is_authenticated():
		tiene_reservas = False
		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
		session = Session.objects.get(session_key=session_key)
		id_usuario = session.get_decoded().get('_auth_user_id')
		reservas = Registro_reservacion.objects.filter(id_cliente_id=id_usuario)
		restaurantes = Restaurante.objects.filter()
		if len(reservas) > 0:
			tiene_reservas = True			
		ctx = {'tiene_reservas':tiene_reservas,'reservas':reservas,'restaurantes':restaurantes}
		return render_to_response('home/reservaciones_cliente.html',ctx,context_instance =RequestContext(request))	
	else:
		return HttpResponseRedirect('/')
	
def listado_platos_view(request):
	if request.user.is_authenticated():
		tiene_pedidos = False
		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
		session = Session.objects.get(session_key=session_key)
		id_usuario = session.get_decoded().get('_auth_user_id')
		pedidos = Registro_pedido.objects.filter(id_cliente_id=id_usuario)
		platillos = Platillo.objects.filter()
		restaurantes = Restaurante.objects.filter()
		if len(pedidos) > 0:
			tiene_pedidos = True			
		ctx = {'tiene_pedidos':tiene_pedidos,'pedidos':pedidos,'restaurantes':restaurantes,'platillos':platillos}
		return render_to_response('home/pedidos_cliente.html',ctx,context_instance =RequestContext(request))	
	else:
		return HttpResponseRedirect('/')
	
'''def login_view(request):
	info_enviado = False
	login_correcto = False
	usuariof = ''
	passwordf = ''
	if request.method == "POST":
		formulario = LoginForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			usuariof = formulario.cleaned_data['usuario']
			passwordf = formulario.cleaned_data['password']
			coincidencia = Cliente.objects.filter(usuario=usuariof,password=passwordf)
			if len(coincidencia) > 0:
				login_correcto = True
				ctx = {'usuario':usuariof}
				return render_to_response('home/opciones_cliente.html',ctx,context_instance =RequestContext(request))
	else:			
		formulario = LoginForm()
		
	ctx = {'formulario':formulario,'login_correcto':login_correcto,'info_enviado':info_enviado,'usuario':usuariof}
	return render_to_response('home/login.html',ctx,context_instance =RequestContext(request))
'''

'''
def registro_view(request):
	info_enviado = False
	usuario_repetido = False
	nombref = ''
	apellidosf = ''
	emailf = ''
	usuariof = ''
	if request.method == "POST":
		formulario = RegistroForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			nombref = formulario.cleaned_data['nombre']
			apellidosf = formulario.cleaned_data['apellidos']
			emailf = formulario.cleaned_data['email']
			usuariof = formulario.cleaned_data['usuario']
			passwordf = formulario.cleaned_data['password']
			usuarios = Cliente.objects.filter(usuario=usuariof)
			if len(usuarios) > 0:
				usuario_repetido = True;
			else:
				nuevo = Cliente(usuario=usuariof,password=passwordf,nombre=nombref,apellidos=apellidosf,email=emailf,status=True)
				nuevo.save()
	else:
		formulario = RegistroForm()
			
	ctx = {'formulario':formulario,'email':emailf,'nombre':nombref,'usuario_repetido':usuario_repetido,'info_enviado':info_enviado,'usuario':usuariof}
	return render_to_response('home/registro.html',ctx,context_instance =RequestContext(request))		 
'''