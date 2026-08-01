from models.conta import Conta


class Cartao:
    def __init__(self, numero, conta: Conta, validade, vcc, senha):
        self._numero = numero
        self._conta = conta
        self._validade = validade
        self._vcc = vcc
        self._senha = senha

    def validar_uso(self, senha: str):
        if self._conta._status != "ativa":
            raise ValueError("Conta não está ativa.")
        if self._conta._saldo <= 0:
            raise ValueError("Saldo insuficiente na conta.")
        if self._senha != senha:
            raise ValueError("Senha incorreta.")

    def __str__(self):
        return f"Cartão {self._numero} - Titular: {self._conta._cliente}"   