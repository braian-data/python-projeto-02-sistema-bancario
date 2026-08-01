from cliente import Cliente, PessoaFisica, PessoaJuridica

class Conta:
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

    def adicionar_valor(self, valor: decimal.Decimal):
        if self._status != "ativa":
            raise ValueError("Conta não está ativa.")
        if valor <= 0:
            raise ValueError("Valor a ser adicionado deve ser positivo.")
        self._saldo += valor
    