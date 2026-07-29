from cliente import Cliente, PessoaFisica, PessoaJuridica,

class PerfilAcesso:
    def __init__(self, login, senha) -> None:
        self.autenticar_senha()
        self._login = login
        self._senha = senha

    def autenticar_senha(self, senha):
        if not isinstance(senha, str):
            return False
        return True
    