from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import Union

from model import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id    = Column("pk_usuario", Integer, primary_key=True)
    nome  = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    senha = Column( String(100), nullable=False ) 

    def __int__(self, nome:str, email:str, senha:str):

        """
        Cria um usuario

        Arguments.
            nome : nome do usuario
            email: email do usuario
            senha: senha
        """
        self.nome = nome
        self.email = email
        self.senha = senha



