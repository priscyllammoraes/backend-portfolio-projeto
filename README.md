
# Portfólio de Projetos - API

  

Este projeto foi elaborado para o MVP da Disciplina **Desenvolvimento Full Stack Básico**.
Seu objetivo é prover um sistema de Gestão de Portfólio de Projetos, permitindo o cadastro, edição, exclusão; e ainda, o registro de um histórico sobre cada projeto. Foi desenvolvido em **Python** utilizando as tecnologias **SQLAlchemy**, **SQLite**, **Flask**, **Pydantic**, e **Flask-OpenAPI3**.

  

## Funcionalidades

  

1.  **Gerenciamento de Projetos**:

- Cadastro, edição e exclusão de projetos.

- Atributos de cada projeto: ID, Nome, Sigla, Descrição, Tipo, Custo, Status (A iniciar, Em andamento, Suspenso, Concluído, Cancelado) e Data de registro

  

2.  **Gerenciamento de Histórico**:

- Registro de múltiplas entradas de histórico para cada projeto.

- Visualização dos históricos registrados.

  

3.  **API REST**:

- Endpoints para gerenciamento dos projetos e históricos.

- Documentação gerada automaticamente com **Flask-OpenAPI3**.
 

## Tecnologias Utilizadas

  

 **Back-end**:

- Python

- Flask

- SQLAlchemy

- SQLite

- Flask-CORS

- Flask-OpenAPI3

- Pydantic
 

## Requisitos do Sistema

  - Python 3.10 ou superior

- Pacotes Python listados em `requirements.txt`

  
## Como Rodar o Projeto

  

### 1. Clonar o Repositório

``` bash
    git  clone  https://github.com/seu-usuario/portfolio-de-projetos.git
    cd  portfolio-de-projetos
 ```

### 2. Instalar bibliotecas
 
Será  necessário  ter  todas  as  bibliotecas  python  listadas  no  `requirements.txt`  instaladas.

Após  clonar  o  repositório,  é  necessário  ir  ao  diretório  raiz,  pelo  terminal,  para  poder  executar  os  comandos  descritos  abaixo.

```
(env)$ pip install -r requirements.txt
```
Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.


### 3. Executar a API

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.