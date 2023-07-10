from pydantic import BaseModel
from typing import Optional, List   
from model.usuario import Usuario
import base64


class UsuarioSchema(BaseModel):
    """ Define como um novo usuario a ser inserido dever ser representado
    """
    nome: str = "RONES MENDONCA"
    email: str = "rones@rmsys.net"
    senha: str = "123456"

class UpdateUsuarioSchema(BaseModel):
    """ Define como um email pode ser atualizado.
    """
    id : int = 1
    nome: str = "RONES MENDONCA"
    email: str = "rones@rmsys.net"

class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id o usuario.
    """    
    usuario_id: int = 1


class UsuarioValidaLoginSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no email e senha do usuario.
    """    
    email: str = "rones@rmsys.net"
    senha: str = "123456"


class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuarios será retornada.
    """
    usuarios:List[UsuarioSchema]   


def apresenta_usuarios(usuarios: List[Usuario] ):
    """ Retorna uma representação do usuario seguindo o schema definido em 
        UsuarioViewSchema.
    """
    result=[]
    for usuario in usuarios:        
        result.append({
               "id": usuario.id,
             "nome": usuario.nome,
            "email": usuario.email,
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um usuario será retornado.
    """
    email: str = "rones@rmsys.net"
    senha: str = "123456"


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    message: str
    email: str

def apresenta_usuario(usuario: Usuario):
    """ Retorna um representação do usuario seguindo o schema definido em 
        UsuarioViewSchema.
    """
    return {
           "id": usuario.id,
         "nome": usuario.nome,
        "email": usuario.email,
    }

def apresenta_login(usuario: Usuario):
    """ Retorna um representação do usuario seguindo o schema definido em 
        UsuarioViewSchema.
    """
    return {
        "email": usuario.email,
        "senha": usuario.senha,
    }