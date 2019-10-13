import pymysql

#FUNÇÕES USUARIO

def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            adiciona_cidade(conn, cidade)
            cursor.execute('INSERT INTO user (Nome,Email,Cidade) VALUES((%s),(%s),(%s))', (nome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela user')

def acha_usuario(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser FROM user WHERE Nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, id, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE user SET nome=%s where idUser=%s', (novo_nome, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario')

def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM user WHERE idUser=%s', (id))

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser from user')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#FUNÇÕES CIDADE

def adiciona_cidade(conn, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT IGNORE INTO cidades (Nome) VALUES (%s)', (cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {cidade} na tabela cidades')

def acha_cidade(conn, cidade):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome FROM cidades WHERE nome = %s', (cidade))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#FUNÇOES PÁSSAROS

def adiciona_passaro(conn, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT IGNORE INTO Passaros (Nome) VALUES (%s)', (nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela user')

def acha_passaro(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPassaros FROM Passaros WHERE Nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPassaros from Passaros')
        res = cursor.fetchall()
        Passaros = tuple(x[0] for x in res)
        return Passaros

def remove_passaro(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Passaros WHERE idPassaros=%s', (id))

#FUNÇÕES POST

def adiciona_post(conn, iduser, titulo, Texto=None, Url=None):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Post (Titulo,Url,Texto,Ativo,User_idUser) VALUES (%s, %s, %s , %s, %s)' , (titulo, Url, Texto, "True", iduser))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possível inserir o post do usuario de id {iduser} na tabela Post')

def acha_post_portitulo(conn, Titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Post WHERE Titulo = %s', (Titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_post_porid(conn, idpost):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Titulo FROM Post WHERE idPost = %s', (idpost))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def lista_posts(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Post WHERE Ativo = "True"')
        res = cursor.fetchall()
        #Posts = tuple(x[0] for x in res)
        return res

def lista_posts_usuario(conn, iduser):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Post WHERE User_idUser=%s AND Ativo = "True"', (iduser))
        res = cursor.fetchall()
        Posts = tuple(x[0] for x in res)
        return Posts 

def remove_post(conn, id_post):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Post SET Ativo = "False" WHERE idPost = %s', (id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possível remover o post escolhido da tabela Post')

def status_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Ativo FROM Post WHERE idPost=%s', (id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def edita_post_titulo(conn, idpost, novo_titulo):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Post SET Titulo=%s WHERE idPost=%s', (novo_titulo, idpost))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possível alterar o titulo do Post de id: {idpost} para {novo_titulo}')
 
def edita_post_texto(conn, idpost, novo_texto):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Post SET Texto=%s WHERE idPost=%s', (novo_texto, idpost))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possível alterar o texto do Post de id: {idpost} para {novo_texto}')

def edita_post_URL(conn, idpost, novo_URL):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Post SET URL=%s WHERE idPost=%s', (novo_URL, idpost))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possível alterar a URL do Post de id: {idpost} para {novo_URL}')  

#FUNÇÕES PASSARO-USUARIO

