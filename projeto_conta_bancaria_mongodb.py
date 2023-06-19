import pymongo as pyM
import datetime

#Connectando ao cluster do mongoDB Atlas
#user -> Nickname do administrador
#password -> Senha de acesso ao administrador
client = pyM.MongoClient("mongodb+srv://<user>:<password>@cluster1.os5a8p6.mongodb.net/?retryWrites=true&w=majority")

#Vamos definir "test" como banco de dados
db = client.test

#Verificando se há uma coleção (Coleções são tabelas de bancos de dados não relacionais)
collection = db.test_collection
print(db.list_collection_names())

#Criando múltiplos documentos pelo índice de forma ascendente na nova coleção "Users"
result = db.Users.create_index([('cpf', pyM.ASCENDING)], unique = True)
print(sorted(list(db.Users.index_information())))

#Constante user_id
user_id = 1


def is_cliente_no_banco(cpf):
    print("CPF: ",cpf)
    stmt = db.Users.find_one({"cpf": cpf})
    print("stmt: ",stmt)
    if stmt == None:
        return False
    else:
        return True

def cliente_criar(nome, cpf, user_id):
    if is_cliente_no_banco(cpf) == False:
        user_profile_user = {'user_id': user_id, 'name': nome, 'cpf': cpf, 'contas':[]}
        result = db.Users.insert_one(user_profile_user)
        user_id += 1
        print("Cliente cadastrado com sucesso")
    else:
        print("Cliente já cadastrado")

def conta_criar(cpf, agencia, nro_conta):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = db.Users.find_one({"cpf": cpf})
        print(stmt['cpf'])
        if len(stmt['contas']):
            for conta in stmt['contas']:
                if conta['nro_conta'] == nro_conta:
                    print("Conta Já cadastrada!")
                    return False
            stmt['contas'].append({'agencia': agencia, 'nro_conta': nro_conta, 'saldo': 0})
            new_data = {"name": stmt["name"], "cpf": stmt['cpf'], "contas": stmt['contas']}
            db.Users.update_one({"user_id": stmt["user_id"]}, {"$set": new_data})
            print(stmt)
            print("Conta cadastrada com sucesso!")
        else:
            stmt['contas'].append({'agencia': agencia, 'nro_conta': nro_conta, 'saldo': 0})
            new_data = {"name": stmt["name"], "cpf": stmt['cpf'], "contas": stmt['contas']}
            db.Users.update_one({"user_id": stmt["user_id"]}, {"$set": new_data})
            print(stmt)
            print("Conta cadastrada com sucesso!")

def conta_apagar(cpf, nro_conta):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = db.Users.find_one({"cpf": cpf})
        print(stmt['cpf'])
        if len(stmt['contas']):
            idx = 0
            for conta in stmt['contas']:
                if conta['nro_conta'] == nro_conta:
                    del stmt['contas'][idx]
                    print("Conta deletada com sucesso!")
                    new_data = {"name": stmt["name"], "cpf": stmt['cpf'], "contas": stmt['contas']}
                    db.Users.update_one({"user_id": stmt["user_id"]}, {"$set": new_data})
                    print(stmt)
                    return True
                idx += 1
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
        # Definir o critério para encontrar o documento a ser apagado
        critério = {'cpf': cpf}
        # Apagar o documento que corresponda ao critério
        resultado = db.Users.delete_one(critério)
        if is_cliente_no_banco(cpf) == False:
            print("Cliente deletado!")
            return False
        else:
            print("Erro ao tentar deletar o cliente")


def conta_realizar_transacao(transaction, cpf, nro_conta, valor):
    if is_cliente_no_banco(cpf) == False:
        print("Cliente não cadastrado")
        return False
    else:
        stmt = db.Users.find_one({"cpf": cpf})
        print(stmt['cpf'])
        if len(stmt['contas']):
            idx = 0
            for conta in stmt['contas']:
                if conta['nro_conta'] == nro_conta:
                    if transaction == '+':
                        conta['saldo'] += valor
                    else:
                        conta['saldo'] -= valor
                    stmt['contas'][idx] = conta
                    new_data = {"name": stmt["name"], "cpf": stmt['cpf'], "contas": stmt['contas']}
                    db.Users.update_one({"user_id": stmt["user_id"]}, {"$set": new_data})
                    print(stmt)
                    print("Conta atualizada com sucesso!")
                    return True
                idx += 1
            print("Conta não encontrada")
            return False
        else:
            print("Conta não encontrada")
            return False

print("criar cliente")
cliente_criar("Fulano", "1", user_id)
cliente_criar("Ciclano", "2", user_id)
print("criar conta")
conta_criar("1", "1", "1")
conta_criar("1", "1", "2")

print("criar transacao")
conta_realizar_transacao('+', "1", "1", 100)
conta_realizar_transacao('-', "1", "1", 2)
conta_realizar_transacao('+', "1", "2", 100)

conta_apagar("1", "1")
cliente_apagar("2")