#imports
from core.crud import Crud
from core.conexao import Database


#classe que representa um sensor no sistema
class ItemSolicitacaoEntrada(Crud):
    table = "item_solicitacao_entrada"
    #lista de campos da tabela
    fields = [
        "id_item_e",
        "id_operacao_e",
        "estoque_id"
    ]

    def __init__(self, id_item_e, id_operacao_e, estoque_id):
        self.id_item_e = id_item_e
        self.id_operacao_e = id_operacao_e
        self.estoque_id= estoque_id

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO item_solicitacao_entrada
        (id_operacao_e, estoque_id)
        VALUES (%s, %s)
        """
        valores = (
            self.id_operacao_e,
            self.estoque_id
        )

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()

    @classmethod
    def find_all_with_product(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT solicitacao_entrada.id_operacao_e,item_solicitacao_entrada.estoque_id FROM solicitacao_entrada INNER JOIN item_solicitacao_entrada ON solicitacao_entrada.id_operacao_e = item_solicitacao_entrada.id_operacao_e;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def update(cls,produto_quantidade,estoque_id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE estoque SET produto_quantidade = %s WHERE estoque_id = %s"
            cursor.execute(sql, (produto_quantidade, estoque_id))
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
