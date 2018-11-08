# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django.shortcuts import (
    render_to_response, HttpResponse, HttpResponseRedirect)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from datetime import datetime
from django.urls import reverse, resolve
from django.contrib import auth
from .forms import CambiarPasswdForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.six.moves.urllib.parse import urlparse
from django.conf import settings

from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'core/index.html')


# Vista de login
def login(request):
    if request.method == 'POST':
        try:
            referer = request.META['HTTP_REFERER']
            # url para el redirecionamiento después de loguearse desde una
            # página que no requiere loguearse
            query = urlparse(referer)[4]
            if query:
                url = query.partition('=')[2]
            else:
                url = urlparse(referer)[2]
        except KeyError:
            url = settings.LOGIN_URL

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
        else:
            messages.error(request, 'Credenciales incorrectas, por favor intente nuevamente.')

        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(settings.LOGIN_URL)


@login_required(login_url="core:login")
def logout(request):
    auth.logout(request)
    next = request.GET['next']
    return HttpResponseRedirect(next)


# Yusdanis Feus Pérez
@login_required(login_url="core:login")
def cambiar_passwd(request):

    if request.POST:
        form = CambiarPasswdForm(request.POST)
        if form.is_valid():
            usuario = User.objects.get(username=request.user.username)
            pass_actual = form.cleaned_data['passwd_actual']
            pass_nuevo = form.cleaned_data['nuevo_passwd']

            if check_password(pass_actual, usuario.password):
                if check_password(pass_nuevo, usuario.password):
                    form.add_error(None, "La nueva contraseña es igual a la actual.")
                    return render_to_response("cambiar_passwd.html", {'form': form}, context_instance=RequestContext(request))
                else:
                    usuario.set_password(pass_nuevo)
                    usuario.save()
                    update_session_auth_hash(request, usuario)
                    messages.add_message(request, messages.INFO, 'Contraseña actualizada satisfacotiamente.')
            else:
                form.add_error(None, "Contraseña actual incorrecta, intente nuevamente.")
                return render_to_response("cambiar_passwd.html", {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response("cambiar_passwd.html", {'form': form}, context_instance=RequestContext(request))

    form = CambiarPasswdForm()

    return render_to_response("cambiar_passwd.html", {'form': form}, context_instance=RequestContext(request))


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')
