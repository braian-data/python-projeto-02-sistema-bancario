class Banco:
    def __init__(self, nome, unidade, endereco, passivo = 0, ativo = 0):
        self._nome = nome
        self._unidade = unidade
        self._endereco = endereco
        self._passivo = passivo
        self._ativo = ativo

