from validacoes.validacoes import validar_email, estrurar_data, estruturar_telefone
from abc import ABC, abstractmethod

class Cliente(ABC):
    def __init__(self, nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal):
        validar_email(email)
        self._nome = nome
        self._email = email
        self._endereco = endereco
        self._telefone = estruturar_telefone(telefone)
        self._data_nascimento = estrurar_data(data_nascimento)
        self._data_criacao = estrurar_data(data_criacao)
        self._limite_diario = 5
        self._renda_mensal = renda_mensal

    @property
    def limite_restante(self):
        return self._limite_diario


    @property
    @abstractmethod
    def pode_sacar(self):
        if self._limite_diario > 0:
            return True
        return False
