from datetime import date
from pydantic import ValidationError
from schema.projeto_schema import ProjetoSchema  # Ajuste o caminho conforme necessário

# Exemplo de payload válido
payload_valido = {
    "nome": "Projeto Exemplo",
    "sigla": "PE",
    "descricao": "Este é um projeto exemplo",
    "tipo": "Tipo 1",
    "data_inicio": "2024-12-01",
    "data_fim": "2024-12-31",
    "custo": 10000.00,
    "status": "Ativo"
}

# Exemplo de payload inválido
payload_invalido = {
    "nome": "Projeto Exempjjjlo",
    "sigla": "PE",
    "descricao": "Este é um projeto exemplo",
    "tipo": "Tipo 1",
    #"data_inicio": "31-12-2024",  # Formato errado
    #"data_fim": "01-01-2025",     # Formato errado
    "custo": 10000.00,
    "status": "Ativo"
}

def testar_payload(payload):
    try:
        projeto = ProjetoSchema(**payload)
        print("Payload válido:", projeto)
    except ValidationError as e:
        print("Erros de validação:")
        print(e.json())

# Teste com payload válido
print("Teste com payload válido:")
testar_payload(payload_valido)

# Teste com payload inválido
print("\nTeste com payload inválido:")
testar_payload(payload_invalido)
