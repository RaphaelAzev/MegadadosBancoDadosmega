import pymysql
from fastapi import FastAPI
from functools import partial
from projeto import *
import json
from pydantic import BaseModel
from starlette.requests import Request

# def run_db_query(connection, query, args=None):
#     with connection.cursor() as cursor:
#         print('Executando query:')
#         cursor.execute(query, args)
        
#         #for result in cursor:
#         #    print(result)


with open('config_tests.json', 'r') as confjson:
    conf = json.load(confjson)

conn = pymysql.connect(
    host= conf['HOST'],
    user= conf['USER'],
    password= conf['PASS'],
    database='mydb')

conn.autocommit(True)

app = FastAPI()

class User(BaseModel):
    NomeUser: str
    email: str
    cidade: str

class Passaro(BaseModel):
    NomePassaro: str
    
class Cidade(BaseModel):
    NomeCidade: str

class Post(BaseModel):
    idUser: int
    Titulo: str
    Texto: str = None
    URL: str = None

class PostEdit(BaseModel):
    idPost: int
    novoTitulo: str = None
    novoTexto: str = None
    novoURL: str = None

class LikePost(BaseModel):
    idPostToLikeDislike: int
    idUserLiking: int

#Tabela Cidade
@app.post("/Cidades")
def add_cidade(cidade: Cidade):
    return adiciona_cidade(conn, cidade.NomeCidade)

@app.get("/Cidades")
def get_cidades():
    return lista_cidades(conn)

#Tabela User
@app.post("/Users")
def add_user(usuario: User):
    return adiciona_usuario(conn, usuario.NomeUser, usuario.email, usuario.cidade)

@app.get("/Users/{user_id}")
def get_user(user_id: int):
    return lista_usuarios_tudo_porid(conn, user_id)

@app.get("/Users")
def get_all_Users():
    return lista_usuarios_tudo(conn)

@app.get("/Users/posts/{user_id}")
def get_userPosts_by_TimeStampOrder(user_id: int):
    return lista_tudo_posts_usuario_em_ordem_cronologica(conn, user_id)
#Usuarios nao deveriam poder deletar outros
# @app.delete("/Users/{user_id}")
# def delete_user(user_id: int):
#     return remove_usuario(conn, user_id)

#Tabela Post
@app.post("/Posts")
def add_post(post: Post):
    return adiciona_post_parseia_mencoes(conn, post.idUser, post.Titulo, post.Texto, post.URL)

@app.put("/Posts")
def edita_post(post: PostEdit):
    if(post.novoTexto != None):
        edita_post_texto(conn, post.idPost, post.novoTexto)
    if(post.novoTitulo != None):    
        edita_post_titulo(conn, post.idPost, post.novoTitulo)
    if(post.novoURL != None):
        edita_post_URL(conn, post.idPost, post.novoURL)
    pass 

@app.get("/Posts")
def get_all_Posts(req: Request):
    ipdevice = req.client.host
    devicebrowserinfo = req.headers["user-agent"].split()
    #print("Esse é o primeiro {0}".format("".join(devicebrowserinfo[-3:-1])))
    #print("Esse é o segundo {0}".format(devicebrowserinfo[1]))
    adiciona_vizualizacao_em_post(conn, acha_usuario_aleatorio(conn), Post_id, ipdevice, "".join(devicebrowserinfo[-3:-1]), devicebrowserinfo[1])
    return lista_posts(conn)

@app.get("/Posts/{Post_id}")
def get_Post(Post_id: int, req: Request):
    ipdevice = req.client.host
    devicebrowserinfo = req.headers["user-agent"].split()
    #print("Esse é o primeiro {0}".format("".join(devicebrowserinfo[-3:-1])))
    #print("Esse é o segundo {0}".format(devicebrowserinfo[1]))
    adiciona_vizualizacao_em_post(conn, acha_usuario_aleatorio(conn), Post_id, ipdevice, "".join(devicebrowserinfo[-3:-1]), devicebrowserinfo[1])
    return acha_tudo_post_porid(conn, Post_id)

@app.delete("/Posts/{Post_id}")
def delete_post(Post_id: int):
    return remove_post(conn, Post_id)

#Tabela Passaros
@app.post("/Birds")
def add_Passaro(bird: Passaro):
    return adiciona_passaro(conn, bird.NomePassaro)

@app.get("/Birds")
def get_all_Passaros():
    return lista_passaros_nome(conn)

@app.get("/Birds/{bird_id}")
def get_Passaro(bird_id: int):
    return acha_passaro_porid(conn, bird_id)

#Usuarios não deveriam poder deletar passaros
# @app.delete("/Birds/{bird_id}")
# def delete_Passaro(bird_id: int):
#     return remove_passaro(conn, bird_id)

#Tabela Curtidas
@app.post("/Likes/Like")
def like_post_api(like: LikePost):
    return like_post(conn, like.idUserLiking, like.idPostToLikeDislike)

@app.post("/Likes/Dislike")
def dislike_post_api(like: LikePost):
    return dislike_post(conn, like.idUserLiking, like.idPostToLikeDislike)

@app.put("/Likes/Like")
def like_to_dislike(like: LikePost):
    return muda_para_dislike(conn, like.idUserLiking, like.idPostToLikeDislike)

@app.put("/Likes/Dislike")
def dislike_to_like(like: LikePost):
    return muda_para_like(conn, like.idUserLiking, like.idPostToLikeDislike)

@app.put("/Likes")
def remove_like_dislike(like: LikePost):
    return zera_estado_da_curtida(conn, like.idUserLiking, like.idPostToLikeDislike)

@app.get("/Likes/{user_id}")
def acha_likes_user(user_id: int):
    return acha_curtidas_de_usuario(conn, user_id)

#Tabela Cruzada para saber qnt de Aparelhos e Browsers
@app.get("/VizualizacaoCruzada")
def tabela_cruzada():
    return quantidade_de_tipo_de_aparelho_por_browser(conn)
