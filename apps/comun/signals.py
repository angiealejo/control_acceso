from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.templatetags.staticfiles import static

from rest_framework.authtoken.models import Token


def login_signal(sender, user, request, **kwargs):
    token = Token.objects.get_or_create(user=user)
    request.session['token'] = token[0].key
    if finders.find('logo/logo.png'):
        request.session['logo_existe'] = True


def logout_signal(sender, user, request, **kwargs):
    request.session['token'] = None
    request.session['logo_existe'] = False


user_logged_in.connect(login_signal)
user_logged_out.disconnect(logout_signal)
