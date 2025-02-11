import sqlite3
import matplotlib.pyplot as plt
import pandas as pd


class MomCare:
    def __init__(self):
        self.conn = sqlite3.connect('momcare.db')
        self.c = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS utilizadores (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome VARCHAR(45) NOT NULL,
                            email VARCHAR(45) UNIQUE NOT NULL,
                            senha VARCHAR(45) NOT NULL)''')
    
            self.c.execute('''CREATE TABLE IF NOT EXISTS bebe (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome VARCHAR(45) NOT NULL,
                            data_nascimento DATE NOT NULL,
                            peso DECIMAL NOT NULL,
                            altura DECIMAL NOT NULL,
                            mae_id INTEGER,
                            FOREIGN KEY (mae_id) 
                                REFERENCES utilizadores (id))''')
            
            self.c.execute('''CREATE TABLE IF NOT EXISTS diario_bebe (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            alimentacao TEXT NOT NULL,
                            fraldas TEXT NOT NULL,
                            sono TEXT NOT NULL,
                            desenvolvimento TEXT NOT NULL,
                            peso DECIMAL NOT NULL,
                            altura DECIMAL NOT NULL, 
                            data DATE NOT NULL,
                            hora TIME NOT NULL,
                            bebe_id INTEGER,
                            FOREIGN KEY (bebe_id) 
                                REFERENCES bebe (id))''')
            
                        
            self.c.execute('''CREATE TABLE IF NOT EXISTS lembretes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            descricao TEXT NOT NULL,
                            data DATE NOT NULL,
                            hora TIME NOT NULL,
                            bebe_id INTEGER,
                            FOREIGN KEY (bebe_id) 
                                REFERENCES bebe (id))''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS comunidade (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            utilizador_id INTEGER,
                            mensagem TEXT NOT NULL,
                            data_envio DATE NOT NULL,
                            FOREIGN KEY (utilizador_id) 
                                REFERENCES utilizadores(id))''')
                            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
            self.conn.rollback()
            
    def registar_utilizador(self, utilizadores):
        try:
            self.c.execute("INSERT INTO utilizadores (nome, email, senha) VALUES (?, ?, ?)", (utilizadores))
            self.conn.commit()
            print("Sucesso!", "Utilizador registado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao registar utilizador: {e}")

    def listar_utilizadores(self):
        self.c.execute("SELECT * FROM utilizadores")
        dados = self.c.fetchall()

        for i in dados:
                print(f'Nome:{i[1]} | Email:{i[2]} | Senha:{i[3]}')
        
    def atualizar_utilizador(self, nova_informacao):
        query = "UPDATE utilizadores SET nome=?, email=?, senha=? WHERE id=?"
        
        try:
            self.c.execute(query, nova_informacao)
            self.conn.commit()
            print("Sucesso!", f"Utilizador com ID:{nova_informacao[3]} atualizado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao atualizar utilizador: {e}")
            
    def eliminar_utilizador(self, id):
        try:
            self.c.execute("DELETE FROM utilizadores WHERE id=?", (id,))
            self.conn.commit()
            print("Sucesso!", f"Utilizador com ID:{id} eliminado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao eliminar utilizador: {e}")
    
    def verificar_mae_id(self, mae_id):
        self.c.execute("SELECT id FROM utilizadores WHERE id = ?", (mae_id,))
        return self.c.fetchone() is not None
    
    def registar_bebe(self, nome, data_nascimento, peso, altura, mae_id):
        if not self.verificar_mae_id(mae_id):
            print("Erro!", "O ID da mãe não existe!")
            return
        try:
            self.c.execute("INSERT INTO bebe (nome, data_nascimento, peso, altura, mae_id) VALUES (?, ?, ?, ?, ?)", (nome, data_nascimento, peso, altura, mae_id))
            self.conn.commit()
            print("Sucesso!", "Bebé registado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao registar bebé: {e}")
      
    def listar_bebes(self):
        self.c.execute("SELECT * FROM bebe")
        dados = self.c.fetchall()

        for i in dados:
            print(f'Nome:{i[1]} | Data de Nascimento:{i[2]} | Peso:{i[3]} | Altura:{i[4]} | Mãe ID:{i[5]}')

    def atualizar_bebe(self, id, nome, data_nascimento, peso, altura, mae_id):
        query = "UPDATE bebe SET nome=?, data_nascimento=?, peso=?, altura=?, mae_id=? WHERE id=?" 
        
        try:
            self.c.execute(query, (nome, data_nascimento, peso, altura, mae_id, id))
            self.conn.commit()
            print("Sucesso!", f"Bebé com ID:{id} atualizado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao atualizar bebé: {e}")

    def eliminar_bebe(self, id):
        try:
            self.c.execute("DELETE FROM bebe WHERE id=?", (id,))
            self.conn.commit()
            print("Sucesso!", f"Bebé com ID:{id} eliminado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao eliminar bebé: {e}")
          
    def registar_diario_bebe(self, alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id):
        try:
            self.c.execute("INSERT INTO diario_bebe (alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id))
            self.conn.commit()
            print("Ação registada no diário com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao registar ação no diário: {e}")
            
    def listar_diario_bebe(self):
        self.c.execute("SELECT * FROM diario_bebe")
        dados = self.c.fetchall()

        for i in dados:
                print(f'Alimentação:{i[1]} | Fraldas:{i[2]} | Sono:{i[3]} | Desenvolvimento:{i[4]} | Peso:{i[5]} | Altura:{i[6]} | Data:{i[7]} | Hora:{i[8]} | Bebé ID:{i[9]}')
    
    def atualizar_diario_bebe(self, id, alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id):
        query = "UPDATE diario_bebe SET alimentacao=?, fraldas=?, sono=?, desenvolvimento=?, peso=?, altura=?, data=?, hora=?, bebe_id=? WHERE id=?"
        
        try:
            self.c.execute(query, (alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id, id))
            self.conn.commit()
            print("Sucesso!", f"Ação com ID:{id} atualizada com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao atualizar ação: {e}")
    
    def eliminar_diario_bebe(self, id):
        try:
            self.c.execute("DELETE FROM diario_bebe WHERE id=?", (id,))
            self.conn.commit()
            print("Sucesso!", f"Ação com ID:{id} eliminada com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao eliminar ação: {e}")
    
    def grafico_crescimento_bebe(self, bebe_id):
        try:
            self.c.execute("SELECT data_nascimento, peso, altura FROM bebe WHERE id = ?", (bebe_id,))
            dados = self.c.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao consultar base de dados: {e}")
            return

        if not dados:
            print(f"Nenhum dado encontrado para o bebé com ID {bebe_id}.")
            return

        df = pd.DataFrame(dados, columns=['Data Nascimento', 'Peso', 'Altura'])
        df['Data Nascimento'] = pd.to_datetime(df['Data Nascimento'])
        df.set_index('Data Nascimento', inplace=True)
        
        if not df.empty:
            plt.figure(figsize=(10, 5))  
            plt.plot(df.index, df['Peso'], label='Peso (kg)', marker='o', linestyle='-')
            plt.plot(df.index, df['Altura'], label='Altura (cm)', marker='s', linestyle='--')

            plt.xlabel("Data de Nascimento")
            plt.ylabel("Peso/Altura")
            plt.title(f"Gráfico de Crescimento do Bebé (ID: {bebe_id})")
            plt.legend()
            plt.grid(True) 
            plt.xticks(rotation=45)  
            plt.tight_layout()  
            plt.show()
        else:
            print(f"Nenhum dado encontrado para o bebé com ID {bebe_id}.")
    
    def registar_lembrete(self, descricao, data, hora, bebe_id):
        try:
            self.c.execute("INSERT INTO lembretes (descricao, data, hora, bebe_id) VALUES (?, ?, ?, ?)", (descricao, data, hora, bebe_id))
            self.conn.commit()
            print("Lembrete registado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao registar Lembrete: {e}")
    
    def listar_lembretes(self):
        self.c.execute("SELECT * FROM lembretes")
        dados = self.c.fetchall()

        for i in dados:
                print(f'Descrição:{i[1]} | Data:{i[2]} | Hora:{i[3]} | Bebé ID:{i[4]}')
                           
    def atualizar_lembrete(self, id, descricao, data, hora, bebe_id):   
        query = "UPDATE lembretes SET descricao=?, data=?, hora=?, bebe_id=? WHERE id=?" 
        
        try:
            self.c.execute(query, (descricao, data, hora, bebe_id, id))
            self.conn.commit()
            print("Sucesso!", f"Lembrete com ID:{id} atualizado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao atualizar lembrete: {e}")           
    
    def eliminar_lembrete(self, id):
        try:
            self.c.execute("DELETE FROM lembretes WHERE id=?", (id,))
            self.conn.commit()
            print("Sucesso!", f"Lembrete com ID:{id} eliminado com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao eliminar lembrete: {e}")

    def registar_mensagem(self, comunidade):
        try:
            self.c.execute("INSERT INTO comunidade (utilizador_id, mensagem, data_envio) VALUES (?, ?, ?)", (comunidade))
            self.conn.commit()
            print("Sucesso!", "Mensagem registada com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao adicionar mensagem: {e}")

    def listar_mensagens(self):
        self.c.execute("SELECT * FROM comunidade")
        dados = self.c.fetchall()

        for i in dados:
                print(f'Utilizador ID:{i[1]} | Mensagem:{i[2]} | Data de Envio:{i[3]}')
    
    def atualizar_mensagem(self, id, utiliizador_id, mensagem, data_envio):
        query = "UPDATE comunidade SET utilizador_id=?, mensagem=?, data_envio=? WHERE id=?"
        
        try:
            self.c.execute(query, (utiliizador_id, mensagem, data_envio, id))
            self.conn.commit()
            print("Sucesso!", f"Mensagem com ID:{id} atualizada com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao atualizar mensagem: {e}")

    def eliminar_mensagem(self, id):
        try:
            self.c.execute("DELETE FROM comunidade WHERE id=?", (id,))
            self.conn.commit()
            print("Sucesso!", f"Mensagem com ID:{id} eliminada com sucesso!")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Erro!", f"Erro ao eliminar mensagem: {e}")
            
            
    def menu(self):
        while True:
            print("\n=== Menu Principal ====")
            print("1. Utilizador")
            print("2. Bebé")
            print("3. Diário do Bebé")
            print("4. Lembretes")
            print("5. Comunidade")
            print("0. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.menu_utilizadores()
            elif opcao == '2':
                self.menu_bebe()
            elif opcao == '3':
                self.menu_diario_bebe()
            elif opcao == '4':
                self.menu_lembretes()
            elif opcao == '5':
                self.menu_comunidade()
            elif opcao == '0':
                print("Obrigada por usar o MomCare!")
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_utilizadores(self):
        while True:
            print("\n--- Menu Utilizador ---")
            print("1. Registar Utilizador")
            print("2. Listar Utilizadores")
            print("3. Atualizar Utilizador")
            print("4. Eliminar Utilizador")
            print("0. Voltar ao Menu Principal")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                nome = input("Nome: ")
                email = input("Email: ")
                senha = input("Senha: ")
                self.registar_utilizador((nome, email, senha))
            elif opcao == '2':
                self.listar_utilizadores()
            elif opcao == '3':
                id = input("ID do utilizador a ser atualizado: ")
                nome = input("Novo nome: ")
                email = input("Novo email: ")
                senha = input("Nova senha: ")
                self.atualizar_utilizador((nome, email, senha, id))
            elif opcao == '4':
                id = input("ID do utilizador a ser eliminado: ")
                self.eliminar_utilizador(id)
            elif opcao == '0':
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_bebe(self):
        while True:
            print("\n--- Menu Bebé ---")
            print("1. Registar Bebé")
            print("2. Listar Bebés")
            print("3. Atualizar Bebé")
            print("4. Eliminar Bebé")
            print("0. Voltar ao Menu Principal")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                nome = input("Nome do bebé: ")
                data_nascimento = input("Data de nascimento (YYYY-MM-DD): ")
                peso = input("Peso: ")
                altura = input("Altura: ")
                mae_id = input("ID da mãe: ")
                self.registar_bebe(nome, data_nascimento, peso, altura, mae_id)
            elif opcao == '2':
                self.listar_bebes()
            elif opcao == '3':
                id = input("ID do bebé a ser atualizado: ")
                nome = input("Novo nome: ")
                data_nascimento = input("Nova data de nascimento (YYYY-MM-DD): ")
                peso = input("Novo peso: ")
                altura = input("Nova altura: ")
                mae_id = input("Novo ID da mãe: ")
                self.atualizar_bebe(id, nome, data_nascimento, peso, altura, mae_id)
            elif opcao == '4':
                id = input("ID do bebé a ser eliminado: ")
                self.eliminar_bebe(id)
            elif opcao == '0':
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_diario_bebe(self):
        while True:
            print("\n--- Menu Diário do Bebé ---")
            print("1. Registar Ação no Diário")
            print("2. Listar Ações no Diário")
            print("3. Atualizar Ação no Diário")
            print("4. Eliminar Ação no Diário")
            print("5. Exibir Gráfico de Crescimento")
            print("0. Voltar ao Menu Principal")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                alimentacao = input("Alimentação: ")
                fraldas = input("Fraldas: ")
                sono = input("Sono: ")
                desenvolvimento = input("Desenvolvimento: ")
                peso = input("Peso: ")
                altura = input("Altura: ")
                data = input("Data (YYYY-MM-DD): ")
                hora = input("Hora (HH:MM): ")
                bebe_id = input("ID do bebé: ")
                self.registar_diario_bebe(alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id)
            elif opcao == '2':
                self.listar_diario_bebe()
            elif opcao == '3':
                id = input("ID da ação a ser atualizada: ")
                alimentacao = input("Nova alimentação: ")
                fraldas = input("Novas fraldas: ")
                sono = input("Novo sono: ")
                desenvolvimento = input("Novo desenvolvimento: ")
                peso = input("Novo peso: ")
                altura = input("Nova altura: ")
                data = input("Nova data (YYYY-MM-DD): ")
                hora = input("Nova hora (HH:MM): ")
                bebe_id = input("Novo ID do bebé: ")
                self.atualizar_diario_bebe(id, alimentacao, fraldas, sono, desenvolvimento, peso, altura, data, hora, bebe_id)
            elif opcao == '4':
                id = input("ID da ação a ser eliminada: ")
                self.eliminar_diario_bebe(id)
            elif opcao == '5':
                bebe_id = input("ID do bebé: ")
                self.grafico_crescimento_bebe(bebe_id)
            elif opcao == '0':
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_lembretes(self):
        while True:
            print("\n--- Menu Lembretes ---")
            print("1. Registar Lembrete")
            print("2. Listar Lembretes")
            print("3. Atualizar Lembrete")
            print("4. Eliminar Lembrete")
            print("0. Voltar ao Menu Principal")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                descricao = input("Descrição do lembrete: ")
                data = input("Data (YYYY-MM-DD): ")
                hora = input("Hora (HH:MM): ")
                bebe_id = input("ID do bebé: ")
                self.registar_lembrete(descricao, data, hora, bebe_id)
            elif opcao == '2':
                self.listar_lembretes()
            elif opcao == '3':
                id = input("ID do lembrete a ser atualizado: ")
                descricao = input("Nova descrição: ")
                data = input("Nova data (YYYY-MM-DD): ")
                hora = input("Nova hora (HH:MM): ")
                bebe_id = input("Novo ID do bebé: ")
                self.atualizar_lembrete(id, descricao, data, hora, bebe_id)
            elif opcao == '4':
                id = input("ID do lembrete a ser eliminado: ")
                self.eliminar_lembrete(id)
            elif opcao == '0':
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_comunidade(self):
        while True:
            print("\n--- Menu Comunidade ---")
            print("1. Registar Mensagem")
            print("2. Listar Mensagens")
            print("3. Atualizar Mensagem")
            print("4. Eliminar Mensagem")
            print("0. Voltar ao Menu Principal")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                utilizador_id = input("ID do utilizador: ")
                mensagem = input("Mensagem: ")
                data_envio = input("Data de envio (YYYY-MM-DD): ")
                self.registar_mensagem((utilizador_id, mensagem, data_envio))
            elif opcao == '2':
                self.listar_mensagens()
            elif opcao == '3':
                id = input("ID da mensagem a ser atualizada: ")
                utilizador_id = input("Novo ID do utilizador: ")
                mensagem = input("Nova mensagem: ")
                data_envio = input("Nova data de envio (YYYY-MM-DD): ")
                self.atualizar_mensagem(id, utilizador_id, mensagem, data_envio)
            elif opcao == '4':
                id = input("ID da mensagem a ser eliminada: ")
                self.eliminar_mensagem(id)
            elif opcao == '0':
                break
            else:
                print("Opção inválida, tente novamente.")

# instância da base de dados
mom_care = MomCare()
mom_care.menu()
