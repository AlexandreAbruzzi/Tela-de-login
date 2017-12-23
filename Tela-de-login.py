#!/usr/bin/env python3.5
#-*- coding: utf-8 -*-
"""
    @author: Hiago dos Santos (hiagop22@gmail.com)

    Tela de login com opção de entrar e de criar novo usuário, sendo que
    os usuários cadastrados são armazenados em um arquivo database.
"""
import shelve
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
except:
    print('Não foi possível importar o módulo tkinter')
    exit(1)

USUARIO_EM_BRANCO = 4
USUARIO_NAO_CADASTRADO = 1
SENHA_INVALIDA = 2
USUARIO_CADASTRADO_E_SENHA_CORRETA = 3
ERRO = 0
ARQUIVO = 'pessoas.db'
COR_DE_FUNDO = '#FFFFFF'
REMEMBER_USER_DESATIVADO = 0
REMEMBER_USER_ATIVADO = 1

class Pessoa(object):
    """docstring for Pessoa"""
    def __init__(self, user = '', password = ''):
        self.user = user
        self.__password = password

class ArquivoDbm(object):
    """docstring for ArqDbm"""
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def verifica_usuario(self, user = '', password = ''):
        """verifica se o usuário e senha, passados como argumentos, estão no arquivo dbm"""
        try:
            with shelve.open(self.arquivo) as p_db:
                if user == '':
                    return USUARIO_EM_BRANCO
                else:
                    if not user in p_db:
                        return USUARIO_NAO_CADASTRADO
                    else:
                        if p_db[user] != password:
                            return SENHA_INVALIDA
                        else:
                            return USUARIO_CADASTRADO_E_SENHA_CORRETA
        except :
            print('Ocorreu um erro inesperado...')
            return ERRO

    def insere_usuario(self, user = '', password = ''):
        """insere um novo usuário com sua senha no arquivo dbm"""
        try:
            with shelve.open(self.arquivo) as p_db:
                p_db[user] = password
        except :
            print('Ocorreu um erro inesperado...')
            return ERRO

    def insere_ultimo_usuario_no_arq(self, ultimo_acesso = 'n', user = '', password = ''):
        """
        insere uma lista no arquivo dbm com o usuário e senha,
        e que representa o último acesso realizado. Caso o Check button
        esteja ativado
        """
        lista_de_ultimo_acesso = [ultimo_acesso, user, password]
        try:
            with shelve.open(self.arquivo) as p_db:
                p_db['ultimo_acesso'] = lista_de_ultimo_acesso
        except :
            print('Ocorreu um erro inesperado...1')
            exit(1)

    def devolve_ult_acesso(self):
        lista_de_ultimo_acesso = []
        try:
            with shelve.open(self.arquivo) as p_db:
                if 'ultimo_acesso' in p_db:
                    lista_de_ultimo_acesso = p_db['ultimo_acesso']
                    return lista_de_ultimo_acesso[0], lista_de_ultimo_acesso[1], lista_de_ultimo_acesso[2]
                else:
                    return 'n', '', ''
        except :
            print('Ocorreu um erro inesperado...2')
            exit(1)

