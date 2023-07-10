from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date
from datetime import datetime
from model.produto import Produto
import re

class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "BANANA PRATA"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    data_validade: str = "25/12/2023"

    @validator('data_validade')
    def valida_data_validade(cls, v):
        if re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", v):
            return v

        raise ValueError('A data tem que ser no formato dd/mm/aaaa')    


class UpdateProdutoSchema(BaseModel):
    """ Define como um novo produto pode ser atualizado.
    """
    id : int = 1
    nome: str = "BANANA PRATA"
    quantidade: Optional[int] = 12
    valor: Optional[float] = 12.50
    data_validade: Optional[str] = "25/12/2023"


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do produto.
    """
    produto_id: int = 1


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
            "data_validade": datetime.strftime(produto.data_validade, '%d/%m/%Y')            
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto.
    """
    id: int = 1
    nome: str = "BANANA PRATA"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    data_validade: str = "25/12/2023"    


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        "data_validade": datetime.strftime(produto.data_validade, '%d/%m/%Y')        
    }
