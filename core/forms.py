# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput


class CambiarPasswdForm(forms.Form):

    passwd_actual = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput)
    nuevo_passwd = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    conf_nuevo_passwd = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CambiarPasswdForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_conf_nuevo_passwd(self):
        nuevo_passwd = self.cleaned_data.get('nuevo_passwd')
        conf_nuevo_passwd = self.cleaned_data.get('conf_nuevo_passwd')
        if nuevo_passwd and conf_nuevo_passwd and nuevo_passwd != conf_nuevo_passwd:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return conf_nuevo_passwd
