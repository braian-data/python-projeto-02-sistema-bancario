from conta import Conta
from abc import ABC, abstractmethod
import decimal
from datetime import datetime

class Transacao(ABC):
    def __init__(self, origem: Conta, destino: Conta, valor: decimal.Decimal):
        self._origem = origem
        self._destino = destino
        self._valor = valor

    @abstractmethod
    def processar(self, senha: str):
        pass

    def horario_limite(self) -> bool:
        now = datetime.now()
        if now.hour < 6 or now.hour > 22:
            raise ValueError("Transações online só podem ser realizadas entre 06:00 e 22:00.")
        return True

class Saque(Transacao):
    def processar(self, senha: str):
        # A lógica específica do saque
        self._origem.sacar(self._valor)

class Deposito(Transacao):
    def processar(self, senha: str):
        # A lógica específica do depósito
        self._destino.adicionar_valor(self._valor)

class Transferencia(Transacao):
    def processar(self, senha: str):
        if self._origem.status != "ativa" or self._destino.status != "ativa":
            raise ValueError("Uma das contas não está ativa.")   
        
        # O saque já subtrai o limite diário e valida o saldo internamente
        self._origem.sacar(self._valor)
        self._destino.adicionar_valor(self._valor)