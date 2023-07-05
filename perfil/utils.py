from .models import Conta

def calcular_saldo(conta, valor):
    contas = Conta.objects.all()
    saldo_atual = 0

    for conta in contas:
        saldo_atual += conta.valor
    return saldo_atual
