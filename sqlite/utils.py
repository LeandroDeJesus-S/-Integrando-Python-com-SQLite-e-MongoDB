"""
Modulo contendo funções uteis para criação e manipulação do banco de dados
sqlite.
"""
from typing import Mapping, Any

from sqlalchemy import Column
from sqlalchemy import Engine
from sqlalchemy import Select
from sqlalchemy import Table
from sqlalchemy.orm import Session
from sqlite.models import Base
from sqlite.models import Cliente
from sqlite.models import Conta


def create_tables(engine: Engine) -> list:
    """Cria as tabelas verificando se já existe

    Args:
        engine (Engine): Um objeto sqlalqchemy.Engine.
    
    Returns:
        type (list): Lista com o nome das tabelas que foram criadas.
        Se nenhum tabela for criada, retorna uma lista vazia.
    """
    created_tables = []
    for table in Base.metadata.tables.keys():
        Base.metadata.tables[table].create(engine, checkfirst=True)
        created_tables.append(table)
    
    return created_tables


def create_client(engine: Engine, nome: str, cpf: str, endereco: str) -> Column[int]|None:
    """Adiciona um novo cliente na base de dados

    Args:
        engine (Engine): Um objeto sqlalqchemy.Engine.
        nome (str): Nome do cliente
        cpf (str): cpf do cliente com 9 digitos
        endereco (str): endereço do cliente com máximo 9 digitos
    
    Returns:
        type (sqlalchemy.Column[int] | None): Retorna o id do novo cliente
        ou None caso o cliente não seja persistido na base de dados.
    """
    with Session(engine) as session:
        try:
            cliente = Cliente(
                nome=nome,
                cpf=cpf,
                endereco=endereco
            )
            session.add(cliente)

        except Exception as e:
            print(e)
            session.rollback()
            return None

        else:
            session.commit()
            return cliente.id


def create_account(engine: Engine, tipo: str, agencia: str, num: str, id_cliente: int, saldo: float=0.0) -> bool:
    """Adiciona uma conta para um cliente

    Args:
        engine (Engine): Um objeto sqlalqchemy.Engine.
        tipo (str): Tipo da conta. Ex.: Corrente, Poupança, ...
        agencia (str): Número da agência
        num (str): Número da conta.
        id_cliente (str): Id do cliente ao qual a conta pertencerá.
        saldo (float, Opicional): Valor do saldo em conta, Por padrão é 0.
    
    Returns:
        type (bool): Retorna True se a conta for persistida sem erros. 
        Caso contrario, retorna False.
    """
    with Session(engine) as session:
        try:
            conta = Conta(
                tipo=tipo,
                agencia=agencia,
                num=num,
                id_cliente=id_cliente,
                saldo=saldo
            )
            session.add(conta)

        except Exception as e:
            print(e)
            session.rollback()
            return False

        else:
            session.commit()
            return True


def create_client_with_account(engine: Engine, client_map: Mapping[str, Any], account_map: Mapping[str, Any]) -> bool:
    """
    Args:
        engine (Engine): Um objeto sqlalqchemy.Engine.
        client_map (Mapping[str, Any]): Valores mapeados para a entidade Cliente.
        account_map (Mapping[str, Any]): Valores mapeados para a entidade Conta.
        Não incluindo o atribudo `id_client`.
    
    Returns:
        type (bool): Retorna True se o cliente e a conta forem persistidos no banco de dados.
        Caso contrário, retorna False.
    """
    id_client = create_client(engine, **client_map)
    if id_client is None:
        return False
    
    return create_account(engine, **account_map)


def simple_select(engine: Engine, model: Any, whereclause=None, limit=100) -> list:
    """
    Args:
        engine (Engine): Um objeto sqlalqchemy.Engine.
        model (Any): Instancia de um objeto originado de sqlite.models.Base
        whereclause (Any, Opcional): Query para clausa where.
        limit (int, Opcional): Quantidade imite de dados.
    
    Returns:
        type (bool): Retorna uma lista de tuplas com os registros encontrados.
    """
    with Session(engine) as session:
        stmt = Select(model)
        if whereclause is not None:
            stmt = stmt.where(whereclause)
        
        stmt = stmt.limit(limit)
        data = [tup for tup in session.scalars(stmt)]
    return data


def cliente_scalars_mapping(scalars: Any) -> list[dict]:
    """Formata scalars do model cliente em uma lista de dicionarios contendo o nome do
    atributo e o valor.

    Args:
        scalars (Any): resultado de sqlite.utils.simple_select

    Returns:
    type (list[dict]): scalars formatados.
    """
    maps = [
        {
            'id': c.id,
            'nome': c.nome,
            'cpf': c.cpf,
            'endereco': c.endereco
        }
        for c in scalars
    ]
    return maps


def accounts_scalars_mapping(scalars):
    """Formata scalars do model conta em uma lista de dicionarios contendo o nome do
    atributo e o valor.

    Args:
        scalars (Any): resultado de sqlite.utils.simple_select

    Returns:
    type (list[dict]): scalars formatados.
    """
    maps = [
        {
            'id': a.id,
            'tipo': a.tipo,
            'agencia': a.agencia,
            'num': a.num,
            'id_cliente': a.id_cliente,
            'saldo': a.saldo
        }
        for a in scalars
    ]
    return maps
