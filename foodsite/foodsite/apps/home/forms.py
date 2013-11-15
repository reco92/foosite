from django import forms

class RegistroForm(forms.Form):
	usuario = forms.CharField(label='Usuario',widget=forms.TextInput())
	email =  forms.EmailField(label='Correo electronico',widget=forms.TextInput()) 
	nombre = forms.CharField(widget=forms.TextInput())
	apellidos = forms.CharField(widget=forms.TextInput())	
	password_1 = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
	password_2 = forms.CharField(label='Confirmar password',widget=forms.PasswordInput(render_value=False))

#class LoginForm(forms.Form):
#	usuario = forms.CharField(widget=forms.TextInput())
#	password = forms.CharField(max_length=32, widget=forms.PasswordInput()) 
	
class LoginForm(forms.Form):
	usuario = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(render_value=False))
	
class Reservacion_registroForm(forms.Form):
	restaurante = forms.CharField(widget=forms.TextInput())
	hora = forms.CharField(max_length=20)
	dia = forms.CharField(max_length=20)
	
class Pedido_registroForm(forms.Form):
	platillo_id = forms.CharField(label='Numero plato',widget=forms.TextInput())
		
	"""
	cliente
	nombre = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	email = models.EmailField(max_length=75)
	status = models.BooleanField(default=True)
	
	restaurante
	usuario = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	nombre = models.CharField(max_length=200)
	email = models.EmailField(max_length=75)
	telefono = models.CharField(max_length=20)
	descripcion = models.CharField(max_length=350)
	reservaciones = models.IntegerField()
	
	registro reservacion mesa	
	id_restaurante = models.ForeignKey(Restaurante)
	id_cliente = models.ForeignKey(Cliente)
	#id_cliente = models.ForeignKey(User)
	hora = models.CharField(max_length=20)
	dia = models.CharField(max_length=20)
	status = models.CharField(max_length=2) # p en proceso, n esta negado, a aceptado
	"""
	
	