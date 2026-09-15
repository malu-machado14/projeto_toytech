from core.conexao import Database
from core.crud import Crud
from core.validar import Validador

#classe que representa um fornecedor no sistema
class Estoque(Crud):

    table = "estoque"
    #lista de campos da tabela
    fields = [
        "estoque_id",
        "produto_id",
        "produto_quantidade"
    ]
    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, estoque_id,produto_id=None, produto_quantidade = 0):
        #atribui os valores aos objetos
        self.estoque_id = estoque_id
        self.produto_id = produto_id
        self.produto_quantidade = produto_quantidade

    def validate(self):
        erros = [
             Validador.required(self.estoque_id, "estoque_id"),
             Validador.required(self.produto_id, "produto_id"),
             Validador.required(self.produto_quantidade, "produto_quantidade"),
             Validador.non_negative(self.estoque_id, "estoque_id"),
             Validador.non_negative(self.produto_id, "produto_id"),
             Validador.non_negative(self.produto_quantidade, "produto_quantidade")]
        return [erro for erro in erros if erro]
    
    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            INSERT INTO estoque
            (produto_id,produto_quantidade)
            VALUES (%s,%s) 
        """
        valores = (
            self.produto_id,
            self.produto_quantidade
        )

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()

    @classmethod
    def find_all_stock(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM estoque"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
    
    @classmethod
    def find_product_by_id_stock(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM estoque WHERE estoque_id = %s"
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()