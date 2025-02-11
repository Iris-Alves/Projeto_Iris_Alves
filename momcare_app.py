import customtkinter as tk

tk.set_appearance_mode('dark')

def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if usuario == 'iris' and senha == '1234':
        print('Entrou')
    else:
        print('Usuário ou senha inválidos')


app = tk.CTk()
app.title('MomCare')
app.geometry('400x400')

logo = tk.CTkLabel(app, text='MomCare - Assitente para Mães de Primeira Viagem', font=('Arial', 15), justify='center')
logo.pack(pady=10)

label_senha = tk.CTkLabel(app, text='Bem-Vinda, mamã!', justify='center')
label_senha.pack(pady=10)

campo_usuario = tk.CTkEntry(app, placeholder_text='Nome de utilizador', justify='center')
campo_usuario.pack(pady=10)


campo_senha = tk.CTkEntry(app, placeholder_text='Digite a sua Senha', show='*', justify='center')
campo_senha.pack(pady=10)

ctk_button = tk.CTkButton(app, text='Login', command=validar_login)
ctk_button.pack(pady=10)

campo_criar = tk.CTkEntry(app, placeholder_text='Criar Nova Conta', justify='center')
campo_criar.pack(pady=10)

app.mainloop()

