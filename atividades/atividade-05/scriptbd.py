import sqlite3

def cria_tabela():
    conexao = sqlite3.connect("pessoas.db")
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            estado TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def insere_aluno(nome, cpf, estado):
    conexao = sqlite3.connect("pessoas.db")
    cursor = conexao.cursor()

    try:
        cursor.execute('''
            INSERT INTO pessoas (nome, cpf, estado) VALUES (?, ?, ?)
        ''', (nome, cpf, estado))
        conexao.commit()
        print("Pessoa registrada com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já registrado.")
    conexao.close()

def busca_aluno(nome=None, cpf=None):
    conexao = sqlite3.connect("pessoas.db")
    cursor = conexao.cursor()

    query = 'SELECT * FROM pessoas WHERE 1=1'
    parametros = []

    if nome:
        query += ' AND nome = ?'
        parametros.append(nome)
    if cpf:
        query += ' AND cpf = ?'
        parametros.append(cpf)

    cursor.execute(query, parametros)
    resultado = cursor.fetchall()
    conexao.close()

    return resultado

def atualiza_aluno(id, nome=None, cpf=None, estado=None):
    conexao = sqlite3.connect("pessoas.db")
    cursor = conexao.cursor()

    campos = []
    parametros = []

    if nome:
        campos.append('nome = ?')
        parametros.append(nome)
    if cpf:
        campos.append('cpf = ?')
        parametros.append(cpf)
    if estado:
        campos.append('estado = ?')
        parametros.append(estado)

    if not campos:
        print("Nenhuma informação para atualizar.")
        conexao.close()
        return

    query = f'UPDATE pessoas SET {", ".join(campos)} WHERE id = ?'
    parametros.append(id)

    cursor.execute(query, parametros)
    conexao.commit()
    conexao.close()

    print("Registro atualizado com sucesso!")

def deleta_aluno(id):
    conexao = sqlite3.connect("pessoas.db")
    cursor = conexao.cursor()

    cursor.execute('''
        DELETE FROM pessoas WHERE id = ?
    ''', (id,))

    conexao.commit()
    conexao.close()

    print("Registro deletado com sucesso!")

def main():
    cria_tabela()

    while True:
        print("\nEscolha uma opção:")
        print("1. Inserir aluno")
        print("2. Buscar aluno")
        print("3. Atualizar aluno")
        print("4. Deletar aluno")
        print("5. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            print("Insira o nome da pessoa: ")
            nome = input()
            print("Insira o CPF: ")
            cpf = input()
            print("Insira o estado: ")
            estado = input()

            insere_aluno(nome, cpf, estado)

        elif opcao == "2":
            print("Digite o nome da pessoa (ou deixe em branco para ignorar): ")
            nome = input()
            print("Digite o CPF da pessoa (ou deixe em branco para ignorar): ")
            cpf = input()

            resultado = busca_aluno(nome if nome else None, cpf if cpf else None)
            if resultado:
                for linha in resultado:
                    print(f"ID: {linha[0]}, Nome: {linha[1]}, CPF: {linha[2]}, Estado: {linha[3]}")
            else:
                print("Nenhum aluno encontrado com esses critérios.")

        elif opcao == "3":
            print("Digite o ID do aluno a ser atualizado: ")
            id = input()
            print("Digite o novo nome (ou deixe em branco para não alterar): ")
            nome = input()
            print("Digite o novo CPF (ou deixe em branco para não alterar): ")
            cpf = input()
            print("Digite o novo estado (ou deixe em branco para não alterar): ")
            estado = input()

            atualiza_aluno(int(id), nome if nome else None, cpf if cpf else None, estado if estado else None)

        elif opcao == "4":
            print("Digite o ID do aluno a ser deletado: ")
            id = input()
            deleta_aluno(int(id))

        elif opcao == "5":
            break

        else:
            print("Opção inválida! Tente novamente.")

# Execução
if __name__ == "__main__":
    main()
