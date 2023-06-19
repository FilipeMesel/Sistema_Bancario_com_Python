from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, ForeignKey, inspect, select, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    # Criando a tabela:
    __tablename__ = "user_account"

    # Definindo os atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)

    #Estabelecendo uma relação entre a tabela Address e a tabela User
    conta = relationship(
        "Conta", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, cpf={self.cpf})"

class Conta(Base):
    # Criando a tabela:
    __tablename__ = "conta"

    # Definindo os atributos
    id = Column(Integer, primary_key=True)
    agencia = Column(String(30), nullable=False)
    nro_conta = Column(String(30), nullable=False)
    saldo = Column(Integer, nullable=False)  # Corrigir o nome da coluna para "saldo"
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    #Estabelecendo uma relação entre a tabela Address e a tabela User
    user = relationship("User", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, agencia={self.agencia}, nro_conta={self.nro_conta}, saldo={self.saldo})"


print(User().__tablename__)
print(Conta().__tablename__)

#Conexão com o banco de dados do tipo sqlite
engine = create_engine('sqlite:///meu_banco_de_dados.db')
#Criando as classes como tabelas no banco de dados
Base.metadata.create_all(bind=engine)

#O inspetor investiga o banco de dados
inspetor_engine = inspect(engine)

#Retornando o nome das tabelas
print(inspetor_engine.get_table_names())

#Buscando o nome do esquema do banco
print(inspetor_engine.default_schema_name)

#Criando uma sessão para add dados ao banco
with Session(engine) as session:
    session.commit()

def is_cliente_no_banco(cpf):
    print("CPF: ",cpf)
    stmt = session.query(User).filter_by(cpf=cpf).first()
    if stmt == None:
        return False
    else:
        return True

def cliente_criar(nome, cpf):
    if is_cliente_no_banco(cpf) == False:
        cliente = User(name=nome, cpf=cpf)
        session.add(cliente)
        session.commit()
        print("Cliente cadastrado com sucesso")
    else:
        print("Cliente já cadastrado")

def conta_criar(cpf, agencia, nro_conta):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = session.query(User).filter_by(cpf=cpf).first()
        print(stmt.cpf)
        if len(stmt.conta):
            for conta in stmt.conta:
                if conta.nro_conta == nro_conta:
                    print("Conta Já cadastrada!")
                    return False
            stmt.conta.append(Conta(agencia = agencia, nro_conta = nro_conta, saldo = 0))
            session.commit()
            print("Conta cadastrada com sucesso!")
        else:
            stmt.conta.append(Conta(agencia = agencia, nro_conta = nro_conta, saldo = 0))
            session.commit()
            print("Conta cadastrada com sucesso!")
        # stmt = session.query(User).filter_by(cpf=cpf).first()
        # print(stmt.conta)

def conta_apagar(cpf, nro_conta):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = session.query(User).filter_by(cpf=cpf).first()
        print(stmt.cpf)
        if len(stmt.conta):
            for conta in stmt.conta:
                if conta.nro_conta == nro_conta:
                    session.delete(conta)
                    session.commit()
                    print("Conta deletada com sucesso!")
                    return True
            print("Conta não encontrada")
            return False
        else:
            print("Conta não encontrada")
            return False

def cliente_apagar(cpf):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = session.query(User).filter_by(cpf=cpf).first()
        session.delete(stmt)
        if is_cliente_no_banco(cpf) == False:
            print("Cliente deletado!")
            return False
        session.commit()

def conta_realizar_transacao(transaction, cpf, nro_conta, valor):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = session.query(User).filter_by(cpf=cpf).first()
        print(stmt.cpf)
        if len(stmt.conta):
            for conta in stmt.conta:
                if conta.nro_conta == nro_conta:
                    if transaction == '+':
                        conta.saldo += valor
                    else:
                        conta.saldo -= valor
                    stmt = session.query(User).filter_by(cpf=cpf).first()
                    print(stmt.conta)
                    session.commit()
                    print("Conta atualizada com sucesso!")
                    return True
            print("Conta não encontrada")
            return False
        else:
            print("Conta não encontrada")
            return False
            

cliente_criar("filipe", "1")
print("criar conta: ")
conta_criar("1", "1", "3")
conta_apagar("1", "3")
conta_realizar_transacao("+", "1", "1", 100)
conta_realizar_transacao("-", "1", "1", 2)
cliente_apagar("1")

