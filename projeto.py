import pymysql


def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            adiciona_cidade(conn, cidade)
            cursor.execute('INSERT INTO user (Nome,Email,Cidade) VALUES((%s),(%s),(%s))', (nome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela user')

def adiciona_cidade(conn, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT IGNORE INTO cidades (Nome) VALUES (%s)', (cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {cidade} na tabela cidades')

def acha_usuario(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser FROM user WHERE Nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_cidade(conn, cidade):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome FROM cidades WHERE nome = %s', (cidade))
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
            raise ValueError(f'Não posso alterar nome do id {idUser} para {novo_nome} na tabela usuario')

def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM user WHERE idUser=%s', (id))

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idUser from user')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

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

def adiciona_passaro_favorito(conn, id_usuario, passaro):
    with conn.cursor() as cursor:
        adiciona_passaro(conn, passaro)
        id_passaro = acha_passaro(conn, passaro)
        try:
            cursor.execute('INSERT INTO Passaro_User (User_idUser, Passaros_idPassaros) VALUES (%s,%s)', (id_usuario, id_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {passaro} e {usuario} na tabela Passaro_User')

def remove_passaro_favorito(conn, id_usuario, passaro):
    with conn.cursor() as cursor:
        id_passaro = acha_passaro(conn, passaro)
        try:
            cursor.execute('DELETE FROM Passaro_User WHERE (User_idUser=%s) AND (Passaros_idPassaros=%s)', (id_usuario, passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {passaro} e {usuario} na tabela Passaro_User')

def acha_passaro_favoritos(conn, id, passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Passaros_idPassaros FROM Passaro_User WHERE (User_idUser=%s) AND (Passaros_idPassaros=%s)', (id,passaro))
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

# def adiciona_perigo(conn, nome):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('INSERT INTO perigo (nome) VALUES (%s)', (nome))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso inserir {nome} na tabela perigo')
#
# def acha_perigo(conn, nome):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id FROM perigo WHERE nome = %s', (nome))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None
#
# def muda_nome_perigo(conn, id, novo_nome):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE perigo SET nome=%s where id=%s', (novo_nome, id))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela perigo')
#
# def remove_perigo(conn, id):
#     with conn.cursor() as cursor:
#         cursor.execute('DELETE FROM perigo WHERE id=%s', (id))
#
# def lista_perigos(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id from perigo')
#         res = cursor.fetchall()
#         perigos = tuple(x[0] for x in res)
#         return perigos
#
# def adiciona_comida(conn, nome):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('INSERT INTO comida (nome) VALUES (%s)', (nome))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso inserir {nome} na tabela comida')
#
# def acha_comida(conn, nome):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id FROM comida WHERE nome = %s', (nome))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None
#
# def remove_comida(conn, id):
#     with conn.cursor() as cursor:
#         cursor.execute('DELETE FROM comida WHERE id=%s', (id))
#
# def muda_nome_comida(conn, id, novo_nome):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE comida SET nome=%s where id=%s', (novo_nome, id))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela comida')
#
# def lista_comidas(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id from comida')
#         res = cursor.fetchall()
#         comidas = tuple(x[0] for x in res)
#         return comidas
#
# def adiciona_perigo_a_comida(conn, id_perigo, id_comida):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO comida_perigo VALUES (%s, %s)', (id_comida, id_perigo))
#
# def remove_perigo_de_comida(conn, id_perigo, id_comida):
#     with conn.cursor() as cursor:
#         cursor.execute('DELETE FROM comida_perigo WHERE id_perigo=%s AND id_comida=%s',(id_perigo, id_comida))
#
# def lista_comidas_de_perigo(conn, id_perigo):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_comida FROM comida_perigo WHERE id_perigo=%s', (id_perigo))
#         res = cursor.fetchall()
#         comidas = tuple(x[0] for x in res)
#         return comidas
#
# def lista_perigos_de_comida(conn, id_comida):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_perigo FROM comida_perigo WHERE id_comida=%s', (id_comida))
#         res = cursor.fetchall()
#         perigos = tuple(x[0] for x in res)
#         return perigos