class Login(object):
    """docstring for Login"""
    def __init__(self, instancia):
        self.fonte = ('Trebuchet MS', '15') #, 'bold' )

        #Frames do programa
        self.frame0 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame1 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame2 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame3 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame4 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame5 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame6 = Frame(instancia, bg = COR_DE_FUNDO)
        self.frame7 = Frame(instancia, bg = COR_DE_FUNDO)

        #Subframe que contém os botões de entrar e criar usuário
        self.subframe = Frame(self.frame7, bg = COR_DE_FUNDO)

        #Empacotando as frames
        self.frame0.pack()
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack()
        self.frame6.pack()
        self.frame7.pack()
        self.subframe.pack()

        #Inserindo imagem de logo no programa
        logo = PhotoImage(file = 'images/logo2.gif')
        self.logo = Label(self.frame0)
        self.logo['image'] = logo
        self.logo.image = logo
        self.logo['bg'] = COR_DE_FUNDO
        self.logo.pack()

        #Texto que pede o nome de usuário
        self.user = Label(self.frame1, bg = COR_DE_FUNDO, font = self.fonte)
        self.user.pack()

        #Entrada do nome de usuário
        self.user_received = Entry(self.frame2)
        self.user_received.pack()

        #Texto de que pede a senha
        self.password = Label(self.frame3, bg = COR_DE_FUNDO, font = self.fonte)
        self.password.pack()

        #Entrada da senha
        self.__password_received = Entry(self.frame4, show = '*')
        self.__password_received.pack()

        #Texto com as informaçẽs de a respeito da validação do usuário
        self.info = Label(self.frame5, pady = 10, bg = COR_DE_FUNDO)
        self.info.pack()

        #Checkbutton para lembrar do usuário
        self.lembrar_usuario = IntVar()
        self.remember_user = Checkbutton(self.frame6, text = 'Lembrar usuário', bg = COR_DE_FUNDO, highlightbackground = COR_DE_FUNDO)
        self.remember_user['activebackground'] = COR_DE_FUNDO
        self.remember_user['pady'] = 10
        self.remember_user['offvalue'] = REMEMBER_USER_DESATIVADO
        self.remember_user['onvalue'] = REMEMBER_USER_ATIVADO
        self.remember_user['variable'] = self.lembrar_usuario
        self.remember_user['highlightthickness'] = -1 #Retirando a borda ao redor do Checkbutton
        self.remember_user.pack()

        #Botões para entrar ou criar novo usuário
        self.enter = Button(self.subframe, width = 7)
        self.enter.pack(side = 'left')
        self.create = Button(self.subframe, width = 7)
        self.create.pack(side = 'right')

        self.arq_dbm = ArquivoDbm(ARQUIVO)
        self.pessoa = Pessoa()
        self.acessar_ult = ''   #variável auxiliar que vai ler do arquivo dbm o caractere 's'(acessar último) ou 'n' (não acessar último user)

        self.sign_in()

    def sign_in(self):
        #Limpando Entry de user_received e password_received
        self.user_received.delete(0, END)
        self.__password_received.delete(0, END)

        #Verifica se o último usuário que fez login desejou que lembrasse do nome de usuário e senha dela
        self.acessar_ult, self.pessoa.user, self.pessoa.__password = self.arq_dbm.devolve_ult_acesso()

        #Se tiver desejado que lembrasse então atribui suas informações aos widgets: user_received e password_reecived
        if self.lembrar_usuario.get() == REMEMBER_USER_ATIVADO or self.acessar_ult == 's':
            self.user_received.insert(END, self.pessoa.user)
            self.__password_received.insert(END, self.pessoa.__password)
            self.remember_user.select()

        self.user['text'] = 'Usuário'
        self.user['fg'] = 'black'

        self.password['text'] ='Senha'
        self.password['fg'] = 'black'

        self.info['text'] = ''
        self.info['fg'] = 'red'

        #Configurando os Buttons de 'ENTRAR' e 'CRIAR'(novo usuário)
        self.enter['text'] = 'ENTRAR'
        self.enter['command'] = self.__verificar
        self.create['text'] = 'NOVO'
        self.create['fg'] = 'black'
        self.create['bg'] = self.enter['bg']
        self.create['command'] = self.create_user

    def create_user(self):
        #Limpando Entry de user_received e password_received
        self.user_received.delete(0, END)
        self.__password_received.delete(0, END)

        self.user['text'] = 'Nome de Usuário'
        self.user['fg'] = 'green'

        self.password['fg'] = 'green'

        self.enter['command'] = self.sign_in

        self.info['text'] = ''
        self.info['fg'] = 'red'

        self.create['text'] = 'CRIAR'
        self.create['fg'] = 'white'
        self.create['bg'] = 'black'
        self.create['command'] = self.__inserir

    def __inserir(self):
        """Insere os dados no novo usuário, mas antes fazendo as devidas validações dos dados"""
        self.pessoa.user = self.user_received.get().lower()
        self.pessoa.__password = self.__password_received.get()

        if self.pessoa.user == '' and self.pessoa.__password != '':
            self.info['text'] = 'Usuário não pode ficar em branco'
        else:
            if self.pessoa.user != '' and self.pessoa.__password == '':
                self.info['text'] = 'Senha não pode ficar em branco'
            else:
                if self.pessoa.user == '' and self.pessoa.__password == '':
                    self.info['text'] = 'Usuário e senha não podem ficar em branco'
                else:
                    if self.arq_dbm.verifica_usuario(self.pessoa.user) == USUARIO_NAO_CADASTRADO:
                        self.arq_dbm.insere_usuario(self.pessoa.user, self.pessoa.__password)
                        if self.lembrar_usuario.get() == REMEMBER_USER_ATIVADO:
                            self.arq_dbm.insere_ultimo_usuario_no_arq('s', pessoa.user, pessoa.__password)
                        else:
                            self.arq_dbm.insere_ultimo_usuario_no_arq('n', pessoa.user, pessoa.__password)
                        self.sign_in()
                    else:
                        self.info['text'] = 'Usuário já cadastrado'

    def __verificar(self):
        """Verifica se o nome de usuário e senha estão corretos e se deseja que lembre desses dados"""
        self.pessoa.user = self.user_received.get().lower()
        self.pessoa.__password = self.__password_received.get()

        #Valida suas informações de login no arquivo que os tem guardados
        resultado = self.arq_dbm.verifica_usuario(self.pessoa.user, self.pessoa.__password)
        if resultado == USUARIO_EM_BRANCO:
            self.info['text'] = 'Usuário não pode ficar em branco'
            self.info['fg'] = 'red'
        else:
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
                        if self.lembrar_usuario.get() == REMEMBER_USER_ATIVADO:
                            self.arq_dbm.insere_ultimo_usuario_no_arq('s', self.pessoa.user, self.pessoa.__password)
                        else:
                            self.arq_dbm.insere_ultimo_usuario_no_arq('n', self.pessoa.user, self.pessoa.__password)
                    else:
                        if resultado == ERRO:
                            exit(1)

instancia = Tk()
instancia.title('Login')
instancia['bg'] = COR_DE_FUNDO

Login(instancia)

instancia.mainloop()