from operator import and_
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
import base64

from model import Session, Produto, Usuario
from schemas import *

from datetime import datetime

info = Info(title="Gescom WEB", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
usuario_tag = Tag(name="Usuario", description="Adição, visualização e remoção de usuarios à base")
                  
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor,
        data_validade=datetime.strptime(form.data_validade, '%d/%m/%Y') 
    )    

    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.post('/update_produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_produto(form: UpdateProdutoSchema):
    """Edita um Produto já salvo na base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    id_prod = form.id
    session = Session()
    
    try:
        query = session.query(Produto).filter(Produto.id == id_prod)
        db_produto = query.first()
        if not db_produto:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.nome:
                db_produto.nome = form.nome
            
            if form.quantidade:
                db_produto.quantidade = form.quantidade
            
            if form.valor:
                db_produto.valor = form.valor

            if form.data_validade:
                db_produto.data_validade = datetime.strptime( form.data_validade, '%d/%m/%Y' )

            session.add(db_produto)
            session.commit()
            return apresenta_produto(db_produto), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400
    

@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        # retorna a representação de produto
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.produto_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_id = query.produto_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.id == produto_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Produto removido", "id": produto_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        return {"mesage": error_msg}, 404


"""
   Abaixo segue os metodos POST/GET/Delete da base Usuario.
"""

@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """ Adiciona um novo Usuario à base de dados

    Retorna uma representação dos usuarios.
    """
    usuario = Usuario(
        nome = form.nome,
        email = form.email,
        senha = base64.b64encode( form.senha.encode() ) 
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionado usuario
        session.add(usuario)
        # efetivando o comando de adição de novo usuario na tabela.
        session.commit()
        return apresenta_usuario(usuario), 200
    
    except IntegrityError as e:
        # duplicidade no Email - IntegrityError
        error_msg = "Email já existe na base :/"
        return {"message": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo usuario :/"
        return {"mesage": error_msg}, 400       


@app.post('/update_usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_usuario(form: UpdateUsuarioSchema ):
    """Edita um Usuario já salvo na base de dados

    Retorna uma representação do usuario.
    """

    id = form.id
    #senha   = base64.b64encode( form.senha.encode() )

    session = Session()
    
    try:
        query = session.query(Usuario).filter(Usuario.id == id)
        db_usuario = query.first()
        if not db_usuario:
            # se o usuario não foi encontrado
            error_msg = "Usuário não encontrado na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.nome:
                db_usuario.nome = form.nome
            
            if form.email:
                db_usuario.email = form.email

            """
            if form.senha:
                db_usuario.senha = usuario.senha
            """

            session.add(db_usuario)
            session.commit()
            return apresenta_usuario(db_usuario), 200
    
    except IntegrityError as e:
        # como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Email com mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível alterar novo usuário :/"
        return {"mesage": error_msg}, 400


@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """ Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da Listagem de usuarios.
    """         
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não ha usuarios cadastrados
        return {"usuarios": []}, 200         
    else:
         # retorna a representação dos usuarios
         return apresenta_usuarios(usuarios), 200      


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioDelSchema, "404": ErrorSchema})    
def get_usuario(query: UsuarioBuscaSchema):
    """ Faz a busca por um Usuario a partir do ID

    Retorna uma representação do Usuario.
    """         
    usuario_id = query.usuario_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        error_msg = "Usuario não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})    
def del_usuario(query:UsuarioBuscaSchema):
    """ Deleta um usuario a partir do id informado
    
    Retorna uma mensagem de confirmação da remoção.
    """         
    usuario_id = query.usuario_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.id == usuario_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"message": "Usuario removido", "id": usuario_id}
    else:
        # se o usuario não foi encontrado
        error_msg = "Usuário não encontrado na base :/"
        return {"message": error_msg}, 404


@app.post('/validaLogin', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def valida_login(form: UsuarioValidaLoginSchema):
    """ 
        busca um usuario a partir do email e senha

    Retorna uma representação da Listagem de usuarios.
    """        
    usuario = Usuario(
        email   = form.email,
        senha   = form.senha
    )

    senha_s = base64.b64encode( form.senha.encode() )

    try:
        # criando conexão com a base
        session = Session()   
        # fazendo a busca
        query = session.query(Usuario).filter( Usuario.email == usuario.email, Usuario.senha == senha_s )  

        if query.count() == 0:
            error_msg = "Email não encontrado ou senha incorreta na base :/"
            return {"message": error_msg}, 404
        else:
            return apresenta_login(usuario), 200
        
    except Exception as e:
        error_msg = "Não foi possível encontrar o usuario: /"
        return {"mesage": error_msg}, 400       
