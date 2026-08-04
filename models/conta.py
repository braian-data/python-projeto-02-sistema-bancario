from cliente import Cliente
from abc import ABC, abstractmethod
import decimal

class Conta(ABC):
    def __init__(self, cliente: Cliente, _saldo: decimal.Decimal = decimal.Decimal('0.0'), _status: str = "ativa"):
        self._cliente = cliente
        self._saldo = _saldo
        self._status = _status

    def __eq__(self, other):
        if not isinstance(other, Conta):
            return False
        return self._cliente == other._cliente and self._saldo == other._saldo and self._status == other._status

    def __repr__(self):
        return f"Conta(cliente={self._cliente}, saldo={self._saldo}, status={self._status})"

    __str__ = __repr__

    @abstractmethod
    def adicionar_valor(self, valor: decimal.Decimal) -> decimal.Decimal:
        pass

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def status(self):
        return self._status


class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, _saldo: decimal.Decimal = decimal.Decimal('0.0'), _status: str = "ativa"):
        super().__init__(cliente, _saldo, _status)
        self._tx = decimal.Decimal('0.01')  

    @property
    def tx(self):
        return self._tx

    def adicionar_valor(self, valor: decimal.Decimal) -> decimal.Decimal:
        if self._status != "ativa":
            raise ValueError("Conta não está ativa.")
        if valor <= 0:
            raise ValueError("Valor a ser adicionado deve ser positivo.")
        self._saldo += valor
        return self._saldo

    def sacar(self, valor: decimal.Decimal):
        if self._status != "ativa":
            raise ValueError("Conta não está ativa.")
        if valor <= 0:
            raise ValueError("Valor a ser sacado deve ser positivo.")
        if not self._cliente.pode_sacar(valor):
            raise ValueError("Limite diário excedido.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente.")
        self._saldo -= valor
        self._cliente._limite_diario -= valor


class ContaPoupanca(Conta):
    def __init__(self, cliente: Cliente, _saldo: decimal.Decimal = decimal.Decimal('0.0'), _status: str = "ativa"):
        super().__init__(cliente, _saldo, _status)
        self.__principal = decimal.Decimal('0.0')

    def adicionar_valor(self, valor: decimal.Decimal) -> decimal.Decimal:
        if self._status != "ativa":
            raise ValueError("Conta não está ativa.")
        if valor <= 0:
            raise ValueError("Valor a ser adicionado deve ser positivo.")
        self._saldo += valor
        return self._saldo

    def sacar(self, valor: decimal.Decimal):
        if self._status != "ativa":
            raise ValueError("Conta não está ativa.")
        if valor <= 0:
            raise ValueError("Valor a ser sacado deve ser positivo.")
        if not self._cliente.pode_sacar(valor):
            raise ValueError("Limite diário excedido.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente.")
        self._saldo -= valor
        self._cliente._limite_diario -= valor