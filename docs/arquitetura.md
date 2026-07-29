---
config:
  theme: mc
---
classDiagram

class Cliente {
    <<abstract>>
    #_nome: String
    #_email: String
    #_endereco: String
    #_telefone: String
    #_data_nascimento: String
    #_data_criacao: String
    #_limite_diario: decimal
    #_qtd_saques_realizados: int
    #_tipo_cliente: String
    #_renda_mensal: decimal

    +get_limite_restante()* : decimal
    +pode_sacar(valor: decimal)* : bool
}

class PessoaFisica {
    #_cpf: String
    +get_limite_restante(): decimal
    +pode_sacar(valor: decimal): bool
}

class PessoaJuridica {
    #_cnpj: String
    #_razao_social: String
    +get_limite_restante(): decimal
    +pode_sacar(valor: decimal): bool
}

class PerfilAcesso {
    #_login: String
    #_senha: String
    +autenticar(senha: String): bool
}

class Cartao {
    #_numero: String
    #_vcc: int
    #_validade: String
    #_senha: String
    +validar_uso(senha: String): bool
}

class Conta {
    <<abstract>>
    #_saldo: decimal
    #_status: String
    
    +adicionar_valor(valor: decimal)*: decimal
}

class ContaCorrente {
    #_tx: decimal
    +get_saldo(): decimal
    +get_status(): String
    +adicionar_valor(valor: decimal): decimal
}

class ContaPoupanca {
    #_principal: decimal
    +adicionar_valor(valor: decimal): decimal
}

class Banco {
    #_nome: String
    #_unidade: String
    #_endereco: String
    #_passivo: decimal
    #_ativo: decimal
}

class Transacao {
    <<abstract>>
    #_origem: String
    #_destino: String
    #_valor: decimal
    +horario_limite()*: bool
    +processar()*: decimal
}

class TransacaoOnline {
    +processar(): decimal
    +horario_limite(): bool
}

class TransacaoCaixaEletronico {
    +processar(): decimal
    +horario_limite(): bool
}

%% Heranças
Cliente <|-- PessoaFisica
Cliente <|-- PessoaJuridica
Transacao <|-- TransacaoOnline
Transacao <|-- TransacaoCaixaEletronico
Conta <|-- ContaPoupanca
Conta <|-- ContaCorrente

%% Composições e Agregações
Cliente "1" *-- "1" PerfilAcesso : possui
Cliente "1" o-- "1..*" Conta : titular
Conta "1" *-- "0..*" Cartao : emite
Banco "1" o-- "*" Conta : gerencia
Conta "1" o-- "*" Transacao : registra