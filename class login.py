# IMPORTAÇÃO DE MODULOS.
import tkinter
import shelve


class login(object):

    #INICIA O OBJETO
    def __init__(self, mestre, proxima_tela):

        #INSTANCIA DE TK.
        self.interface = mestre
        self.proxima_tela = proxima_tela

        #ABRE A BASE DE DADOS.
        self.data = shelve.open('data_base')

        # DEFINE OS PARAMETROS DA INSTANCIA DE TK.
        self.interface.title('LOGIN')
        self.interface.geometry("250x260")
        self.interface.resizable(False, False)
        self.interface['bg'] = 'SystemButtonFace'

        # VARIAVEL PARA FUNÇAO LEMBRAR.
        self.setlembrar = tkinter.IntVar(0)

        # CRIA OS FRAMES DA INTERFACE.
        self.nada = tkinter.Label(self.interface, pady=6, text=' ')
        self.frame1 = tkinter.Frame(self.interface)
        self.frame2 = tkinter.Frame(self.interface, pady=4)
        self.frame3 = tkinter.Frame(self.interface)

        #EMPACOTA OS FRAMES DA INTERFACE
        self.nada.pack()
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        #CRIA OS ELEMENTOS DA INTERFACE DE LOGIN.
        self.usuariotxt = tkinter.Label(self.frame1, text='Usuário')
        self.usuarioentry = tkinter.Entry(self.frame1)
        self.senhatxt = tkinter.Label(self.frame1, text='Senha')
        self.senhaentry = tkinter.Entry(self.frame1, show='*')
        self.lembrar = tkinter.Checkbutton(self.frame1, text='Lembrar', variable=self.setlembrar, command=self.lembrar)
        self.mensagem = tkinter.Label(self.frame2)
        self.entrar = tkinter.Button(self.frame3, text='Entrar', command=self.fazer_login, fg='green', padx=15)
        self.novo = tkinter.Button(self.frame3, text='Novo', command=self.mostra_criar, fg='blue', padx=15)

        # CRIA OS ELEMENTOS DA INTERFACE DE CRIAR USUARIO.
        self.nometxt = tkinter.Label(self.frame1, text='Nome')
        self.nomeentry = tkinter.Entry(self.frame1)
        self.emailtxt = tkinter.Label(self.frame1, text='E-mail')
        self.emailentry = tkinter.Entry(self.frame1)
        self.voltar = tkinter.Button(self.frame3, text='Voltar', command=self.mostra_login, padx=15)
        self.criar = tkinter.Button(self.frame3, text='Criar', command=self.criar_usuario, fg='green', padx=15)

        # CRIA REGISTRO DO ULTIMO USUARIO CASO NAO EXISTA
        if 'ultimo<>:/?' not in self.data:
            self.data['ultimo<>:/?'] = ['', '']
        else:
            # VERIFICA SE A FUNÇAO LEMBRAR ESTA ATIVADA.
            if 'lembrar<>:/?' in self.data:
                if self.data['lembrar<>:/?'] == 1:
                    self.setlembrar.set(1)
                    self.usuarioentry.insert(0, self.data['ultimo<>:/?'][0])
                    self.senhaentry.insert(0, self.data['ultimo<>:/?'][1])

        # MOSTRA INTERFACE DE LOGIN.
        self.usuariotxt.pack()
        self.usuarioentry.pack()
        self.senhatxt.pack()
        self.senhaentry.pack()
        self.mensagem.pack()
        self.lembrar.pack()
        self.entrar.pack(side=tkinter.LEFT)
        self.novo.pack()

    def fazer_login(self):
        """
        METODO PARA FAZER LOGIN.
        """
        #VERIFICA EXISTENCIA DO USUARIO E SENHA.
        try:
            usuario_atual = self.usuarioentry.get()
            senha_atual = self.senhaentry.get()
            if self.data[usuario_atual]['senha'] == senha_atual:
                self.mensagem['text'] = f'Bem vindo {usuario_atual}!'
                self.mensagem['fg'] = 'blue'
                if self.setlembrar.get() == 1:
                    self.data['ultimo<>:/?'] = [usuario_atual, senha_atual]
                    self.data.close()
                    self.destroy_login()
                    self.inicia_aplicacao(usuario_atual)
            else:
                self.mensagem['text'] = 'Senha inválida'
                self.mensagem['fg'] = 'red'
        except:
            self.mensagem['text'] = 'Usuário inválido'
            self.mensagem['fg'] = 'red'

    def criar_usuario(self):
        """
        METODO PARA CRIAR NOVO USUARIO.
        """
        #VERIFICA CAMPOS DIGITADOS E CRIA NOVO USUARIO.
        email = self.emailentry.get()
        usuario = self.usuarioentry.get()
        senha = self.senhaentry.get()
        nome = self.nomeentry.get()
        for c in self.data:
            if c == 'lembrar<>:/?' or 'ultimo<>:/?':
                pass
            elif email == self.data[c]['email']:
                print('ok')
                self.mensagem['text'] = 'E-mail já cadastrado.'
                self.mensagem['fg'] = 'red'
                break

        if usuario == '' or senha == '' or email == '' or nome == '':
            self.mensagem['text'] = 'Todos os campos devem ser preenchidos.'
            self.mensagem['fg'] = 'red'

        elif usuario in self.data:
            self.mensagem['text'] = 'Nome de usuário em uso.'
            self.mensagem['fg'] = 'red'

        elif self.mensagem['text'] == 'E-mail já cadastrado.':
            pass

        else:
            self.data[usuario] = {'nome': nome, 'email': email, 'senha': senha}
            self.mensagem['text'] = 'Usuário criado com sucesso!'
            self.mensagem['fg'] = 'blue'

    def lembrar(self):
        """
        METODO PARA LEMBRAR USUÁRIO.
        """
        self.data['lembrar<>:/?'] = self.setlembrar.get()
        if self.setlembrar.get() == 0:
            self.data['ultimo<>:/?'] = ['', '']

    def iniciar(self):
        """
        METODO PARA INICIAR INTERFACE.
        """
        #RECEBE INSTANCIA DE TK.
        run = self.interface

        #INICIA A INTERFACE.
        run.mainloop()

    def mostra_login(self):
        """
        METODO PARA MOSTRAR ELEMENTOS DE LOGIN.
        """
        self.esconde_criar()

        # EMPACOTA OS ELEMENTOS DA INTERFACE DE LOGIN.
        self.usuariotxt.pack()
        self.usuarioentry.pack()
        self.senhatxt.pack()
        self.senhaentry.pack()
        self.mensagem.pack()
        self.lembrar.pack()
        self.entrar.pack(side=tkinter.LEFT)
        self.novo.pack()

    def mostra_criar(self):
        """
        METODO PARA MOSTRAR ELEMENTOS DE CRIAR.
        """
        self.esconde_login()

        #EMPACOTA OS ELEMENTOS DA INTERFACE DE CRIAR.
        self.nometxt.pack()
        self.nomeentry.pack()
        self.emailtxt.pack()
        self.emailentry.pack()
        self.usuariotxt.pack()
        self.usuarioentry.pack()
        self.senhatxt.pack()
        self.senhaentry.pack()
        self.voltar.pack(side=tkinter.LEFT)
        self.criar.pack()
        self.mensagem.pack()

    def esconde_login(self):
        """
        METODO PARA ESCONDER ELEMENTOS DE LOGIN.
        """
        #LIMPA DADOS VISUAIS
        self.usuarioentry.delete(0, tkinter.END)
        self.senhaentry.delete(0, tkinter.END)
        self.mensagem['text'] = ''

        #ESCONDE OS ELEMENTOS DA INTERFACE DE LOGIN.
        self.usuariotxt.forget()
        self.usuarioentry.forget()
        self.senhatxt.forget()
        self.senhaentry.forget()
        self.mensagem.forget()
        self.lembrar.forget()
        self.entrar.forget()
        self.novo.forget()

    def esconde_criar(self):
        """
        METODO PARA ESCONDER ELEMENTOS DE CRIAR.
        """
        #LIMPA DADOS VISUAIS
        self.nomeentry.delete(0, tkinter.END)
        self.emailentry.delete(0, tkinter.END)
        self.usuarioentry.delete(0, tkinter.END)
        self.senhaentry.delete(0, tkinter.END)
        self.mensagem['text'] = ''

        # ESCONDE OS ELEMENTOS DA INTERFACE DE CRIAR.
        self.nometxt.forget()
        self.nomeentry.forget()
        self.emailtxt.forget()
        self.emailentry.forget()
        self.usuariotxt.forget()
        self.usuarioentry.forget()
        self.senhatxt.forget()
        self.senhaentry.forget()
        self.criar.forget()
        self.mensagem.forget()
        self.voltar.forget()

    def destroy_login(self):
        self.nometxt.destroy()
        self.nomeentry.destroy()
        self.emailtxt.destroy()
        self.emailentry.destroy()
        self.usuariotxt.destroy()
        self.usuarioentry.destroy()
        self.senhatxt.destroy()
        self.senhaentry.destroy()
        self.voltar.destroy()
        self.criar.destroy()
        self.mensagem.destroy()
        self.lembrar.destroy()
        self.entrar.destroy()
        self.novo.destroy()
        self.nada.destroy()
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()

    def inicia_aplicacao(self, usuario):
        if self.proxima_tela == 'pass':
            pass
        else:
            self.proxima_tela(self.interface, usuario)


tela = tkinter.Tk()
login(tela, 'pass')
tela.mainloop()
