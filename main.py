"""
Modulo principal, responsavel por fazer as operações de mais alto nível
"""
import random

from faker import Faker
from mongodb.connection import MongoDB
from mongodb.utils import insert_clients
from pprint import pprint
from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlite.utils import accounts_scalars_mapping
from sqlite.utils import cliente_scalars_mapping
from sqlite.utils import create_account
from sqlite.utils import create_client
from sqlite.utils import create_tables
from sqlite.utils import simple_select
from sqlite.models import Cliente
from sqlite.models import Conta

faker = Faker()
engine = create_engine('sqlite://')
rand_sequence_num = lambda n: ''.join([str(random.randint(0, 9)) for _ in range(n)])
rand_account_type = lambda: random.choice(['corrente', 'poupança', 'internacional'])

# Criando as tabelas no SQLite
created_tables = create_tables(engine)
print(f'Tabelas criadas: {created_tables}')

# Persistindo dados
for i in range(10):
    cliente = create_client(
        engine=engine,
        nome=faker.name(),
        cpf=rand_sequence_num(11),
        endereco=faker.address()[:9]
    )

    if cliente is not None:
        conta = create_account(
            engine=engine,
            tipo=rand_account_type(),
            agencia=rand_sequence_num(4),
            num=rand_sequence_num(8),
            id_cliente=cliente,
            saldo=0.0
        )
        print(f'status de criação da conta {i}: {conta}')

# Recuperando dados das tabelas do SQLite
clients = simple_select(engine, Cliente)
accounts = simple_select(engine, Conta)
current_accounts = simple_select(engine, Conta, Conta.tipo == 'corrente')

cliente_maps = cliente_scalars_mapping(clients)
conta_maps = accounts_scalars_mapping(accounts)

with engine.connect() as conn:
    stmt = text(
        'SELECT \
            cl.nome, cl.endereco, co.tipo, co.num, co.agencia \
        FROM cliente AS cl JOIN conta AS co \
        ON cl.id == co.id_cliente;'
    )
    res = conn.execute(stmt)
    fetch = res.fetchall()

# Migrando os dados do SQLite para o MongoDB
data = [
    {
        'nome_cliente': nome,
        'endereco_cliente': endereco,
        'tipo_conta': tipo,
        'num_conta': num,
        'agencia_conta': agencia
    } for nome, endereco, tipo, num, agencia in fetch
]
with MongoDB() as mdb:
    db = mdb.Bank
    result = insert_clients(
        db,
        clients_mapping=data,
    )
    print(f'Status da operação: {result}')

# Recuperando dados do MongoDB
with MongoDB() as mdb:
    db = mdb.Bank.clientes
    cursor = db.find({'tipo_conta': {'$in': ['corrente', 'poupança']}}).limit(100)
    for doc in cursor:
        pprint(doc)
    
print()
    
with MongoDB() as mdb:
    db = mdb.Bank.clientes
    cursor = db.find_one({'agencia_conta': '0001'})
    pprint(cursor)

print()

with MongoDB() as mdb:
    db = mdb.Bank.clientes
    cursor = db.find_one({'agencia_conta': '5638', 'tipo_conta': 'internacional'})
    pprint(cursor)

print()

with MongoDB() as mdb:
    db = mdb.Bank.clientes
    cursor = db.find({'$or': [{'agencia_conta': '6436'}, {'agencia_conta': '4652'}]})
    for doc in cursor:
        pprint(doc)
    