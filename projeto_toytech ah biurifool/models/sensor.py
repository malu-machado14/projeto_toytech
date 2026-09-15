#imports
from core.crud import Crud
from core.conexao import Database
from core.validar import Validador

#classe que representa um sensor no sistema
class Sensor(Crud):
    table = "sensor"
    #lista de campos da tabela
    fields = [
        "id",
        "modelo_sensor",
        "descricao_funcao_sensor",
        "fornecedor_id",
        "altura_sensor",
        "largura_sensor",
        "tipo"
    ]

    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, modelo_sensor, descricao_funcao_sensor, fornecedor_id, altura_sensor,
                 largura_sensor,tipo, id=None):
        #atribui os valores aos objetos
        self.id = id
        self.modelo_sensor = modelo_sensor
        self.descricao_funcao_sensor = descricao_funcao_sensor
        self.fornecedor_id = fornecedor_id
        self.altura_sensor = altura_sensor
        self.largura_sensor = largura_sensor
        self.tipo = tipo

    #valida os dados do produto
    def validate(self):
        #lista de possiveis erros
        erros = [
         Validador.required(self.modelo_sensor, "modelo_sensor"),
         Validador.required(self.descricao_funcao_sensor, "descricao_funcao_sensor"),
         Validador.required(self.altura_sensor, "altura_sensor"),
         Validador.required(self.largura_sensor, "largura_sensor"),
         Validador.required(self.tipo, "tipo"),
         Validador.not_have_scaracter(self.modelo_sensor, "modelo_sensor"),
         Validador.non_negative(self.descricao_funcao_sensor, "descricao_funcao_sensor"),
         Validador.non_negative(self.altura_sensor, "altura_sensor"),
         Validador.non_negative(self.largura_sensor, "largura_sensor"),
         Validador.not_have_scaracter(self.altura_sensor, "altura_sensor"),
         Validador.not_have_scaracter(self.largura_sensor, "largura_sensor"),
         Validador.not_have_number(self.tipo,"tipo"),
         Validador.not_have_scaracter(self.tipo,"tipo"),
         Validador.have_upper(self.modelo_sensor, "modelo_sensor")
        ]
        #retorna os erros
        return [erro for erro in erros if erro]
    
    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO sensor
        (modelo_sensor, descricao_funcao_sensor, altura_sensor, largura_sensor, fornecedor_id, tipo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            self.modelo_sensor,
            self.descricao_funcao_sensor,
            self.altura_sensor,
            self.largura_sensor,
            self.self.fornecedor_id,
            self.tipo
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

        sql = "SELECT * FROM sensor"
        cursor.execute(sql,)
        sensor = cursor.fetchall()

        cursor.close()
        conexao.close()
        return sensor

    #retorna sensores em ordem alfabetica
    @classmethod
    def find_by_name(cls, modelo_sensor):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM sensor WHERE modelo_sensor LIKE %s ORDER BY modelo_sensor"
            cursor.execute(sql, (f"%{modelo_sensor}%",))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def find_by_id(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM sensor WHERE id = %s"
        cursor.execute(sql, (id,))
        sensor = cursor.fetchone()

        cursor.close()
        conexao.close()
        return sensor        

    #metodo para atualizar a quantidade de sensor
    @classmethod
    def update(cls, modelo_sensor, descricao_funcao_sensor, altura_sensor, largura_sensor, tipo, id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE sensor SET modelo_sensor = %s, descricao_funcao_sensor = %s, altura_sensor = %s, largura_sensor = %s, tipo = %s WHERE id = %s"
            cursor.execute(sql, ( modelo_sensor, descricao_funcao_sensor, altura_sensor, largura_sensor, tipo, id))
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

    #metodo para deletar um sensor
    @classmethod
    def delete(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM sensor WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()
