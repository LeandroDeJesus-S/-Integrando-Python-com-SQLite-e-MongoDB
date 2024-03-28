"""
Modulo contendo funções uteis para manipulação do banco de dados MongoDB.
"""
from typing import Mapping, Any
from pymongo.database import Database


def insert_client(db: Database, client_mapping: Mapping[str, Any]) -> Any:
    """Insere um unico cliente no banco de dados

    Args:
        db (pymongo.database.Database): Instancia da Base de dados do MongoDB.
        client_mapping (Mapping[str, Any]): Dados mapeados do cliente.
    
    Returns:
        type (Any): id do cliente inserido.
    """
    clients_collection = db.clientes
    result = clients_collection.insert_one(client_mapping)
    return result.inserted_id


def insert_clients(db: Database, clients_mapping: list[Mapping[str, Any]]) -> list[Any]:
    """Insere multiplos clientes no banco de dados

    Args:
        db (pymongo.database.Database): Instancia da Base de dados do MongoDB.
        clients_mapping (List[Mapping[str, Any]]): Lista com os dados mapeados do cliente.
    
    Returns:
        type (list[Any]): id do clientes inserido.
    """
    clients_collection = db.clientes
    result = clients_collection.insert_many(clients_mapping)
    return result.inserted_ids
