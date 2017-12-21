#   -*- coding: utf-8 -*-
#   @author: Hiago dos Santos (hiagop22@gmail.com)
#
#   Tela de login com opção de entrar e de criar novo usuário, sendo que
#   os usuários cadastrados são armazenados em um arquivo database.

import dbm
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
except:
    print('Não foi possível importar o módulo tkinter')
    exit(1)

USUARIO_NAO_CADASTRADO = 1
SENHA_INVALIDA = 2
USUARIO_CADASTRADO_E_SENHA_CORRETA = 3
ERRO = 0
ARQUIVO = 'pessoas.db'

class Pessoa(object):
    """docstring for Pessoa"""
    def __init__(self, user = '', password = ''):
        self.user = user
        self.password = password

class ArquivoDbm(object):
    """docstring for ArqDbm"""
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def verifica_usuario(self, user, password = ''):
        try:
            with dbm.open(self.arquivo, 'c') as p_db:
                if not user in p_db:
                    return USUARIO_NAO_CADASTRADO
                else:
                    if p_db[user].decode() != password:
                        return SENHA_INVALIDA
                    else:
                        return USUARIO_CADASTRADO_E_SENHA_CORRETA
        except :
            print('Ocorreu um erro inesperado...')
            return ERRO

    def insere_usuario(self, user, password):
        try:
            with dbm.open(self.arquivo, 'c') as p_db:
                p_db[user] = password
        except :
            print('Ocorreu um erro inesperado...')
            return ERRO

class Login(object):
    """docstring for Login"""
    def __init__(self, instancia):
        self.user = Label(instancia)
        self.user.pack()

        self.user_received = Entry(instancia)
        self.user_received.pack()

        self.password = Label(instancia)
        self.password.pack()

        self.password_received = Entry(instancia, show = '*')
        self.password_received.pack()

        self.info = Label(instancia)
        self.info.pack()

        self.enter = Button(instancia)
        self.enter.pack(side = 'left')
        self.create = Button(instancia)
        self.create.pack(side = 'right')

        self.arq_dbm = ArquivoDbm(ARQUIVO)
        self.pessoa = Pessoa()
        self.sign_in()

    def sign_in(self):
        self.user_received.delete(0, len(self.user_received.get()))
        self.password_received.delete(0, len(self.password_received.get()))

        self.user['text'] = 'Usuário'
        self.user['fg'] = 'black'

        self.password['text'] ='Senha'
        self.password['fg'] = 'black'

        self.info['text'] = ''
        self.info['fg'] = 'red'

        self.enter['text'] = 'Entrar'
        self.enter['command'] = self.__verificar
        self.create['text'] = 'Novo'
        self.create['fg'] = 'black'
        self.create['bg'] = self.enter['bg']
        self.create['command'] = self.create_user

    def create_user(self):
        self.user_received.delete(0, len(self.user_received.get()))
        self.password_received.delete(0, len(self.password_received.get()))

        self.user['text'] = 'Nome de Usuário'
        self.user['fg'] = 'green'

        self.password['fg'] = 'green'

        self.enter['command'] = self.sign_in

        self.info['text'] = ''
        self.info['fg'] = 'red'

        self.create['text'] = 'Criar'
        self.create['fg'] = 'white'
        self.create['bg'] = 'black'
        self.create['command'] = self.__inserir

    def __inserir(self):
        self.pessoa.user = self.user_received.get().lower()
        self.pessoa.password = self.password_received.get()

        if self.pessoa.user == '' and self.pessoa.password != '':
            self.info['text'] = 'Usuário não pode ficar em branco'
        else:
            if self.pessoa.user != '' and self.pessoa.password == '':
                self.info['text'] = 'Senha não pode ficar em branco'
            else:
                if self.pessoa.user == '' and self.pessoa.password == '':
                    self.info['text'] = 'Usuário e senha não podem ficar em branco'
                else:
                    if self.arq_dbm.verifica_usuario(self.pessoa.user) == USUARIO_NAO_CADASTRADO:
                        self.arq_dbm.insere_usuario(self.pessoa.user, self.pessoa.password)
                        self.user_received.delete(0, len(self.pessoa.user))
                        self.password_received.delete(0, len(self.pessoa.password))
                        self.sign_in()
                    else:
                        self.info['text'] = 'Usuário já cadastrado'

    def __verificar(self):
        self.pessoa.user = self.user_received.get().lower()
        self.pessoa.password = self.password_received.get()

        resultado = self.arq_dbm.verifica_usuario(self.pessoa.user, self.pessoa.password)
        if resultado == USUARIO_NAO_CADASTRADO:
            self.info['text'] = 'Usuário não cadastrado'
            self.info['fg'] = 'red'
        else:
            if resultado == SENHA_INVALIDA:
                self.info['text'] = 'Senha inválida'
                self.info['fg'] = 'red'
            else:
                if resultado == USUARIO_CADASTRADO_E_SENHA_CORRETA:
                    self.info['text'] = 'Seja bem vindo ' + self.pessoa.user
                    self.info['fg'] = 'blue'
                else:
                    if resultado == ERRO:
                        exit(1)

instancia = Tk()
instancia.title('Login')

Login(instancia)

instancia.mainloop()