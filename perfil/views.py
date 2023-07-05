from django.shortcuts import render, redirect
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcular_saldo

# Create your views here.

def home(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()

  total_conta = calcular_saldo(contas, 'valor')

  return render(request, 'home.html',
                {'contas': contas,
                 'categoria': categorias,
                 'total_conta': total_conta})

def gerenciar(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()

  total_conta = calcular_saldo(contas, 'valor')

  return render(request, 'gerenciar.html',
                {'contas': contas,
                 'total_conta': total_conta,
                 'categorias': categorias})

def cadastrar_banco(request):
  apelido = request.POST.get('apelido')
  banco = request.POST.get('banco')
  tipo = request.POST.get('tipo')
  valor = request.POST.get('valor')
  icone = request.FILES.get('icone')

  if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
    messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
    return redirect('/perfil/gerenciar/')


  conta = Conta(
    apelido=apelido,
    banco=banco,
    tipo=tipo,
    valor=valor,
    icone=icone
  )

  conta.save()

  messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
  return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):

  nome = request.POST.get('categoria')
  essencial = bool(request.POST.get('essencial'))
  
  categoria = Categoria(
    categoria=nome,
    essencial=essencial
  )

  categoria.save()

  messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso!')

  return redirect('/perfil/gerenciar/')

def deletar_categoria(request, id):
  categoria = Categoria.objects.get(id=id)
  categoria.delete()

  messages.add_message(request, constants.SUCCESS, 'Categoria removida com sucesso')
  return redirect('/perfil/gerenciar/')

def alterar_categoria(request, id):
  categoria = Categoria.objects.get(id=id)
  categoria.essencial = not categoria.essencial
  categoria.save()

  messages.add_message(request, constants.SUCCESS, 'Categoria alterada com sucesso')
  return redirect('/perfil/gerenciar/')

  