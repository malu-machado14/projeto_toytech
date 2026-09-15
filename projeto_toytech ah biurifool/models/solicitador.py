#imports
from core.crud import Crud
from core.conexao import Database
from core.validar import Validador

#classe que representa um solicitador no sistema
class Solicitador(Crud):
    table = "solicitador"
    #lista de campos da tabela
    fields = [
        "id",
        "nome",
        "cnpj",
        "senha",
        "telefone"
    ]

    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, id, nome, cnpj, senha, telefone,):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.senha = senha
        self.telefone = telefone

    #valida os dados do produto
    def validate(self):
        #lista de possiveis erros
        erros = [
         Validador.required(self.nome, "nome"),
         Validador.non_negative(self.cnpj, "cnpj"),
         Validador.non_negative(self.senha, "senha"),
         Validador.non_negative(self.telefone, "telefone"),
         Validador.count_to_8(self.senha,"senha"),
         Validador.count_to_14(self.cnpj,"cnpj"),
         Validador.count_to_9(self.telefone,"telefone"),
         Validador.have_number(self.telefone,"telefone"),
         Validador.not_have_scaracter(self.telefone,"telefone"),
         Validador.not_have_upper(self.nome, "nome")
        ]
        #retorna os erros
        return [erro for erro in erros if erro]

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO solicitador
        (nome, cnpj, senha, telefone)
        VALUES (%s, %s, %s, %s)
        """
        valores = (
            self.nome,
            self.cnpj,
            self.senha,
            self.telefone
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

        sql = "SELECT * FROM solicitador"
        cursor.execute(sql,)
        solicitador = cursor.fetchall()

        cursor.close()
        conexao.close()
        return solicitador

    #retorna solicitadores em ordem alfabetica
    @classmethod
    def find_by_name(cls, nome):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM solicitador WHERE nome LIKE %s ORDER BY nome"
            cursor.execute(sql, (f"%{nome}%",))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    #metodo para buscar o id de solicitador
    @classmethod
    def find_by_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM solicitador WHERE id = %s"
        cursor.execute(sql, (id,))
        solicitador = cursor.fetchone()

        cursor.close()
        conexao.close()
        return solicitador        


    #metodo para atualizar a quantidade de solicitadores
    @classmethod
    def update(cls, nome, cnpj, senha, telefone, id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE solicitador SET nome = %s, cnpj = %s, senha = %s, telefone = %s WHERE id = %s"
            cursor.execute(sql, ( nome, cnpj, senha, telefone, id))
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



    #metodo para deletar um solicitador
    @classmethod
    def delete(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM solicitador WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()