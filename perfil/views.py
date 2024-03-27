from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import models, forms
import copy


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderizar = None
        self.contexto = None
        self.perfil = None
        self.perfilform = None
        self.userform = None
        self.carrinho = {}

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        usr = self.request.user if self.request.user.is_authenticated else None
        self.perfil = models.Perfil.objects.filter(usuario=usr).first() if usr else None
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None,
                instance=self.request.user if usr else None,
            ),
            'perfilform': forms.PerfilForm(
                data=self.request.POST or None,
                instance=self.perfil
            ),
        }
        self.contexto["userform"].usuario = usr

        self.userform = self.contexto["userform"]
        self.perfilform = self.contexto["perfilform"]
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        data = self.userform.cleaned_data
        perfildata = self.perfilform.cleaned_data

        #  Usuario logado - atualizar
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = data.get('username')
            usuario.email = data.get('email')
            usuario.first_name = data.get('first_name')
            usuario.last_name = data.get('last_name')

            if data.get('password'):
                usuario.set_password(data.get('password'))
            usuario.save()

            if not self.perfil:  # caso o usuário não tenha perfil por algum motivo, será criado abaixo
                perfildata['usuario'] = usuario
                perfil = models.Perfil(**perfildata)
                perfil.save()
            else:  # atualiza perfil existente
                print(self.perfilform.cleaned_data)
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        #  Usuario não logado - criar
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(data.get('password'))
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if data.get('password'):
            if authenticate(self.request, username=data.get('username'), password=data.get('password')):
                login(self.request, user=usuario)

        self.request.session["carrinho"] = self.carrinho
        self.request.session.save()

        return self.renderizar


class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')

