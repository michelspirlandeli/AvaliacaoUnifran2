# This Python file uses the following encoding: utf-8
# ANOTAÇÃO PARA USAR CARACTERES ESPECIAIS AQUI. (MESMO PARA ANOTAÇÕES.)
"""
https://www.facebook.com/groups/pythonmania/
"""

from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from django.db.models import Q #Queries complexas
from caixas.models import Conta
from pessoas.models import Pessoa


def caixaListar(request):
    contas = Conta.objects.all()[0:10]

    return render(request, 'caixas/listaCaixas.html', {'contas': contas})


def caixaAdicionar(request):
    pessoas = Pessoa.objects.all().order_by('nome')

    return render(request, 'caixas/formCaixas.html', {'pessoas': pessoas})

def caixaSalvar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '0')

        try:
            conta = Conta.objects.get(pk=codigo)
        except:
            conta = Conta()

        conta.pessoa_id = request.POST.get('pessoa_id', '1')
        conta.tipo = request.POST.get('tipo', '').upper()
        conta.descricao = request.POST.get('descricao', 'CONTA SEM DESCRIÇÃO').upper()
        conta.valor = request.POST.get('valor', '0.00').replace(',','.')
        conta.data = datetime.strptime(request.POST.get('data', ''), '%d/%m/%Y %H:%M:%S')

        conta.save()
    return HttpResponseRedirect('/caixas/')

def caixaPesquisar(request):
    if request.method == 'POST':
        textoBusca = request.POST.get('textoBusca', 'TUDO').upper()

        try:
            if textoBusca == 'TUDO':
                contas = Conta.objects.all()
            else:
                sql = ("select cc.* from caixas_conta cc inner join pessoas_pessoa pp on pp.id = cc.pessoa_id where pp.nome like '%s' or cc.descricao like '%s' order by data") % ('%%'+textoBusca+'%%', '%%'+textoBusca+'%%')
                contas = Conta.objects.raw(sql)
        except:
            contas = []

        return render(request, 'caixas/listaCaixas.html', {'contas': contas, 'textoBusca': textoBusca})

def caixaEditar(request, pk=0):
    try:
        conta = Conta.objects.get(pk=pk)
        pessoas = Pessoa.objects.all().order_by('nome')
    except:
        return HttpResponseRedirect('/caixas/')

    return render(request, 'caixas/formCaixas.html', {'conta': conta, 'pessoas':pessoas})

def caixaExcluir(request, pk=0):
    try:
        conta = Conta.objects.get(pk=pk)
        conta.delete()
        return HttpResponseRedirect('/caixas/')
    except:
        return HttpResponseRedirect('/caixas/')

def caixaFluxo(request):
    if request.method == 'POST':

        data_inicial = datetime.strptime(request.POST.get('data_inicial', ''), '%d/%m/%Y %H:%M:%S') #1º DATA
        data_final   = datetime.strptime(request.POST.get('data_final',   ''), '%d/%m/%Y %H:%M:%S') #2º DATA
        total = 0 

        try:
            contas = Conta.objects.filter(data__range=(data_inicial, data_final)) #buscando as contas dentro do periodo
            for conta in contas: # percorrer todas as contas que achar, se for E de entrada será somado, se for S de saída será subtraído
                if conta.tipo == 'E':
                    total += conta.valor
                elif conta.tipo == 'S':
                    total -= conta.valor
                    
        except: # se acontecer alguma excessão vai retornar nenhuma conta
            contas = []

        return render(request, 'caixas/formFluxoCaixa.html', {'contas' : contas, 'total': total ,'data_inicial': data_inicial, 'data_final': data_final})

    return render(request, 'caixas/formFluxoCaixa.html', {'contas' : []})




    




