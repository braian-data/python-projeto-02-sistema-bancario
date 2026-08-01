from validacoes.validacoes import validar_email, estruturar_data, estruturar_telefone
from abc import ABC, abstractmethod
import decimal

class Cliente(ABC):
    def __init__(self, nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal):
        validar_email(email)
        self._nome = nome
        self._email = email
        self._endereco = endereco
        self._telefone = estruturar_telefone(telefone)
        self._data_nascimento = estruturar_data(data_nascimento)
        self._data_criacao = estruturar_data(data_criacao)
        self._limite_diario = decimal.Decimal('5.00')
        self._qtd_saques_realizados = int(0)
        self._renda_mensal = decimal.Decimal(renda_mensal)

    def get_limite_restante(self) -> decimal.Decimal:
        return self._limite_diario

    @abstractmethod
    def pode_sacar(self, valor: decimal.Decimal) -> bool:
        pass

    def __eq__(self, other):
        if not isinstance(other, Cliente):
            return False
        return self._email == other._email

    def __repr__(self):
        return f"Cliente(nome={self._nome}, email={self._email}, endereco={self._endereco}, telefone={self._telefone}, data_nascimento={self._data_nascimento}, data_criacao={self._data_criacao}, limite_diario={self._limite_diario}, renda_mensal={self._renda_mensal})"

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal):
        super().__init__(nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal)
        self._cpf = cpf

    def pode_sacar(self, valor: decimal.Decimal) -> bool:
        return valor <= self.get_limite_restante()

class PessoaJuridica(Cliente):
    def __init__(self, razao_social, cnpj: str, nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal):
        super().__init__(nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal)
        self._cnpj = cnpj
        self._razao_social = razao_social

    def pode_sacar(self, valor: decimal.Decimal) -> bool:
        return valor <= self.get_limite_restante()