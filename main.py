import sys
import decimal
from datetime import date

from models.banco import Banco
from models.cliente import PessoaFisica, PessoaJuridica
from models.conta import ContaCorrente, ContaPoupanca
from models.cartao import Cartao
from services.transacao import Saque, Deposito, Transferencia

def exibir_menu():
    print("\n" + "="*30)
    print("=== TERMINAL DE OPERAÇÕES ===")
    print("="*30)
    print("1. Cadastrar Novo Cliente")
    print("2. Alocar Conta Bancária")
    print("3. Emitir Cartão de Crédito")
    print("4. Executar Transação (Depósito/Saque/Transferência)")
    print("5. Consultar Banco de Dados (Exibir Múltiplos Usuários)")
    print("6. Encerrar Sistema")
    return input("Selecione a instrução [1-6]: ").strip()

def buscar_cliente(clientes_db: list, email: str):
    for cliente in clientes_db:
        if cliente._email == email:
            return cliente
    return None

def buscar_conta(contas_db: list, email_cliente: str):
    # Busca a primeira conta vinculada ao email fornecido
    for conta in contas_db:
        if conta._cliente._email == email_cliente:
            return conta
    return None

def main():
    banco = Banco("Erutufin", "123456789", "Av. Faria Lima, 3000")
    
    # Repositórios Voláteis (Substituem o SQL nesta etapa de arquitetura)
    clientes_db = []
    
    while True:
        try:
            opcao = exibir_menu()
            
            if opcao == "1":
                print("\n-- REGISTRO DE CLIENTE --")
                tipo_cliente = input("Tipo Jurídico (PF para Física / PJ para Jurídica): ").strip().upper()
                
                nome = input("Nome/Razão Social: ").strip()
                email = input("Email (Chave Única): ").strip()
                
                if buscar_cliente(clientes_db, email):
                    raise ValueError("Este email já está registrado em outro cliente.")
                
                endereco = input("Endereço: ").strip()
                telefone = input("Telefone (Apenas números): ").strip()
                data_nascimento = input("Data de Nascimento/Fundação (DD/MM/YYYY): ").strip()
                data_criacao = date.today().strftime("%d/%m/%Y")
                renda_mensal = input("Renda/Faturamento Mensal Bruto: ").strip()
                
                if tipo_cliente == "PF":
                    cpf = input("CPF (Apenas números): ").strip()
                    cliente = PessoaFisica(cpf, nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal)
                elif tipo_cliente == "PJ":
                    cnpj = input("CNPJ (Apenas números): ").strip()
                    cliente = PessoaJuridica(nome, cnpj, nome, email, endereco, telefone, data_nascimento, data_criacao, renda_mensal)
                else:
                    raise ValueError("Tipo jurídico não reconhecido pelo sistema.")
                
                clientes_db.append(cliente)
                print(f"\n[SUCESSO] Cliente {nome} instanciado no endereço de memória com sucesso.")

            elif opcao == "2":
                print("\n-- ALOCAÇÃO DE CONTA --")
                email_cliente = input("Email do titular cadastrado: ").strip()
                cliente = buscar_cliente(clientes_db, email_cliente)
                
                if not cliente:
                    raise ValueError("Cliente não localizado na base de dados em memória.")
                
                tipo_conta = input("Modalidade da Conta (CC para Corrente / CP para Poupança): ").strip().upper()
                if tipo_conta == "CC":
                    conta = ContaCorrente(cliente)
                elif tipo_conta == "CP":
                    conta = ContaPoupanca(cliente)
                else:
                    raise ValueError("Modalidade de conta inválida.")
                
                banco._contas.append(conta)
                print(f"\n[SUCESSO] Conta {tipo_conta} alocada para {cliente._nome}.")

            elif opcao == "3":
                print("\n-- EMISSÃO DE CARTÃO --")
                email_cliente = input("Email do titular cadastrado: ").strip()
                conta = buscar_conta(banco._contas, email_cliente)
                
                if not conta:
                    raise ValueError("Nenhuma conta vinculada a este email foi localizada.")
                
                numero_cartao = input("Número do Cartão: ").strip()
                validade = input("Validade (MM/AA): ").strip()
                vcc = input("VCC: ").strip()
                senha = input("Defina a Senha Transacional: ").strip()
                
                cartao = Cartao(numero_cartao, conta, validade, vcc, senha)
                print(f"\n[SUCESSO] Cartão final {numero_cartao[-4:]} emitido e vinculado à conta.")

            elif opcao == "4":
                print("\n-- MOTOR TRANSACIONAL --")
                tipo_transacao = input("Operação (DEP = Depósito / SAQ = Saque / TRA = Transferência): ").strip().upper()
                
                email_origem = input("Email da conta de origem: ").strip()
                conta_origem = buscar_conta(banco._contas, email_origem)
                
                if not conta_origem:
                    raise ValueError("Conta de origem não localizada.")
                
                valor_str = input("Montante (Ex: 150.50): ").strip()
                valor_decimal = decimal.Decimal(valor_str)
                
                if tipo_transacao == "DEP":
                    transacao = Deposito(origem=conta_origem, destino=conta_origem, valor=valor_decimal)
                    transacao.processar(senha="") # Depósito não exige senha na sua modelagem
                    print(f"\n[SUCESSO] Depósito processado. Saldo Atual: R${conta_origem.saldo}")
                    
                elif tipo_transacao == "SAQ":
                    senha = input("Senha de autorização: ").strip()
                    transacao = Saque(origem=conta_origem, destino=conta_origem, valor=valor_decimal)
                    transacao.processar(senha)
                    print(f"\n[SUCESSO] Saque processado. Saldo Atual: R${conta_origem.saldo}")
                    
                elif tipo_transacao == "TRA":
                    email_destino = input("Email da conta de destino: ").strip()
                    conta_destino = buscar_conta(banco._contas, email_destino)
                    
                    if not conta_destino:
                        raise ValueError("Conta de destino não localizada no sistema.")
                        
                    senha = input("Senha de autorização da conta de origem: ").strip()
                    transacao = Transferencia(origem=conta_origem, destino=conta_destino, valor=valor_decimal)
                    transacao.processar(senha)
                    print(f"\n[SUCESSO] Transferência de R${valor_decimal} enviada para {conta_destino._cliente._nome}.")
                    print(f"Saldo restante na origem: R${conta_origem.saldo}")
                else:
                    raise ValueError("Código de operação financeira inexistente.")

            elif opcao == "5":
                print("\n-- AUDITORIA DE BANCO DE DADOS (MEMÓRIA) --")
                if not clientes_db:
                    print("A base de dados está vazia.")
                    continue
                
                print(f"Total de clientes registrados: {len(clientes_db)}")
                for i, c in enumerate(clientes_db):
                    conta_vinculada = buscar_conta(banco._contas, c._email)
                    saldo_str = f"R${conta_vinculada.saldo}" if conta_vinculada else "Sem conta alocada"
                    
                    print(f"[{i+1}] {c._nome} | Chave: {c._email} | Limite Diário: R${c._limite_diario} | Status: {saldo_str}")

            elif opcao == "6":
                print("\nDestruindo variáveis e encerrando o processo...")
                sys.exit()

            else:
                print("\n[ERRO LÓGICO] Instrução desconhecida. Utilize estritamente os numerais do menu.")
                
        except decimal.InvalidOperation:
            print("\n[FALHA DE TIPAGEM] O valor inserido não obedece ao padrão decimal financeiro.")
        except Exception as e:
            print(f"\n[RESTRIÇÃO DE NEGÓCIO] A operação foi abortada pelo sistema: {str(e)}")

if __name__ == "__main__":
    main()