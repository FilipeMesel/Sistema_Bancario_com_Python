# Sistema Bancário em Python

Este repositório contém um código em Python que resolve o desafio proposto de desenvolver um sistema bancário para um grande banco. O objetivo é modernizar as operações utilizando a linguagem Python. Nesta nova versão do sistema, foram implantados dois novos códigos: "projeto_conta_bancaria_sqlite.py" e "projeto_conta_bancaria_mongodb.py"

## Funcionalidades

O código "projeto_conta_bancaria.py" apresenta um menu com as seguintes opções:

- [d] Depositar: adiciona um valor à conta.
- [s] Sacar: retira um valor da conta. O código possui uma constante "LIMITE_SAQUES" que permite apenas três saques por vez.
- [e] Extrato: imprime o histórico das transações.
- [q] Sair: fecha o programa.

Já o código "projeto_conta_bancaria_sqlite.py" apresenta um CRUD para criar, deletar, atualizar e ler Clientes e contas bancárias usando o banco de dados relacional SQLite e a biblioteca "sqlalchemy" (pip install sqlalchemy)

Já o código "projeto_conta_bancaria_mongodb.py" apresenta um CRUD para criar, deletar, atualizar e ler Clientes e contas bancárias usando o banco de dados não relacional mongoDB e a biblioteca "pymongo" (pip install pymongo)

## Branches

 - v001: Primeira versão do projeto. Apresenta conceitos iniciais do python
 - v002: Segunda versão do projeto. Apresenta modularização
 - v003: Terceira versão do projeto. Apresenta conceitos de POO
 - v004: Quarta versão do projeto. Apresenta integração com banco de dados relacionais (SQLite) e NoSQL (mongoDB Atlas)

## Dependências

Este projeto não possui as dependências:
 - Python 3.
 - sqlalchemy.
 - pymongo.

Sinta-se à vontade para clonar este repositório, explorar o código e adaptá-lo conforme necessário para atender às suas necessidades.

## Como utilizar

Qualquer pessoa é livre para clonar este repositório e executar o código localmente. Para isso, siga as instruções abaixo:

1. Certifique-se de ter o Python 3 instalado em seu sistema.
2. Clone este repositório para o seu ambiente local.

$ git clone https://github.com/FilipeMesel/Sistema_Bancario_com_Python.git


3. Navegue até o diretório do projeto.


4. Execute o código Python.

$ python projeto_conta_bancaria.py
