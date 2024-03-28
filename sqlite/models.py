"""
Modulo reservado para a criação dos modelos do banco de dados SQLite
"""
from __future__ import annotations
import sqlalchemy
from typing import List
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

Base: DeclarativeBase = declarative_base()


class Cliente(Base):
    __tablename__ = 'cliente'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, 
        primary_key=True, 
        autoincrement=True
    )
    nome = sqlalchemy.Column(
        sqlalchemy.String(),
    )
    cpf = sqlalchemy.Column(
        sqlalchemy.String(9),
        unique=True,
        nullable=False,
    )
    endereco = sqlalchemy.Column(
        sqlalchemy.String(9)
    )
    conta: Mapped[List["Conta"]] = relationship(back_populates='cliente')


class Conta(Base):
    __tablename__ = 'conta'
    
    id = sqlalchemy.Column(
        sqlalchemy.Integer, 
        primary_key=True, 
        autoincrement=True
    )
    tipo = sqlalchemy.Column(
        sqlalchemy.String()
    )
    agencia = sqlalchemy.Column(
        sqlalchemy.String()
    )
    num = sqlalchemy.Column(
        sqlalchemy.Integer()
    )
    id_cliente = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            'cliente.id'
        )
    )
    saldo = sqlalchemy.Column(
        sqlalchemy.DECIMAL(),
        default=0.0
    )
    cliente: Mapped["Cliente"] = relationship(back_populates='conta')
