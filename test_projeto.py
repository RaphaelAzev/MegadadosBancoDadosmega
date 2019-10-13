import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='mydb'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

   #USER

    def test_adiciona_usuario(self): 
        
        conn = self.__class__.connection

        nome = "Joao"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome, email, cidade)

        # Checa se o usuário existe.
        id = acha_usuario(conn, nome)
        self.assertIsNotNone(id)

        #O teste da adição de cidade também é feito aqui pois elas só são adicionadas quando se adiciona um novo usuário
        #Checa se a cidade foi adicionadas
        id = acha_cidade(conn, 'Sao Paulo')
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_usuario(conn, 'Maria')
        self.assertIsNone(id)

        #Tenta achar uma cidade inexistente
        id = acha_cidade(conn, 'Campinas')
        self.assertIsNone(id)

    def test_remove_usuario(self):
        conn = self.__class__.connection
        c = "Sao Paulo"
        adiciona_usuario(conn, 'Carlos',"Carlos@Carlos.br",c)
        id_user = acha_usuario(conn, 'Carlos')

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id_user,))

        remove_usuario(conn, id_user)

        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_muda_nome_usuario(self):
        conn = self.__class__.connection
        c = "Sao Paulo"
        adiciona_usuario(conn, 'José',"José@José.br",c)

        adiciona_usuario(conn, 'Amdré',"Carlos@Carlos.br",c)
        id = acha_usuario(conn, 'Amdré')

        # Tenta mudar nome
        muda_nome_usuario(conn, id, 'André')

        # Verifica se mudou.
        id_novo = acha_usuario(conn, 'André')
        self.assertEqual(id, id_novo)

    def test_lista_usuarios(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem usuarios no sistema.
        res = lista_usuarios(conn)
        self.assertFalse(res)

        # Adiciona alguns usuarios.
        usuarios_id = []
        email = "email@email.br"
        cidade = "Sao Paulo"
        for u in ('Mario', 'Luigi', 'Vitor'):
            adiciona_usuario(conn, u,email,cidade)
            usuarios_id.append(acha_usuario(conn, u))

        # Verifica se os usuarios foram adicionados corretamente.
        res = lista_usuarios(conn)
        self.assertCountEqual(res, usuarios_id)

        # Remove os usuarios.
        for u in usuarios_id:
            remove_usuario(conn, u)

        # Verifica que todos os usuarios foram removidos.
        res = lista_usuarios(conn)
        self.assertFalse(res)

   #PASSARO

    def test_adiciona_passaro(self):
        conn = self.__class__.connection

        # Adiciona um pássaro não existente.
        adiciona_passaro(conn, "PiuPiu")

        # Checa se o Passaro existe.
        id = acha_passaro(conn, "PiuPiu")
        self.assertIsNotNone(id)

        # Tenta achar um pássaro inexistente.
        id = acha_passaro(conn, 'Pica-Pau')
        self.assertIsNone(id)

    def test_lista_passaros(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros(conn)
        self.assertFalse(res)

        # Adiciona alguns passaros.
        passaros_id = []

        for u in ('Chitao', 'Xororo', 'Tico-Tico'):
            adiciona_passaro(conn, u)
            passaros_id.append(acha_passaro(conn, u))

        # Verifica se os passaros foram adicionados corretamente.
        res = lista_passaros(conn)
        self.assertCountEqual(res, passaros_id)

        # Remove os passaros.
        for u in passaros_id:
            remove_passaro(conn, u)

        # Verifica que todos os passaros foram removidos.
        res = lista_passaros(conn)
        self.assertFalse(res)

    def test_remove_passaro(self):
        conn = self.__class__.connection
        adiciona_passaro(conn, 'Gato')
        id = acha_passaro(conn, 'Gato')

        res = lista_passaros(conn)
        self.assertCountEqual(res, (id,))

        remove_passaro(conn, id)

        res = lista_passaros(conn)
        self.assertFalse(res)

   #POST

    def test_adiciona_post(self):

        conn = self.__class__.connection


        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        # Adiciona Posts feitos por Jõao
        adiciona_post(conn,  id, "Comidas")
        #adiciona_post(conn, "Coisas", "Roda e Corda", id)

       
        # Checa se o Post existe.
        id = acha_post_portitulo(conn, "Comidas")
        self.assertIsNotNone(id)

        # Tenta achar post inexistente.
        id = acha_post_portitulo(conn, "Não Comidas")
        self.assertIsNone(id)
        
        id = acha_post_portitulo(conn, "Comidas")
        self.assertEqual(acha_post_porid(conn, id), "Comidas")

        
        
        #self.assertEqual(acha_post_porid(conn, 2), "Coisas")  

    def test_remove_post(self):
        conn = self.__class__.connection
        
        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        # Adiciona Post
        adiciona_post(conn, id, "Comidas")
        id = acha_post_portitulo(conn, "Comidas")
        # Remove e checa se ocorreu o delete lógico
        remove_post(conn, id)
        self.assertEqual(status_post(conn, id), "False")

    def test_edita_post_URL(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        # Adiciona Post
        adiciona_post(conn, id, "Comidas")

        #Checa se URL é valor padrao None
        res = lista_posts(conn)
        self.assertEqual(res[0][2], None)

        idpost = acha_post_portitulo(conn, "Comidas")

        edita_post_URL(conn, idpost, "ThisIsImage")

        res = lista_posts(conn)
        self.assertEqual(res[0][2], "ThisIsImage")
        
    def test_lista_posts(self):
        conn = self.__class__.connection

        #Adiciona o famigerado Joao
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        idjoao = acha_usuario(conn, nome)

        # Verifica que ainda não tem posts no sistema.
        res = lista_posts(conn)
        self.assertFalse(res)

        lista = []
        # Adiciona alguns posts
        for u in ('Serta', 'Funk', 'SertaFunk'):
            adiciona_post(conn, idjoao, u )
            lista.append("oi")

        # Verifica se tem a mesma quantidade de posts entre a lista e o banco
        res = lista_posts(conn)
        self.assertEqual(len(res), len(lista))

        # Remove os passaros.
        for u in ('Serta', 'Funk', 'SertaFunk'):
            idpost = acha_post_portitulo(conn, u)
            remove_post(conn, idpost)

        # Verifica que todos os posts foram removidos.
        res = lista_posts(conn)
        self.assertEqual(len(res), 0)

    def test_lista_posts_usuario(self):
        conn = self.__class__.connection

        #Adiciona o famigerado Joao
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        idjoao = acha_usuario(conn, nome)

        # Verifica que ainda não tem posts do usuario no sistema.
        res = lista_posts_usuario(conn, idjoao)
        self.assertFalse(res)

        lista = []
        # Adiciona alguns posts
        for u in ('Serta', 'Funk', 'SertaFunk'):
            adiciona_post(conn,idjoao,u, "oi")
            lista.append("oi")

        # Verifica se tem a mesma quantidade de posts entre a lista e o banco
        res = lista_posts_usuario(conn, idjoao)
        self.assertEqual(len(res), len(lista))

        # Remove os passaros.
        for u in ('Serta', 'Funk', 'SertaFunk'):
            idpost = acha_post_portitulo(conn, u)
            remove_post(conn, idpost)

        # Verifica que todos os posts foram removidos.
        res = lista_posts_usuario(conn, idjoao)
        self.assertEqual(len(res), 0)

    def test_edita_post_titulo(self):
        conn = self.__class__.connection

        #Adiciona o famigerado Joao
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        idjoao = acha_usuario(conn, nome)

        # Adiciona post
        adiciona_post(conn,  idjoao,"Poster")
        idpost = acha_post_portitulo(conn, "Poster")
        
        #Edita o post
        edita_post_titulo(conn, idpost, "Poster2.0")

        #Tenta achar o post com o titulo novo
        idpost = acha_post_portitulo(conn, "Poster2.0")
        self.assertEqual(acha_post_porid(conn, idpost), "Poster2.0")

    def test_edita_post_texto(self):
        conn = self.__class__.connection

        #Adiciona o famigerado Joao
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        idjoao = acha_usuario(conn, nome)

        # Adiciona post
        adiciona_post(conn, idjoao, "Poster","oi")
        idpost = acha_post_portitulo(conn, "Poster")
        
        #Edita o post
        edita_post_texto(conn, idpost, "Olagangnam")

        #Tenta achar o post com o texto novo
        res = lista_posts(conn)
        #raise ValueError(f'{res}')
        self.assertEqual(res[0][3], "Olagangnam")

   #PASSARO-USER

    def test_adiciona_passaro_favorito(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        # Adiciona um pássaro.
        adiciona_passaro(conn, "Piu Piu")



        # Adiciona um pássaro favorito para o usuario
        adiciona_passaro_favorito(conn, id,"Piu Piu")

        # Checa se o Passaro foi adicionado.
        fav = acha_passaro_favoritos(conn, id,"Piu Piu")
        self.assertIsNotNone(fav)

        # Tenta achar um pássaro nao adicionado.
        id = acha_passaro_favoritos(conn, id, "Pica-Pau")
        self.assertIsNone(id)

    def test_remove_passaro_user(self):
        conn = self.__class__.connection
        c = "Sao Paulo"
        adiciona_usuario(conn, 'Carlos',"Carlos@Carlos.br",c)
        id_user = acha_usuario(conn, 'Carlos')
        
        # Adiciona um pássaro não existente.
        adiciona_passaro(conn, "PiuPiu")

        # Adiciona um pássaro favorito para o usuario
        adiciona_passaro_favorito(conn, id_user,"Piu Piu")

        res = lista_passaros_favoritos(conn,id_user)
        self.assertCountEqual(res, (acha_passaro_favoritos(conn, id_user, "Piu Piu"),))

        remove_passaro_favorito(conn, id_user,"Piu Piu")

        res = lista_passaros_favoritos(conn,id_user)
        self.assertFalse(res)

    def test_lista_passaro_user(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)


        # Adiciona pássaros.
        adiciona_passaro(conn, "Tico-tico")
        adiciona_passaro(conn, "Marreco")
        adiciona_passaro(conn, "Pato")


        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros_favoritos(conn, id)
        self.assertFalse(res)

        lista = []
        # Adiciona pássaros favorito
        for passaro in ("Tico-tico", "Marreco", "Pato"):
            adiciona_passaro_favorito(conn, id,  passaro)
            lista.append(acha_passaro(conn, passaro))

        # Checa se os Passaros favoritos existem.
        res = lista_passaros_favoritos(conn, id)
        self.assertCountEqual(lista, res)

        # Remove os passaros.
        for u in lista:
            remove_passaro(conn, u)

        # Verifica que todos os passaros foram removidos.
        res = lista_passaros_favoritos(conn,id)
        self.assertFalse(res)

   #POST-PASSSARO

    def test_adiciona_post_mensiona_passaro(self):
        conn = self.__class__.connection
        
        # Adiciona um pássaro.
        adiciona_passaro(conn, "PiuPiu")

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user = acha_usuario(conn, nome)

        # Adiciona Post feitos por Jõao
        adiciona_post(conn, id_user,"Cartoons", "Gosto de frajola e #PiuPiu")

        adiciona_post_menciona_passaro(conn, acha_passaro(conn, "PiuPiu"), acha_post_portitulo(conn,"Cartoons"))
        

        # Checa se o Passaro existe.
        teste = acha_mencao_de_passaro_em_post(conn,acha_post_portitulo(conn,"Cartoons"), acha_passaro(conn, "PiuPiu"))
        self.assertIsNotNone(teste)

        # Tenta achar um pássaro inexistente.
        teste = acha_mencao_de_passaro_em_post(conn,acha_post_portitulo(conn,"Sitcon"), acha_passaro(conn, "Pinguin"))
        self.assertIsNone(teste)

    def test_lista_mencoes_de_passaros_em_post(self):
        conn = self.__class__.connection
        


        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user = acha_usuario(conn, nome)

        # Adiciona pássaros.
        adiciona_passaro(conn, "Tico-tico")
        adiciona_passaro(conn, "Marreco")
        adiciona_passaro(conn, "Pato")

        # Adiciona posts
        adiciona_post(conn, id_user, "Ex1", "#Pato, #Marreco, #Tico-tico")
        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros_mencionados_em_post(conn, acha_post_portitulo(conn, "Ex1"))
        self.assertFalse(res)
        lista = []
        
        for p in ("Tico-tico", "Marreco", "Pato"):
            adiciona_post_menciona_passaro(conn, acha_passaro(conn, p),  acha_post_portitulo(conn, "Ex1"))
            lista.append(acha_passaro(conn, p))
        
        # Checa se os Passaros mensionados existem.
        res = lista_passaros_mencionados_em_post(conn, acha_post_portitulo(conn, "Ex1"))
        
        self.assertCountEqual(lista, res)        

    def test_lista_posts_que_mensionam_passaro(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        # Adiciona pássaros.
        adiciona_passaro(conn, "Tico-tico")

        # Adiciona postas
        adiciona_post(conn, id, "Ex1", "#Tico-tico")
        adiciona_post(conn, id, "Ex2", "#Tico-tico")
        adiciona_post(conn, id, "Ex3", "#Tico-tico")

        # Verifica que ainda não tem passaros no sistema.
        res = lista_posts_mencionam_passaro(conn, acha_passaro(conn, "Tico-Tico"))
        self.assertFalse(res) 

        lista=[]
        for p in ("Ex1", "Ex2", "Ex3"):
            adiciona_post_menciona_passaro(conn, acha_passaro(conn, "Tico-Tico"),  acha_post_portitulo(conn, p))
            lista.append(acha_post_portitulo(conn, p))
          
        # Checa se os Posts feitos existem.
        res = lista_posts_mencionam_passaro(conn, acha_passaro(conn, "Tico-Tico"))
        self.assertCountEqual(lista, res)
   
   #POST-MENSIONA-USUARIO

    def test_adiciona_post_menciona_usuario(self):
        conn = self.__class__.connection     
        
        # Adiciona dois usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)
        nome = "Maria"
        email = "Maria@Maria.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user2 = acha_usuario(conn, nome)

        #Faz o post
        adiciona_post(conn, id_user1,"Shout", "E ai, @Maria" )

        #Registra o post na tabela de referencias
        adiciona_post_menciona_usuario(conn, id_user2, acha_post_portitulo(conn,"Shout"))

        # Checa se a referencia existe.
        teste = acha_mencao_de_usuario_em_post(conn, id_user2,acha_post_portitulo(conn,"Shout"))
        #raise ValueError(f'{teste}')
        self.assertIsNotNone(teste)

        # Tenta achar uma referencia inexistente.
        teste = acha_mencao_de_usuario_em_post(conn, id_user2,acha_post_portitulo(conn,"Techal"))
        self.assertIsNone(teste)

    def test_lista_usuarios_mencionados_em_post(self):
        conn = self.__class__.connection
        


        # Adiciona um usuários.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)

        nome = "Maria"
        email = "Maria@Maria.br"
        adiciona_usuario(conn, nome, email, cidade)

        nome = "Vitor"
        email = "Vitor@Vitor.br"
        adiciona_usuario(conn, nome, email, cidade)
 
        nome = "Fabio"
        email = "Fabio@Fabio.br"
        adiciona_usuario(conn, nome, email, cidade)


        # Adiciona post
        adiciona_post(conn, id_user1, "Bora pra festa", "@Maria, @Vitor, @Fabio")
        # Verifica que ainda não tem usuarios no sistema.
        res = lista_usuarios_mencionados_em_post(conn, acha_post_portitulo(conn, "Bora pra festa"))
        self.assertFalse(res)
        lista = []
        
        for p in ("Maria", "Vitor", "Fabio"):
            adiciona_post_menciona_usuario(conn, acha_usuario(conn, p),  acha_post_portitulo(conn, "Bora pra festa"))
            lista.append(acha_usuario(conn, p))
        
        # Checa se os usuarios mensionados existem.
        res = lista_usuarios_mencionados_em_post(conn, acha_post_portitulo(conn, "Bora pra festa"))
        
        self.assertCountEqual(lista, res)        
    
    def test_lista_posts_que_mencionam_usuario(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)

        nome = "Maria"
        email = "Maria@Maria.br"
        adiciona_usuario(conn, nome, email, cidade)
        id_user2 = acha_usuario(conn, nome)

        nome = "Vitor"
        email = "Vitor@Vitor.br"
        adiciona_usuario(conn, nome, email, cidade)
        id_user3 = acha_usuario(conn, nome)

        nome = "Fabio"
        email = "Fabio@Fabio.br"
        adiciona_usuario(conn, nome, email, cidade)
        id_user4 = acha_usuario(conn, nome)


        # Adiciona posts
        adiciona_post(conn, id_user2, "Ex1", "@Joao")
        adiciona_post(conn, id_user3, "Ex2", "@Joao")
        adiciona_post(conn, id_user4, "Ex3", "@Joao")

        # Verifica que ainda não tem usuario no sistema.
        res = lista_posts_que_mencionam_usuario(conn, id_user1)
        self.assertFalse(res) 

        lista=[]
        for p in ("Ex1", "Ex2", "Ex3"):
            adiciona_post_menciona_usuario(conn, acha_usuario(conn, "Joao"),  acha_post_portitulo(conn, p))
            lista.append(acha_post_portitulo(conn, p))
          
        # Checa se os Posts feitos existem.
        res = lista_posts_que_mencionam_usuario(conn, id_user1)
        self.assertCountEqual(lista, res)

   #USUARIO-VIZUALIZA-POST

    def test_adiciona_vizualizacao(self):
        conn = self.__class__.connection     
        
        # Adiciona dois usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)
        nome = "Maria"
        email = "Maria@Maria.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user2 = acha_usuario(conn, nome)

        #Faz o post
        adiciona_post(conn, id_user1,"Post", "Olha que legal!!" )

        #Registra vizualização de maria na tabela de referencias
        adiciona_vizualizacao_em_post(conn, id_user2, acha_post_portitulo(conn, "Post"))

        # Checa se a referencia existe.
        teste = acha_vizualizacao_de_post(conn, id_user2,acha_post_portitulo(conn,"Post"))
        self.assertIsNotNone(teste)

        # Tenta achar uma referencia inexistente.
        teste = acha_vizualizacao_de_post(conn, id_user2,acha_post_portitulo(conn,"Video"))
        self.assertIsNone(teste)

    def test_lista_vizualizacoes_em_post(self):
        conn = self.__class__.connection
        
        # Adiciona um usuários.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)

        nome = "Maria"
        email = "Maria@Maria.br"
        adiciona_usuario(conn, nome, email, cidade)

        nome = "Vitor"
        email = "Vitor@Vitor.br"
        adiciona_usuario(conn, nome, email, cidade)

        nome = "Fabio"
        email = "Fabio@Fabio.br"
        adiciona_usuario(conn, nome, email, cidade)



        # Adiciona post
        adiciona_post(conn, id_user1, "Link da festa", "www.festa.com")

        # Verifica que ainda não tem usuarios no sistema.
        res = lista_vizualizacoes_em_post(conn, acha_post_portitulo(conn, "Link da festa"))
        self.assertFalse(res)

        lista = []
        for p in ("Maria", "Vitor", "Fabio"):
            adiciona_vizualizacao_em_post(conn, acha_usuario(conn, p),  acha_post_portitulo(conn, "Link da festa"))
            lista.append(acha_usuario(conn, p))
        
        # Checa se os usuarios mensionados existem.
        res = lista_vizualizacoes_em_post(conn, acha_post_portitulo(conn, "Link da festa"))
        
        self.assertCountEqual(lista, res)        
    
    def test_lista_vizualizacoes_de_usuario(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)

        nome = "Maria"
        email = "Maria@Maria.br"
        adiciona_usuario(conn, nome, email, cidade)
        id_user2 = acha_usuario(conn, nome)

        nome = "Vitor"
        email = "Vitor@Vitor.br"
        adiciona_usuario(conn, nome, email, cidade)
        id_user3 = acha_usuario(conn, nome)

        nome = "Fabio"
        email = "Fabio@Fabio.br"
        adiciona_usuario(conn, nome, email, cidade)
        id_user4 = acha_usuario(conn, nome)


        # Adiciona posts
        adiciona_post(conn, id_user1, "Ex1", "texto1")
        adiciona_post(conn, id_user2, "Ex2", "texto2")
        adiciona_post(conn, id_user3, "Ex3", "texto3")

        # Verifica que ainda não tem usuario no sistema.
        res = lista_vizualizacoes_de_usuario(conn, id_user4)
        self.assertFalse(res) 

        lista=[]
        for p in ("Ex1", "Ex2", "Ex3"):
            adiciona_vizualizacao_em_post(conn, id_user4,  acha_post_portitulo(conn, p))
            lista.append(acha_post_portitulo(conn, p))
          
        # Checa se os Posts feitos existem.
        res = lista_vizualizacoes_de_usuario(conn, id_user4)
        self.assertCountEqual(lista, res)

   #TRIGGERS 
    def test_trigger_delecao_post_passaro(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id_user1 = acha_usuario(conn, nome)

        # Adiciona Post
        adiciona_post(conn, id_user1, "Ex1", "texto1")
        idpost = acha_post_portitulo(conn, "Ex1")

        # Adiciona Passaro
        adiciona_passaro(conn, "TicoTeco")
        idpassaro = acha_passaro(conn, "TicoTeco")

        #Relaciona o post ao passaro
        adiciona_post_menciona_passaro(conn, idpassaro, idpost)

        remove_post(conn, idpost)
        res = status_post(conn, idpost)
        self.assertEqual(res, "False")

        res = lista_posts_passaros(conn)
        self.assertEqual(res[0][2], "False")




def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'],
                '-u', config['USER'],
                '-p' + config['PASS'],
                '-h', config['HOST']
            ],
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir()
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
 