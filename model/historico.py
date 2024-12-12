from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base
from datetime import datetime
from typing import Union

class Historico(Base):
    __tablename__ = "historico"  # Nome da tabela no banco de dados
    
    # Colunas do modelo 'Historico'
    id = Column(Integer, primary_key=True)  # Identificador único do histórico
    descricao = Column(String(400), nullable=False)  # Descrição do histórico
    data_insercao = Column(DateTime, default=datetime.now)  # Data de inserção, usa o valor atual por padrão
    projeto_id = Column(Integer, ForeignKey("projeto.id"), nullable=False)  # Relacionamento com o projeto (chave estrangeira)

    # Relacionamento com o modelo 'Projeto', indicando que um histórico pertence a um projeto
    projeto = relationship("Projeto", back_populates="historico")

    # Construtor para inicializar o objeto 'Historico'
    def __init__(self, descricao: str, projeto_id: int, data_insercao: Union[DateTime, None] = None):
        """
        Inicializa uma instância de 'Historico'.

        :param descricao: Descrição do histórico
        :param projeto_id: ID do projeto ao qual o histórico pertence
        :param data_insercao: Data de inserção (opcional). Se não fornecido, a data atual será usada.
        """
        self.descricao = descricao
        self.projeto_id = projeto_id
        if data_insercao:
            self.data_insercao = data_insercao
        else:
            self.data_insercao = datetime.now()  # Usa a data atual se não fornecida

    # Representação do objeto 'Historico' como string
    def __repr__(self):
        """
        Retorna uma string representando o histórico, para facilitar a visualização dos objetos em logs e depuração.
        """
        return f"<Historico(descricao={self.descricao}, data_insercao={self.data_insercao})>"
