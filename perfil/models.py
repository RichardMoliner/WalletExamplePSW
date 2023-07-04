from django.db import models

class Categoria(models.Model):
    categoria = models.CharField(max_length=50, null=False)
    essencial = models.BooleanField(default=False)
    valor = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

class Conta(models.Model):

    banco_choices = (
        ('NU', 'Nubank'),
        ('CX', 'Caixa Economica'),
        ('BR', 'Bradesco'),
        ('ST', 'Santander')
    )

    tipo_choices = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")
    
    def __str__(self):
        return self.apelido