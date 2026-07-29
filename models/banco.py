from decimal import Decimal

class Banco:
    def __init__(self, nome: str, unidade: str, endereco: str, passivo = "0.0", ativo = "0.0"):
        self._nome = nome
        self._unidade = unidade
        self._endereco = endereco
        self._passivo = Decimal(str(passivo))
        self._ativo = Decimal(str(ativo))
        self._contas = [] 

    def __eq__(self, other):
        if not isinstance(other, Banco):
            return False
        return self._nome == other._nome and self._unidade == other._unidade

    def __repr__(self):
        return f"Banco(nome={self._nome}, unidade={self._unidade}, ativo={self._ativo})"