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

    def test_adiciona_usuario(self): #O teste da adição de cidade também é feito aqui pois elas só são adicionadas quando se adiciona um novo usuário
        conn = self.__class__.connection

        nome = "Joao"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome, email, cidade)

        # Checa se o usuário existe.
        id = acha_usuario(conn, nome)
        self.assertIsNotNone(id)

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
        id = acha_usuario(conn, 'Carlos')

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id,))

        remove_usuario(conn, id)

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

    def test_adiciona_passaro_favorito(self):
        conn = self.__class__.connection

        # Adiciona um usuário.
        nome = "João"
        email = "Joao@Joao.br"
        cidade = "Sao Paulo"
        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        # Adiciona um pássaro.
        adiciona_passaro(conn, "PiuPiu")



        # Adiciona um pássaro favorito para o usuario
        adiciona_passaro_favorito(conn, id,"PiuPiu")

        # Checa se o Passaro foi adicionado.
        fav = acha_passaro_favoritos(conn, id,"PiuPiu")
        self.assertIsNotNone(id)

        # Tenta achar um pássaro nao adicionado.
        id = acha_passaro_favoritos(conn, id, "Pica-Pau")
        self.assertIsNone(id)

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


        # Adiciona pássaros favorito
        for passaro in ("Tico-tico", "Marreco", "Pato"):
            adiciona_passaro_favorito(conn, id,  passaro)

        # Checa se os Passaros favoritos existem.
        res = lista_passaros_favoritos(conn, id)
        for i in lista:
            self.assertCountEqual(i, res)

        # Remove os passaros.
        for u in passaros_id:
            remove_passaro(conn, u)

        # Verifica que todos os passaros foram removidos.
        res = lista_passaros(conn)
        self.assertFalse(res)

    # def test_adiciona_perigo(self):
    #     conn = self.__class__.connection
    #
    #     perigo = 'esotérico'
    #
    #     # Adiciona um perigo não existente.
    #     adiciona_perigo(conn, perigo)
    #
    #     # Tenta adicionar o mesmo perigo duas vezes.
    #     try:
    #         adiciona_perigo(conn, perigo)
    #         self.fail('Nao deveria ter adicionado o mesmo perigo duas vezes.')
    #     except ValueError as e:
    #         pass
    #
    #     # Checa se o perigo existe.
    #     id = acha_perigo(conn, perigo)
    #     self.assertIsNotNone(id)
    #
    #     # Tenta achar um perigo inexistente.
    #     id = acha_perigo(conn, 'político')
    #     self.assertIsNone(id)
    #
    # def test_remove_perigo(self):
    #     conn = self.__class__.connection
    #     adiciona_perigo(conn, 'astral')
    #     id = acha_perigo(conn, 'astral')
    #
    #     res = lista_perigos(conn)
    #     self.assertCountEqual(res, (id,))
    #
    #     remove_perigo(conn, id)
    #
    #     res = lista_perigos(conn)
    #     self.assertFalse(res)
    #
    # def test_muda_nome_perigo(self):
    #     conn = self.__class__.connection
    #
    #     adiciona_perigo(conn, 'ecológico')
    #
    #     adiciona_perigo(conn, 'climático')
    #     id = acha_perigo(conn, 'climático')
    #
    #     # Tenta mudar nome para algum nome já existente.
    #     try:
    #         muda_nome_perigo(conn, id, 'ecológico')
    #         self.fail('Não deveria ter mudado o nome.')
    #     except ValueError as e:
    #         pass
    #
    #     # Tenta mudar nome para nome inexistente.
    #     muda_nome_perigo(conn, id, 'apocalíptico')
    #
    #     # Verifica se mudou.
    #     id_novo = acha_perigo(conn, 'apocalíptico')
    #     self.assertEqual(id, id_novo)
    #
    # def test_lista_perigos(self):
    #     conn = self.__class__.connection
    #
    #     # Verifica que ainda não tem perigos no sistema.
    #     res = lista_perigos(conn)
    #     self.assertFalse(res)
    #
    #     # Adiciona alguns perigos.
    #     perigos_id = []
    #     for p in ('nuclear', 'moral', 'emocional'):
    #         adiciona_perigo(conn, p)
    #         perigos_id.append(acha_perigo(conn, p))
    #
    #     # Verifica se os perigos foram adicionados corretamente.
    #     res = lista_perigos(conn)
    #     self.assertCountEqual(res, perigos_id)
    #
    #     # Remove os perigos.
    #     for p in perigos_id:
    #         remove_perigo(conn, p)
    #
    #     # Verifica que todos os perigos foram removidos.
    #     res = lista_perigos(conn)
    #     self.assertFalse(res)
    #
    # def test_adiciona_comida(self):
    #     conn = self.__class__.connection
    #
    #     comida = 'coxinha'
    #
    #     # Adiciona comida não existente.
    #     adiciona_comida(conn, comida)
    #
    #     # Tenta adicionar a mesma comida duas vezes.
    #     try:
    #         adiciona_comida(conn, comida)
    #         self.fail('Nao deveria ter adicionado a mesma comida duas vezes.')
    #     except ValueError as e:
    #         pass
    #
    #     # Checa se a comida existe.
    #     id = acha_comida(conn, comida)
    #     self.assertIsNotNone(id)
    #
    #     # Tenta achar uma comida inexistente.
    #     id = acha_comida(conn, 'esfiha')
    #     self.assertIsNone(id)
    #
    # def test_remove_comida(self):
    #     conn = self.__class__.connection
    #     adiciona_comida(conn, 'coxinha')
    #     id = acha_comida(conn, 'coxinha')
    #
    #     res = lista_comidas(conn)
    #     self.assertCountEqual(res, (id,))
    #
    #     remove_comida(conn, id)
    #
    #     res = lista_comidas(conn)
    #     self.assertFalse(res)
    #
    # def test_muda_nome_comida(self):
    #     conn = self.__class__.connection
    #
    #     adiciona_comida(conn, 'alface')
    #     adiciona_comida(conn, 'tomate')
    #     id = acha_comida(conn, 'tomate')
    #
    #     # Tenta mudar nome para algum nome já existente.
    #     try:
    #         muda_nome_comida(conn, id, 'alface')
    #         self.fail('Não deveria ter mudado o nome.')
    #     except ValueError as e:
    #         pass
    #
    #     # Tenta mudar nome para nome inexistente.
    #     muda_nome_comida(conn, id, 'azeitona')
    #
    # def test_lista_comidas(self):
    #     conn = self.__class__.connection
    #
    #     # Verifica que ainda não tem comidas no sistema.
    #     res = lista_comidas(conn)
    #     self.assertFalse(res)
    #
    #     # Adiciona algumas comidas.
    #     comidas_id = []
    #     for p in ('abacaxi', 'tomate', 'cebola'):
    #         adiciona_comida(conn, p)
    #         comidas_id.append(acha_comida(conn, p))
    #
    #     # Verifica se as comidas foram adicionadas corretamente.
    #     res = lista_comidas(conn)
    #     self.assertCountEqual(res, comidas_id)
    #
    #     # Remove as comidas.
    #     for c in comidas_id:
    #         remove_comida(conn, c)
    #
    #     # Verifica que todos as comidas foram removidas.
    #     res = lista_comidas(conn)
    #     self.assertFalse(res)
    #
    # #@unittest.skip('Em desenvolvimento.')
    # def test_adiciona_perigo_a_comida(self):
    #     conn = self.__class__.connection
    #
    #     # Cria algumas comidas.
    #     adiciona_comida(conn, 'coxinha')
    #     id_coxinha = acha_comida(conn, 'coxinha')
    #
    #     adiciona_comida(conn, 'kibe')
    #     id_kibe = acha_comida(conn, 'kibe')
    #
    #     # Cria alguns perigos.
    #     adiciona_perigo(conn, 'estomacal')
    #     id_estomacal = acha_perigo(conn, 'estomacal')
    #
    #     adiciona_perigo(conn, 'moral')
    #     id_moral = acha_perigo(conn, 'moral')
    #
    #     adiciona_perigo(conn, 'emocional')
    #     id_emocional = acha_perigo(conn, 'emocional')
    #
    #     adiciona_perigo(conn, 'viral')
    #     id_viral = acha_perigo(conn, 'viral')
    #
    #     # Conecta comidas e perigos.
    #     adiciona_perigo_a_comida(conn, id_estomacal, id_coxinha)
    #     adiciona_perigo_a_comida(conn, id_estomacal, id_kibe)
    #     adiciona_perigo_a_comida(conn, id_viral, id_coxinha)
    #     adiciona_perigo_a_comida(conn, id_viral, id_kibe)
    #     adiciona_perigo_a_comida(conn, id_moral, id_coxinha)
    #     adiciona_perigo_a_comida(conn, id_emocional, id_kibe)
    #
    #     res = lista_comidas_de_perigo(conn, id_estomacal)
    #     self.assertCountEqual(res, (id_coxinha, id_kibe))
    #
    #     res = lista_comidas_de_perigo(conn, id_viral)
    #     self.assertCountEqual(res, (id_coxinha, id_kibe))
    #
    #     res = lista_comidas_de_perigo(conn, id_moral)
    #     self.assertCountEqual(res, (id_coxinha,))
    #
    #     res = lista_comidas_de_perigo(conn, id_emocional)
    #     self.assertCountEqual(res, (id_kibe,))
    #
    #     res = lista_perigos_de_comida(conn, id_coxinha)
    #     self.assertCountEqual(res, (id_estomacal, id_viral, id_moral))
    #
    #     res = lista_perigos_de_comida(conn, id_kibe)
    #     self.assertCountEqual(res, (id_estomacal, id_viral, id_emocional))
    #
    #     # Testa se a remoção de uma comida causa a remoção das relações entre essa comida e seus perigos.
    #     remove_comida(conn, id_kibe)
    #
    #     res = lista_comidas_de_perigo(conn, id_estomacal)
    #     self.assertCountEqual(res, (id_coxinha,))
    #
    #     res = lista_comidas_de_perigo(conn, id_viral)
    #     self.assertCountEqual(res, (id_coxinha,))
    #
    #     res = lista_comidas_de_perigo(conn, id_emocional)
    #     self.assertFalse(res)
    #
    #     # Testa se a remoção de um perigo causa a remoção das relações entre esse perigo e suas comidas.
    #     remove_perigo(conn, id_viral)
    #
    #     res = lista_perigos_de_comida(conn, id_coxinha)
    #     self.assertCountEqual(res, (id_estomacal, id_moral))
    #
    #     # Testa a remoção específica de uma relação comida-perigo.
    #     remove_perigo_de_comida(conn, id_estomacal, id_coxinha)
    #
    #     res = lista_perigos_de_comida(conn, id_coxinha)
    #     self.assertCountEqual(res, (id_moral,))

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
