from django.contrib.auth.models import User
from django import forms
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)
        widgets = {
            'dt_nascimento': forms.DateInput(attrs={'data-mask': "00/00/0000"}),
            'cpf': forms.TextInput(attrs={'data-mask': "000.000.000-00"}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Senha"
    )

    confirmacao_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Confirmação senha"
    )

    def __int__(self, usuario=None, *args, **kwargs):
        super(UserForm, self).__int__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'confirmacao_password', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}
        usuario = cleaned.get('username')
        email = cleaned.get('email')
        password = cleaned.get('password')
        confirmacao_password = cleaned.get('confirmacao_password')

        usuario_db = User.objects.filter(username=usuario).first()
        email_db = User.objects.filter(email=email).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'Senhas diferentes'
        error_msg_password_short = 'Senha muito curta'
        error_msg_required_field = 'Este campo é obrigatório'

        if self.usuario:
            if usuario_db:
                if usuario != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password or confirmacao_password:
                if password != confirmacao_password:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['confirmacao_password'] = error_msg_password_match

                if len(password) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password:
                validation_error_msgs['password'] = error_msg_required_field

            if not confirmacao_password:
                validation_error_msgs['confirmacao_password'] = error_msg_required_field

            if password != confirmacao_password:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['confirmacao_password'] = error_msg_password_match

            if len(password) < 6:
                validation_error_msgs['password'] = error_msg_password_short
                validation_error_msgs['confirmacao_password'] = error_msg_password_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))


