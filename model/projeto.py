from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base
from model.historico import Historico
from typing import Union
from sqlalchemy.exc import IntegrityError
import re

class Projeto(Base):
    __tablename__ = "projeto"  # Nome da tabela no banco de dados

    # Colunas do modelo 'Projeto'
    id = Column(Integer, primary_key=True)  # Identificador único do projeto
    nome = Column(String(150), unique=True, nullable=False)  # Nome do projeto, único e não nulo
    sigla = Column(String(10), unique=True, nullable=False)  # Sigla do projeto, único e não nulo
    descricao = Column(Text, nullable=True)  # Descrição do projeto (opcional)
    tipo = Column(String(50), nullable=False)  # Tipo de projeto (não nulo)
    # data_inicio = Column(Date, nullable=True)  # Data de início (comentada, caso necessário no futuro)
    # data_fim = Column(Date, nullable=True)  # Data de fim (comentada, caso necessário no futuro)
    custo = Column(Float, nullable=False)  # Custo do projeto (não nulo)
    status = Column(String(50), nullable=False)  # Status do projeto (não nulo)
    data_registro = Column(DateTime, default=datetime.now)  # Data de registro do projeto, padrão é o momento atual
    
    # Relacionamento com o modelo 'Historico', onde um projeto pode ter vários históricos associados.
    historico = relationship("Historico", back_populates="projeto", cascade="all, delete")

    # Construtor para inicializar o objeto 'Projeto'
    def __init__(self, nome: str, sigla: str, descricao: str, tipo: str, custo: float, status: str, data_registro: Union[DateTime, None] = None):
        """
        Inicializa uma instância do projeto e realiza as validações dos dados inseridos.

        :param nome: Nome do projeto
        :param sigla: Sigla do projeto
        :param descricao: Descrição do projeto (opcional)
        :param tipo: Tipo do projeto
        :param custo: Custo do projeto
        :param status: Status do projeto
        :param data_registro: Data de registro do projeto (opcional). Se não fornecida, será usada a data atual.
        """
        self.nome = nome
        self.sigla = sigla
        self.descricao = descricao
        self.tipo = tipo
        # self.data_inicio = data_inicio  # Comentado, caso você queira usar no futuro
        # self.data_fim = data_fim  # Comentado, caso você queira usar no futuro
        self.custo = custo
        self.status = status

        # Se não for fornecida, o valor de 'data_registro' será o horário da criação do registro
        if data_registro:
            self.data_registro = data_registro
        else:
            self.data_registro = datetime.now()

        # Chamando as validações
        self.validar_nome()
        #self.validar_sigla()
        self.validar_custo()


    def validar_nome(self):
        """
        Valida o nome do projeto para garantir que não ultrapasse o limite de caracteres e que seja único.
        """
        if len(self.nome) > 150:
            raise ValueError("O nome do projeto não pode ter mais de 150 caracteres.")
        

    def validar_sigla(self):
        """
        Valida a sigla do projeto para garantir que tenha no máximo 10 caracteres e siga um padrão específico.
        A sigla também deve ser única.
        """
        if len(self.sigla) > 10:
            raise ValueError("A sigla do projeto não pode ter mais de 10 caracteres.")
        
        # Verificando se a sigla segue um padrão (apenas letras maiúsculas e números)
        if not re.match("^[A-Z0-9]+$", self.sigla):
            raise ValueError("A sigla do projeto deve conter apenas letras maiúsculas e números.")


    def validar_custo(self):
        """
        Valida o custo do projeto para garantir que seja um valor positivo.
        """
        if self.custo <= 0:
            raise ValueError("O custo do projeto deve ser um valor positivo.")


    def adiciona_historico(self, historico: Historico):
        """
        Adiciona um novo histórico a este projeto.

        :param historico: Instância do modelo 'Historico' a ser associada ao projeto.
        """
        self.historico.append(historico)

    # Representação do objeto 'Projeto' como string
    def __repr__(self):
        """
        Retorna uma representação do objeto 'Projeto', útil para depuração e visualização dos objetos.
        """
        return f"<Projeto(id={self.id}, nome={self.nome}, sigla={self.sigla}, tipo={self.tipo}, custo={self.custo}, status={self.status})>"

