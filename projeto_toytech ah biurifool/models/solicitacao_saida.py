#imports
from core.crud import Crud
from core.conexao import Database


#classe que representa um sensor no sistema
class SolicitacaoSaida(Crud):
    table = "solicitacao_saida"
    #lista de campos da tabela
    fields = [
        "id_operacao_s",
        "data_solicitacao_saida",
        "observacao",
        "funcionario_id",
        "solicitador_id",
    ]

    def __init__(self, id_operacao_s, data_solicitacao_saida, observacao,funcionario_id,solicitador_id):
        self.id_operacao_s = id_operacao_s
        self.data_solicitacao_saida = data_solicitacao_saida
        self.observacao = observacao
        self.funcionario_id = funcionario_id
        self.solicitador_id = solicitador_id
        

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO solicitacao_saida
        (funcionario_id,observacao,solicitador_id)
        VALUES (%s,%s,%s)
        """
        valores = (
            self.funcionario_id,
            self.observacao,
            self.solicitador_id
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
            sql = "SELECT * FROM solicitacao_saida"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()