def adiciona_passaro_favorito(conn, id_usuario, passaro):
    with conn.cursor() as cursor:
        adiciona_passaro(conn, passaro)
        id_passaro = acha_passaro(conn, passaro)
        try:
            cursor.execute('INSERT INTO Passaro_User (User_idUser, Passaros_idPassaros) VALUES (%s,%s)', (id_usuario, id_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {passaro} e {id_usuario} na tabela Passaro_User')

def remove_passaro_favorito(conn, id_usuario, passaro):
    with conn.cursor() as cursor:
        id_passaro = acha_passaro(conn, passaro)
        try:
            cursor.execute('DELETE FROM Passaro_User WHERE (User_idUser=%s) AND (Passaros_idPassaros=%s)', (id_usuario, id_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {passaro} e ao usuario de id {id_usuario} na tabela Passaro_User')

def acha_passaro_favoritos(conn, id, passaro):
    with conn.cursor() as cursor:
        
        cursor.execute('SELECT Passaros_idPassaros FROM Passaro_User WHERE (User_idUser=%s) AND (Passaros_idPassaros=%s)', (id,acha_passaro(conn, passaro)))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def lista_passaros_favoritos(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Passaros_idPassaros from Passaro_User  WHERE User_idUser = %s', (id))
        res = cursor.fetchall()
        Passaros = tuple(x[0] for x in res)
        return Passaros

#FUNÇÕES PASSARO-POST

def adiciona_post_menciona_passaro(conn, id_passaro, id_post):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post_passaro (Passaros_idPassaros, Post_idPost, Ativo) VALUES (%s,%s,%s)', (id_passaro, id_post,"True"))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir passaro id {id_passaro} e post id {id_post} na tabela post_passaro')

def acha_mencao_de_passaro_em_post(conn, id_post, id_passaro):
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM post_passaro WHERE (Post_idPost=%s) AND (Passaros_idPassaros=%s)', (id_post,id_passaro))
            res = cursor.fetchone()
            if res:
                return res[0]
            else:
                return None

def lista_passaros_mencionados_em_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Passaros_idPassaros FROM post_passaro WHERE Post_idPost=%s', id_post)
        res = cursor.fetchall()
        Passaros = tuple(x[0] for x in res)
        return Passaros

def lista_posts_mencionam_passaro(conn,id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Post_idPost FROM Post_Passaro WHERE Passaros_idPassaros=%s', (id_passaro))
        res = cursor.fetchall()
        Posts = tuple(x[0] for x in res)
        return Posts

def lista_posts_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Post_Passaro')
        res = cursor.fetchall()
        return res

#FUNCÕES USUARIO-MENCIONA-USUARIO-EM-POST

def adiciona_post_menciona_usuario(conn, user, post):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO user_mencao_post (User_idUser, Post_idPost, Ativo) VALUES (%s,%s,%s)', (user, post,"True"))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir usuario id {user} e post id {post} na tabela user_mencao_post')

def acha_mencao_de_usuario_em_post(conn, user, post):
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM user_mencao_post WHERE (Post_idPost=%s) AND (User_idUser=%s)', (post,user))
            res = cursor.fetchone()
            if res:
                return res[0]
            else:
                return None    

def lista_usuarios_mencionados_em_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT User_idUser FROM user_mencao_post WHERE Post_idPost=%s', id_post)
        res = cursor.fetchall()
        Users = tuple(x[0] for x in res)
        return Users

def lista_posts_que_mencionam_usuario(conn, id_user):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Post_idPost FROM user_mencao_post WHERE User_idUser=%s', id_user)
        res = cursor.fetchall()
        Posts = tuple(x[0] for x in res)
        return Posts
#FUNCÕES USUARIO-VIZUALIZA-POST

def adiciona_vizualizacao_em_post(conn, user, post, ip = None, Browser = None, Aparelho = None, Timestamp = None):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Post_visualizar_User (User_idUser, Post_idPost, IP, Browser, Aparelho, TimeStamp, Ativo) VALUES (%s,%s,%s,%s,%s,%s,%s)', (user, post, ip, Browser, Aparelho, Timestamp,"True"))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir a vizualizção de {user} em {post} na tabela post_vizualizar_user')

def acha_vizualizacao_de_post(conn, user, post):
        with conn.cursor() as cursor:
            cursor.execute('SELECT idView FROM Post_visualizar_User WHERE (Post_idPost=%s) AND (User_idUser=%s)', (post,user))
            res = cursor.fetchone()
            if res:
                return res[0]
            else:
                return None    

def lista_vizualizacoes_em_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT User_idUser FROM Post_visualizar_User WHERE Post_idPost=%s', id_post)
        res = cursor.fetchall()
        Users = tuple(x[0] for x in res)
        return Users

def lista_vizualizacoes_de_usuario(conn, id_user):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Post_idPost FROM Post_visualizar_User WHERE User_idUser=%s', id_user)
        res = cursor.fetchall()
        Posts = tuple(x[0] for x in res)
        return Posts