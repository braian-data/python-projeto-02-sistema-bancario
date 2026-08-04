from models.cliente import Cliente, PessoaFisica, PessoaJuridica

class PerfilAcesso:
    def __init__(self, login, senha, cliente: Cliente) -> None:
        self.autenticar_senha()
        self._login = login
        self._senha = senha
        self._cliente = cliente

    def autenticar_senha(self, senha):
        if not isinstance(senha, str):
            return False
        return True
    