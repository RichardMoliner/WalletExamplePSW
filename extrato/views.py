from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, FileResponse
from datetime import datetime, timedelta
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO

# Create your views here.
def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categoria = Categoria.objects.all()
        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categoria})
    elif request.method == "POST":
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')
        
        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        conta = Conta.objects.get(id=conta)

        if tipo == 'E':
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)

        conta.save()

        tipo_movimentacao = ''
        if tipo == 'E':
            tipo_movimentacao = 'Entrada'
        else:
            tipo_movimentacao = 'Saída'

        messages.add_message(request, constants.SUCCESS, f'{tipo_movimentacao} cadastrada com sucesso')
        return redirect('/extrato/novo_valor')
    
def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.all()
    reset_get = request.GET.get('resetar')
    start_date_get = request.GET.get('start_date')
    end_date_get = request.GET.get('end_date')
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

  
    
    if conta_get and categoria_get:
        valores = valores.filter(conta__id=conta_get, categoria__id=categoria_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)
    if start_date_get and end_date_get:
        valores = Valores.objects.filter(data__gte=start_date_get, data__lte=end_date_get)
    if reset_get:
        return redirect(view_extrato)
   
    return render(request, 'view_extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias, 'start_date_get': start_date_get, 'end_date_get': end_date_get})


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    path_output = BytesIO()

    template_render = render_to_string(path_template, {'valores': valores, 'contas': contas, 'categorias': categorias})
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    return FileResponse(path_output, filename="extrato.pdf")