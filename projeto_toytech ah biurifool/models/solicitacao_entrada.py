#imports
from core.crud import Crud
from core.conexao import Database

#classe que representa um sensor no sistema
class SolicitacaoEntrada(Crud):
    table = "solicitacao_entrada"
    #lista de campos da tabela
    fields = [
        "id_operacao_e",
        "data_solicitacao_entrada",
        "funcionario_id",
        "fornecedor_id",
        "observacao",
    ]

    def __init__(self, id_operacao_e, data_solicitacao_entrada, funcionario_id, fornecedor_id, observacao=None):
        self.id_operacao_e = id_operacao_e
        self.data_solicitacao_entrada = data_solicitacao_entrada
        self.funcionario_id = funcionario_id
        self.fornecedor_id = fornecedor_id
        self.observacao = observacao

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO solicitacao_entrada
        (funcionario_id,fornecedor_id,observacao)
        VALUES (%s,%s,%s)
        """
        valores = (
            self.funcionario_id,
            self.fornecedor_id,
            self.observacao
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
            sql = "SELECT * FROM solicitacao_entrada"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()