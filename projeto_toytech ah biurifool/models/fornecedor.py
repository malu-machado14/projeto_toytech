#imports
from core.conexao import Database
from core.crud import Crud
from core.validar import Validador

#classe que representa um fornecedor no sistema
class Fornecedor(Crud):

    table = "fornecedor"
    #lista de campos da tabela
    fields = [
        "id",
        "nome",
        "cnpj",
        "telefone"
    ]
    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, nome, cnpj, telefone, id = None):
        #atribui os valores aos objetos
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        
        
    
    #valida os dados do fornecedor
    def validate(self):

        #lista de possiveis erros
        erros = [
             Validador.required(self.nome, "nome"),
             Validador.not_have_number(self.nome, "nome"),
             Validador.required(self.cnpj, "cnpj"),
             Validador.not_have_scaracter(self.cnpj, "cnpj"),
             Validador.not_have_upper(self.nome,"nome"),
             Validador.non_negative(self.cnpj, "cnpj"),
             Validador.non_negative(self.telefone, "telefone"),
             Validador.count_to_14(self.cnpj, "cnpj"),
             Validador.count_to_9(self.telefone, "telefone")

            ]
        #retorna os erros
        return [erro for erro in erros if erro]

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO fornecedor
        (nome, cnpj,telefone)
        VALUES (%s, %s, %s)
        """
        valores = (
            self.nome,
            self.cnpj,
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

        sql = "SELECT * FROM fornecedor"
        cursor.execute(sql,)
        fornecedor = cursor.fetchall()

        cursor.close()
        conexao.close()
        return fornecedor
    
    #metodo para listar fornecedor
    @classmethod
    def find_by_name(cls,nome):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM fornecedor WHERE nome LIKE %s ORDER BY nome"
        cursor.execute(sql, (f"%{nome}%",))
        fornecedor = cursor.fetchall()

        cursor.close()
        conexao.close()
        return fornecedor
    
    #metodo para buscar o id do fornecedor
    @classmethod
    def find_by_id(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM fornecedor WHERE id = %s"
        cursor.execute(sql, (id,))
        fornecedor = cursor.fetchone()

        cursor.close()
        conexao.close()
        return fornecedor

    #metodo para atualizar fornecedor
    @classmethod
    def update(cls, nome, cnpj, telefone, id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE fornecedor SET nome = %s, cnpj = %s, telefone = %s WHERE id = %s"
            cursor.execute(sql, (nome, cnpj, telefone, id))
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


    #metodo para excluir fornecedor
    @classmethod
    def delete(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM fornecedor WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()

    