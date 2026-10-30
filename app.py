import sqlite3

def conexao_banco():
    conexao = sqlite3.connect("contatos.db")
    cursor = conexao.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        );
        '''
    )
    return conexao

def adicionar_contato(nome, telefone, email):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
        INSERT INTO contatos (nome, telefone, email)
        VALUES (?, ?, ?)
    '''
    cursor.execute(sql, (nome, telefone, email))
    conexao.commit()
    conexao.close()

def listar_contatos():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
        SELECT * FROM contatos;
    '''
    cursor.execute(sql)
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("### LISTA DE CONTATOS ###")
        print(f"{'ID':<5} | {'NOME':<20} | {'TELEFONE':<15} | {'EMAIL':<30}")
        print("-" * 75)
        for contato in contatos:
            print(f"{contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30}")

def buscar_contato():
    termo = input("Digite o nome ou parte do nome para buscar: ").strip()

    if not termo:
        print("Nome inválido.")
        return

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT * FROM contatos WHERE nome LIKE ? ORDER BY nome",
        (f"%{termo}%",),
    )
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
        return

    print("### RESULTADO DA BUSCA ###")
    print(f"{'ID':<5} | {'NOME':<20} | {'TELEFONE':<15} | {'EMAIL':<30}")
    print("-" * 75)
    for contato in contatos:
        print(f"{contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30}")

def atualizar_contato():
    id_contato = input("Digite o ID do contato que deseja atualizar: ").strip()

    if not id_contato.isdigit():
        print("ID inválido.")
        return

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM contatos WHERE id = ?", (id_contato,))
    contato = cursor.fetchone()

    if contato is None:
        print("Contato não encontrado.")
        conexao.close()
        return

    nome = input(f"Novo nome ({contato[1]}): ").strip() or contato[1]
    telefone = input(f"Novo telefone ({contato[2]}): ").strip() or contato[2]
    email = input(f"Novo email ({contato[3]}): ").strip() or contato[3]

    cursor.execute(
        "UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?",
        (nome, telefone, email, id_contato),
    )
    conexao.commit()
    conexao.close()
    print("Contato atualizado com sucesso!")

def excluir_contato():
    id_contato = input("Digite o ID do contato que deseja excluir: ").strip()

    if not id_contato.isdigit():
        print("ID inválido.")
        return

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM contatos WHERE id = ?", (id_contato,))
    contato = cursor.fetchone()

    if contato is None:
        print("Contato não encontrado.")
        conexao.close()
        return

    cursor.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))
    conexao.commit()
    conexao.close()
    print(f"Contato '{contato[1]}' excluído com sucesso!")

def menu():
    while True:
        print("### CONTATOS ###")
        print("1. Adicionar contato")
        print("2. Listar contatos")
        print("3. Buscar contato pelo nome")
        print("4. Atualizar contato")
        print("5. Excluir contato")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do contato: ")
            telefone = input("Digite o telefone do contato: ")
            email = input("Digite o email do contato: ")
            adicionar_contato(nome, telefone, email)
            print("Contato adicionado com sucesso!")
        elif opcao == "2":
            listar_contatos()
        elif opcao == "3":
            buscar_contato()
        elif opcao == "4":
            atualizar_contato()
        elif opcao == "5":
            excluir_contato()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()