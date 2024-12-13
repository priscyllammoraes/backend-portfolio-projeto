from flask import Flask, jsonify, request, redirect
from flask_openapi3 import OpenAPI, Info, Tag
from model import Session
from model.projeto import Projeto
from model.historico import Historico
from schema.projeto_schema import ProjetoSchema, ProjetoIdSchema, ProjetoEditSchema, ProjetoMsgSchema, ProjetoBuscaIdSchema, ListagemProjetoSchema
from schema.historico_schema import HistoricoSchema, HistoricoViewSchema
from schema.error_schema import ErrorSchema
from flask_cors import CORS
from logger import logger
from sqlalchemy.exc import IntegrityError


# Informações da API
info = Info(
    title="Portfólio de Projetos", 
    version="1.0.0",
    description="API para gerenciar o portfólio de projetos, incluindo a criação, exclusão e listagem de projetos e histórico."
)
app = OpenAPI(__name__, info=info)

'''
Rotas criadas:
    post: /projeto - Adicionar Projeto
    get: /projetos - Listar Projetos
    delete: /projeto - Deletar Projeto
    put: /projeto - Editar Projeto
    post: /historico - Adicionar Histórico
    get: /historico - Listar Histórico
'''

# Habilitar CORS
CORS(app)

# Definir tags para organizar os endpoints
projeto_tag = Tag(name="Projeto", description="Gerenciamento de Projetos")
historico_tag = Tag(name="Histórico", description="Gerenciamento de Histórico")

# Rota para redirecionamento para a página da documentação OpenAPI
@app.route('/')
def home():
    return redirect('/openapi')

# Rota para criar um novo projeto
@app.post("/projeto", tags=[projeto_tag], responses={"200": ProjetoMsgSchema, "400": ErrorSchema, "409": ErrorSchema})
def criar_projeto(body: ProjetoSchema):
    """Adiciona um novo projeto na base de dados.

    Retorna uma representação do projeto e histórico associado
    """
    try:
        # Convertendo o corpo da requisição para um dicionário
        projeto = Projeto(**body.dict())  

        # Sessão de banco de dados para persistir o projeto
        session = Session()
        session.add(projeto)
        session.commit()

        logger.info(f"Projeto '{projeto.id}' criado com sucesso!")
        return {"mensagem": "Projeto criado com sucesso!", "id": projeto.id}, 200
    except IntegrityError:
        # Erro de integridade, como duplicidade de dados
        session.rollback()
        logger.warning(f"Erro ao criar o projeto '{projeto.nome}': Nome ou sigla já existentes.")
        return {"mensagem": "Projeto com mesmo nome ou sigla já existe."}, 409
    except Exception as e:
        # Erro inesperado
        session.rollback()
        logger.error(f"Erro inesperado ao criar projeto: {e}")
        return {"mensagem": f"Erro ao criar projeto: {str(e)}"}, 400

# Rota para listar projetos
@app.get("/projetos", tags=[projeto_tag], responses={"200": ListagemProjetoSchema, "404": ErrorSchema})
def listar_projetos():
    """Lista todos os projetos cadastrados.

    Retorna uma representação da listagem de projetos.
    """
    session = Session()
    projetos = session.query(Projeto).all()
    logger.info(f"Listagem de projetos realizada com sucesso.")
    if not projetos:
        logger.info("Nenhum projeto encontrado na base de dados.")
        return jsonify({"mensagem": "Nenhum projeto encontrado."}), 200
    else:
        logger.info(f"%dProjetos encontrado:" % len(projetos))
        print(projetos)
        return jsonify([ProjetoIdSchema.from_orm(p).dict() for p in projetos])
    
@app.get('/projeto', tags=[projeto_tag], responses={"200": ProjetoIdSchema, "500": ErrorSchema})
def buscar_projeto(query: ProjetoBuscaIdSchema):
    """Buscar um projeto pelo ID fornecido.

    Retorna uma representação do projeto.
    """
    try:
        # Buscar o projeto no banco de dados pelo ID
        session = Session()
        projeto_id = query.id
        projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()

        if not projeto:
            return jsonify({"mensagem": "Projeto não encontrado"}), 404

        # Converter o objeto para JSON
        projeto = {
            "id": projeto.id,
            "nome": projeto.nome,
            "sigla": projeto.sigla,
            "descricao": projeto.descricao,
            "tipo": projeto.tipo,
            "custo": projeto.custo,
            "status": projeto.status,
            "data_registro": projeto.data_registro.strftime('%Y-%m-%d %H:%M:%S'),
        }
        logger.info("TESTE",projeto)
        return jsonify(projeto), 200

    except Exception as e:
        # Tratando qualquer erro inesperado
        error_msg = f"Erro interno ao tentar buscar o projeto com ID {projeto_id}: {str(e)}"
        logger.error(error_msg)
        return {"mensagem": error_msg}, 500

