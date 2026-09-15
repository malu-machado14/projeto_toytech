#imports
from core.crud import Crud
from core.conexao import Database
from core.validar import Validador

#classe que representa um funcionario no sistema
class Funcionario(Crud):
    table = "funcionario"
    #lista de campos da tabela
    fields = [
        "id",
        "nome",
        "cpf",
        "email",
        "senha",
        "telefone",
        "cargo"
    ]

    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, nome, cpf, email, senha,
                 telefone, cargo, id=None):
        #atribui os valores aos objetos
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.cargo = cargo

    #valida os dados do funcionario
    def validate(self):
        #lista de possiveis erros
        erros = [
         Validador.required(self.nome, "nome"),
         Validador.non_negative(self.cpf, "cpf"),
         Validador.required(self.email, "email"),
         Validador.required(self.senha, "senha"),
         Validador.non_negative(self.senha, "senha"),
         Validador.non_negative(self.telefone, "telefone"),
         Validador.non_negative(self.cargo, "cargo"),
         Validador.have_number(self.telefone, "telefone"),
         Validador.have_scaracter(self.email, "email"),
         Validador.count_to_8(self.senha, "senha"),
         Validador.count_to_11(self.cpf, "cpf"),
         Validador.count_to_9(self.telefone,"telefone"),
         Validador.not_have_upper(self.nome, "nome")
        ]
        #retorna os erros
        return [erro for erro in erros if erro]

    def autenticar(self, email, senha):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM funcionario
            WHERE email = %s
            AND senha = %s
        """

        cursor.execute(sql, (email,senha,))
        funcionario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if funcionario is None:
            return None
        return funcionario

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO funcionario
        (nome, cpf, email, senha, telefone, cargo)
        VALUES (%s, %s, %s, %s, %s,%s)
        """
        valores = (
            self.nome,
            self.cpf,
            self.email,
            self.senha,
            self.telefone,
            self.cargo
        )

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()

    @classmethod
    def find_all(cls):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM funcionario"
        cursor.execute(sql,)
        funcionario = cursor.fetchall()

        cursor.close()
        conexao.close()
        return funcionario
    
    #retorna funcionarios que possuem tais cargos
    @classmethod
    def find_by_cargo(cls, cargo):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM funcionario WHERE cargo = %s"
            cursor.execute(sql, (cargo,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def find_by_name(cls, nome):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM funcionario WHERE nome LIKE %s ORDER BY nome "
        cursor.execute(sql, (f"%{nome}%",))
        funcionario = cursor.fetchall()

        cursor.close()
        conexao.close()
        return funcionario

    @classmethod
    def find_by_email(cls, email):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM funcionario WHERE email = %s "
        cursor.execute(sql, (email,))
        funcionario = cursor.fetchone()

        cursor.close()
        conexao.close()
        return funcionario


    #metodo para buscar o id de funcionario
    @classmethod
    def find_by_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM funcionario WHERE id = %s"
        cursor.execute(sql, (id,))
        funcionario = cursor.fetchone()

        cursor.close()
        conexao.close()
        return funcionario        


    #metodo para atualizar o funcionario
    @classmethod
    def update(cls, nome, cpf, email, senha, telefone, cargo, id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE funcionario SET nome = %s, cpf = %s, email = %s, senha = %s, telefone = %s, cargo = %s WHERE id = %s"
            cursor.execute(sql, (nome,cpf,email,senha,telefone,cargo,id))
            if connection is None:
                conexao.commit()
            return cursor.rowcount
        except Exception:
            if connection is None:
                conexao.rollback()
            raise
        finally:
            cursor.close()
            if connection is None:
                conexao.close()


    #metodo para excluir funcionario
    @classmethod
    def delete(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM funcionario WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()
