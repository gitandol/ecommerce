from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from base.functions.cpf import valida_cpf
import re


class Perfil(models.Model):
    class Meta:
        db_table = "perfil"
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ["pk"]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dt_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)

    def __str__(self):
        desc = []
        if self.usuario.first_name:
            desc.append(self.usuario.first_name)
        if self.usuario.last_name:
            desc.append(self.usuario.last_name)
        desc = ' '.join(desc)
        return desc or str(self.usuario)

    def clean(self):
        error_messages = {}

        if not valida_cpf.validar(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if error_messages:
            raise ValidationError(error_messages)


class Endereco(models.Model):
    # TODO: https://servicodados.ibge.gov.br/api/docs/localidades alterar para dados IBGE
    CHOICE_ESTADO = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    CHOICE_TIPO = [
        ('C', 'Casa'),
        ('T', 'Trabalho'),
        ('O', 'Outros'),
    ]

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=50)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2, choices=CHOICE_ESTADO)
    tipo = models.CharField(max_length=1, choices=CHOICE_TIPO)
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.logradouro}, {self.numero}'

    def clean(self):
        error_messages = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cpf'] = 'CEP inválido, digite os 8 números do CEP.'

        if error_messages:
            raise ValidationError(error_messages)

    def delete(self, *args, **kwargs):
        enderecos = self.perfil.endereco_set.all().count()

        # atualiza endereço principal caso tenha outro cadastrado
        if self.principal and enderecos > 1:
            primeiro = self.perfil.endereco_set.all().exclude(pk=self.pk).first()
            primeiro.principal = True
            primeiro.save()

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        qtd_principal = self.perfil.endereco_set.filter(principal=True).count()

        if not self.pk:
            if not qtd_principal:
                self.principal = True

            elif qtd_principal and self.principal:
                self.perfil.endereco_set.filter(principal=True).update(principal=False)

        else:
            if qtd_principal == 1 and self.perfil.endereco_set.filter(principal=True).last().pk == self.pk:
                self.principal = True
            elif qtd_principal == 1 and self.principal:
                self.perfil.endereco_set.filter(principal=True).update(principal=False)

        super().save(*args, **kwargs)

        if self.perfil.endereco_set.filter(principal=True).count() == 0:
            primeiro = self.perfil.endereco_set.all().first()
            primeiro.principal = True
            primeiro.save()



