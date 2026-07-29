from datetime import datetime
import re

def validar_email(email: str) -> None:
    if not isinstance(email, str):
        raise TypeError("O email deve ser uma string.")

    padrao_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(padrao_regex, email):
        raise ValueError("O email fornecido não é válido.")

def estruturar_data(data_string: str) -> str:
    if not isinstance(data_string, str):
        raise TypeError("A data deve ser uma string.")

    data_sanitizada = data_string.replace(" ", "").replace("-", "/").strip()

    try:
        # Valida se a data existe e formata, garantindo a conversão correta
        datetime.strptime(data_sanitizada, "%d/%m/%Y")  
    except ValueError:
        raise ValueError("A data não está no formato correto (DD/MM/YYYY).")

    return data_sanitizada

def estruturar_telefone(telefone: str) -> str:
    if not isinstance(telefone, str):
        raise TypeError("O telefone deve ser uma string.")

    telefone_sanitizado = telefone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").strip()

    padrao_regex = r"^\d{10,11}$"

    if not re.match(padrao_regex, telefone_sanitizado):
        raise ValueError("O telefone fornecido não é válido.")

    return telefone_sanitizado