from conta import Conta, ContaCorrente, ContaPoupanca
from abc import ABC, abstractmethod

class Transacao(ABC):
    def __init__(self, conta_1: Conta, conta_2: Conta, valor: decimal.Decimal, tipo: str):
        self._origem = conta_1
        self._destino = conta_2
        self._tipo = tipo
        self._valor = valor

    @abstractmethod
    def processar(self, senha: str) -> decimal.Decimal:
        pass

    @abstractmethod
    def horario_limite(self) -> bool:
        pass

class TransacaoOnline(Transacao):
    def __init__(self, conta_1: Conta, conta_2: Conta, valor: decimal.Decimal, tipo: str, senha: str):
        super().__init__(conta_1, conta_2, valor, tipo)
        self._senha = senha

    def processar(self, senha: str) -> decimal.Decimal:
        if self._tipo == "saque":
            self._origem.sacar(self._destino)
        elif self._tipo == "deposito":
            self._origem.adicionar_valor(self._destino)
        elif self._tipo == "transferencia":
            if not isinstance(self._destino, Conta):
                raise ValueError("Conta de destino inválida para transferência.")
            if not isinstance(self._origem, Conta):
                raise ValueError("Conta de origem inválida para transferência.") 
            
            if self._destino.status != "ativa" or self._origem.status != "ativa":
                raise ValueError("Uma das contas não está ativa.")   
            
            if isinstance(self._origem, ContaCorrente) or isinstance(self._origem, ContaPoupanca) and self._origem.saldo >= self._valor and self._origem._senha == senha:
                self._origem.sacar(self._destino)
                self._destino.adicionar_valor(self._valor)
            else:
                raise ValueError("Conta de origem inválida para transferência ou senha incorreta.")
        else:
            raise ValueError("Tipo de transação inválido.")

    def horario_limite(self) -> bool:
        from datetime import datetime
        now = datetime.now()
        if now.hour < 6 or now.hour > 22:
            raise ValueError("Transações online só podem ser realizadas entre 06:00 e 22:00.")
        return True