# Rota para deletar um projeto por ID
@app.delete('/projeto', tags=[projeto_tag], responses={"200": ProjetoMsgSchema, "404": ErrorSchema, "500": ErrorSchema})
def deletar_projeto(query: ProjetoBuscaIdSchema):
    """
    Deleta um projeto pelo ID fornecido.
    """
    try:
        session = Session()
        projeto_id = query.id
        projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()

        if not projeto:
            error_msg = f"Projeto com ID {projeto_id} não encontrado."
            logger.warning(error_msg)
            return {"mensagem": error_msg}, 404

        # Deletando o projeto
        session.delete(projeto)
        session.commit()
        logger.info(f"Projeto com ID {projeto_id} deletado com sucesso.")
        return {"mensagem": "Projeto removido", "id": projeto_id}, 200

    except Exception as e:
        # Tratando qualquer erro inesperado
        error_msg = f"Erro interno ao tentar deletar o projeto com ID {projeto_id}: {str(e)}"
        logger.error(error_msg)
        return {"mensagem": error_msg}, 500
    

@app.put('/projeto', tags=[projeto_tag], responses={"200": ProjetoSchema, "404": ErrorSchema, "400": ErrorSchema})
def editar_projeto(body: ProjetoEditSchema):
    """Edita um projeto existente com base nos dados fornecidos.

    O ID do projeto deve ser enviado no corpo da requisição.
    """
    session = Session()
    
    try:
        # Verificar se o ID foi fornecido
        projeto_id = body.id
        if not projeto_id:
            return {"mensagem": "ID do projeto não fornecido."}, 400
        
        # Buscando o projeto no banco de dados
        projeto = session.query(Projeto).filter_by(id=projeto_id).first()
        if not projeto:
            return {"mensagem": f"Projeto com ID {projeto_id} não encontrado."}, 404

        # Atualizando os atributos do projeto com os dados fornecidos
        for campo, valor in body.dict(exclude_unset=True).items():
            if hasattr(projeto, campo) and campo != "id":  # Evitar atualizar o campo 'id'
                setattr(projeto, campo, valor)

        # Validando as alterações
        projeto.validar_nome()
        projeto.validar_sigla()
        projeto.validar_custo()

        # Salvando as alterações no banco de dados
        session.commit()

        # Retornando resposta de sucesso
        return jsonify({"mensagem": "Projeto atualizado com sucesso!", "projeto": ProjetoSchema.from_orm(projeto).dict()}), 200

    except IntegrityError as e:
        session.rollback()
        return {"mensagem": f"Erro de integridade: {str(e)}"}, 400

    except ValueError as e:
        session.rollback()
        return {"mensagem": f"Erro de validação: {str(e)}"}, 400

    except Exception as e:
        session.rollback()
        return {"mensagem": f"Erro ao atualizar o projeto: {str(e)}"}, 500

    finally:
        session.close()

# Rota para adicionar histórico a um projeto
@app.post('/historico', tags=[historico_tag], responses={"201": HistoricoViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def add_historico(body: HistoricoSchema):
    """Adiciona um novo registro histórico a um projeto.

    Retorna uma lista de histórico.
    """
    session = Session()

    # Recuperando o ID do projeto no cabeçalho
    projeto_id = request.headers.get("projeto_id")
    if not projeto_id:
        error_msg = "ID do projeto não foi fornecido no header."
        logger.warning(error_msg)
        return {"mensagem": error_msg}, 400

    # Verificando se o projeto existe no banco de dados
    projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()
    if not projeto:
        error_msg = f"Projeto com ID {projeto_id} não encontrado."
        logger.warning(error_msg)
        return {"mensagem": error_msg}, 404

    # Criando o histórico e associando-o ao projeto
    historico = Historico(descricao=body.descricao, projeto_id=projeto_id)
    session.add(historico)
    session.commit()

    logger.info(f"Histórico adicionado ao projeto ID {projeto_id}.")
    return {
        "mensagem": "Histórico adicionado com sucesso!",
        "projeto": projeto_id,
        "descricao": body.descricao,}, 200

# Rota para listar o histórico de um projeto
@app.get('/historico', tags=[historico_tag], responses={"200": HistoricoViewSchema, "404": ErrorSchema})
def listar_historico():
    """Lista todo o histórico de um projeto.

    O ID do projeto deve ser enviado no cabeçalho da requisição.
    """
    session = Session()

    # Recuperando o ID do projeto no cabeçalho
    projeto_id = request.headers.get("projeto_id")
    if not projeto_id:
        error_msg = "ID do projeto não foi fornecido no header."
        logger.warning(error_msg)
        return {"mensagem": error_msg}, 400

    # Verificando se o projeto existe no banco de dados
    projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()
    if not projeto:
        error_msg = f"Projeto com ID {projeto_id} não encontrado."
        logger.warning(error_msg)
        return {"mensagem": error_msg}, 404

    # Recuperando o histórico associado ao projeto
    historicos = session.query(Historico).filter(Historico.projeto_id == projeto_id).all()
    print(historicos)

    # Formatando os dados do histórico
    historico_list = [
        {
            "id": historico.id,
            "descricao": historico.descricao,
            "data_insercao": historico.data_insercao.strftime("%d/%m/%Y %H:%M %Z")
        } for historico in historicos
    ]
    logger.info(f"Listagem de histórico do projeto ID {projeto_id} realizada com sucesso.")
    return {"projeto_id": projeto_id, "historico": historico_list}, 200


if __name__ == "__main__":
    app.run(debug=True)