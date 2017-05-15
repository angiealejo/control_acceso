import os

from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader

from apps.empleado.models import DatosUsuarioEmpleado
from apps.punto_control.models import PuntoControl
from control_accesos_v2_server import settings


def generarnumeroempleado():
    numeroempleado = 0
    datos = DatosUsuarioEmpleado.objects.all().order_by('numero_empleado')
    for dato in datos:
        if dato.numero_empleado is None:
            continue
        elif numeroempleado == int(dato.numero_empleado):
            numeroempleado += 1
        elif numeroempleado != int(dato.numero_empleado):
            break
    return convertirnumeroempleadoentero(numeroempleado)


def convertirnumeroempleadoentero(numero):
    numeroempleado = '0000'
    if numero < 10:
        numeroempleado = '000' + str(numero)
    elif numero < 100:
        numeroempleado = '00' + str(numero)
    elif numero < 1000:
        numeroempleado = '0' + str(numero)
    elif numero >= 1000:
        numeroempleado = str(numero)
    return numeroempleado


def traergrupos(idgrupo):
    grupoempleado = Group.objects.get(name='empleado')
    grupos = (grupoempleado,)
    if idgrupo is not None and idgrupo != 0:
        try:
            grupo = Group.objects.get(id=idgrupo)
            if grupo.name is not 'pcin' or grupo.name is not 'empleado' and\
                    (grupo.name is 'administrador' or grupo.name is 'configurador' or grupo.name is 'recursos_humanos'):
                grupos = (grupoempleado, grupo)
        except Exception:
            grupos = (grupoempleado,)
    return grupos


def borrarfotoempleadovieja(numero_empleado_usuario):
    ruta = 'usuarios/'+numero_empleado_usuario+'.png'
    borrararchivo(ruta)
    ruta = 'usuarios/'+numero_empleado_usuario+'.jpg'
    borrararchivo(ruta)
    ruta = 'usuarios/'+numero_empleado_usuario+'.jpeg'
    borrararchivo(ruta)
    ruta = 'usuarios/' + numero_empleado_usuario + '.PNG'
    borrararchivo(ruta)
    ruta = 'usuarios/' + numero_empleado_usuario + '.JPG'
    borrararchivo(ruta)
    ruta = 'usuarios/' + numero_empleado_usuario + '.JPEG'
    borrararchivo(ruta)


def borrararchivo(ruta):
    file_path = settings.BASE_DIR + '/media/' + ruta
    if os.path.isfile(file_path):
        os.remove(file_path)


def traerpuntoscontrol(idspc):
    puntoscontrol = []
    if idspc is not None:
        for idpc in idspc:
            try:
                puntocontrol = PuntoControl.objects.get(id=idpc)
                puntoscontrol.append(puntocontrol)
            except Exception:
                puntoscontrol = puntoscontrol
    return puntoscontrol


def enviar_email_template(subject, email_template_name, email_context, recipients,
                          sender=None):
    contexto = Context(email_context)
    body = loader.render_to_string(email_template_name, contexto)
    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL
    if type(recipients) == str:
        if recipients.find(','):
            recipients = recipients.split(',')
    elif type(recipients) != list:
        recipients = [recipients, ]
    msg = EmailMultiAlternatives(subject, body, sender, recipients)
    html_email = loader.render_to_string(email_template_name, contexto)
    msg.attach_alternative(html_email, 'text/html')
    try:
        msg.send()
    except Exception, e:
        return False
