from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from schema.historico_schema import HistoricoSchema
from model.projeto import Projeto


class ProjetoSchema(BaseModel):
    """
    Schema para representar os dados de um projeto.

    Este schema pode ser usado para criar e representar um projeto.
    """
    nome: str = "Sistema de Gestão de Portifólio de Projetos"  # Nome do projeto
    sigla: str = "SIGEPP"  # Sigla do projeto
    descricao: Optional[str] = "Projeto de especificação e desenvolvimento de sistema para manter um portifólio de projetos de TI gerenciados na área."  # Descrição do projeto, pode ser opcional
    tipo: str = "Interno"  # Tipo de projeto, ex: Interno, Externo
    custo: float = "10000"  # Custo do projeto
    status: str = "Em andamento"  # Status do projeto, ex: 'Em andamento', 'Concluído'

    class Config:
        orm_mode = True  # Permite a conversão de ORM para Pydantic



class ProjetoIdSchema(BaseModel):
    """
    Schema para representar um projeto, utilizando apenas o ID.

    Este schema pode ser útil quando queremos representar um projeto apenas pelo seu ID.
    """
    id: int  # ID do projeto
    nome: str = "Nome Projeto" # Nome do projeto
    sigla: str = "SIGEPP"  # Sigla do projeto
    descricao: Optional[str] = "Projeto de especificação e desenvolvimento de sistema para manter um portifólio de projetos de TI gerenciados na área."  # Descrição do projeto, opcional
    tipo: str = "Interno" # Tipo de projeto
    custo: float = "10000" # Custo do projeto
    status: str = "Em andamento" # Status do projeto
    data_registro: date = '01/01/2024'
    historico:List[HistoricoSchema]

    class Config:
        orm_mode = True  # Permite a conversão de ORM para Pydantic

class ProjetoEditSchema(BaseModel):
    """
    Schema para representar um projeto, utilizando apenas o ID.

    Este schema pode ser útil quando queremos representar um projeto apenas pelo seu ID.
    """
    id: int  # ID do projeto
    nome: str = "Nome Projeto" # Nome do projeto
    sigla: str = "SIGEPP"  # Sigla do projeto
    descricao: Optional[str] = "Projeto de especificação e desenvolvimento de sistema para manter um portifólio de projetos de TI gerenciados na área."  # Descrição do projeto, opcional
    tipo: str = "Interno" # Tipo de projeto
    custo: float = "10000" # Custo do projeto
    status: str = "Em andamento" # Status do projeto

    class Config:
        orm_mode = True  # Permite a conversão de ORM para Pydantic


        
class ProjetoViewSchema(BaseModel):
    """
    Schema para representar o retorno de um projeto com o histórico.

    Este schema será utilizado para retornar um projeto junto com seu histórico associado.
    """
    id: int
    nome: str = "Projeto Teste"
    sigla: str = "PJT"
    descricao: str = "Descrição do projeto teste."
    status: str = "Em andamento"
    custo: float = 12.50
    data_registro: date = '01/01/2024'
    historico:List[HistoricoSchema]


class ListagemProjetoSchema(BaseModel):
    """
    Schema para retornar uma lista de projetos.
    """
    projetos: List[ProjetoViewSchema]  # Lista de projetos


class ProjetoBuscaNomeSchema(BaseModel):
    """
    Schema para representar a busca de projetos com base no nome.
    """
    nome: str  # Nome do projeto a ser buscado


class ProjetoBuscaIdSchema(BaseModel):
    """
    Schema para representar a busca de projetos com base no ID.
    """
    id: int  # ID do projeto a ser buscado


class ProjetoMsgSchema(BaseModel):
    """
    Schema para representar a resposta de uma requisição de remoção de um projeto.
    """
    mensagem: str  # Mensagem de sucesso ou erro
    id: int  # ID do projeto excluído


# def apresenta_projeto(projeto: Projeto):
#     """ Retorna uma representação do projeto seguindo o schema definido em
#         ProjetoViewSchema.
#     """
#     return {
#         "id": projeto.id,
#         "nome": projeto.nome,
#         "sigla": projeto.sigla,
#         "descricao": projeto.descricao,
#         "custo": projeto.custo,
#         "data_registro": projeto.data_registro,
#         "total_cometarios": len(projeto.historico),
#         "historico": [{"descricao": c.descricao} for c in projeto.historico]
#     }


# def apresenta_projetos(projetos: List[Projeto]):
#     """ Retorna uma representação do projeto seguindo o schema definido em
#         ProjetoViewSchema.
#     """
#     result = []
#     for projeto in projetos:
#         result.append(apresenta_projeto(projeto))

#     return {"projetos": result}