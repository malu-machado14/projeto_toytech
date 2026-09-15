#imports
from core.crud import Crud
from core.conexao import Database


#classe que representa um sensor no sistema
class ItemSolicitacaoSaida(Crud):
    table = "item_solicitacao_saida"
    #lista de campos da tabela
    fields = [
        "id_item_s",
        "id_operacao_s",
        "estoque_id"
    ]

    def __init__(self, id_item_s, id_operacao_s, estoque_id):
        self.id_item_s = id_item_s
        self.id_operacao_s = id_operacao_s
        self.estoque_id = estoque_id

    @classmethod
    def find_all_with_product(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT solicitacao_saida.id_operacao_s, item_solicitacao_saida.estoque_id FROM solicitacao_saida INNER JOIN item_solicitacao_saida ON solicitacao_saida.id_operacao_s = item_solicitacao_saida.id_operacao_s;"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO item_solicitacao_saida
        (id_operacao_s, estoque_id)
        VALUES (%s, %s)
        """
        valores = (
            self.id_operacao_s,
            self.estoque_id
        )

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()


    @classmethod
    def update(cls, produto_quantidade,produto_id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE estoque SET produto_quantidade= %s WHERE produto_id = %s"
            cursor.execute(sql, (produto_quantidade, produto_id))
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
