#import

from core.conexao import Database
from core.crud import Crud
from core.validar import Validador

#classe que representa uma localizacao
class Localizacao(Crud):
    table = "localizacao"
    #lista de campos da tabela
    fields = [
        "id",
        "rua",
        "prateleira",
        "andar"
        
    ]
    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, id, rua, prateleira, andar):
        #atribui os valores aos objetos
        self.id = id
        self.rua = rua
        self.prateleira = prateleira
        self.andar = andar

    
    #valida os dados da localizacao
    def validate(self):
        erros = [
             Validador.non_negative(self.rua, "rua"),
             Validador.non_negative(self.prateleira, "prateleira"),
             Validador.non_negative(self.andar, "andar"),
             Validador.required(self.rua, "rua"),
             Validador.required(self.prateleira, "prateleira"),
             Validador.required(self.andar, "andar"),
            ]
        #retorna os erros
        return [erro for erro in erros if erro]

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO localizacao
        (rua, prateleira, andar)
        VALUES (%s, %s, %s)
        """
        valores = (
            self.rua,
            self.prateleira,
            self.andar
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

        sql = "SELECT * FROM localizacao"
        cursor.execute(sql,)
        localizacao = cursor.fetchall()

        cursor.close()
        conexao.close()
        return localizacao

    #metodo para listar localizacao
    @classmethod
    def find_by_name(cls, rua):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM localizacao WHERE rua  LIKE %s ORDER BY rua"
        cursor.execute(sql, (f"%{rua}%",))
        localizacao = cursor.fetchall()

        cursor.close()
        conexao.close()
        return localizacao
    
    #metodo para buscar o id da localizacao
    @classmethod
    def find_by_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM localizacao WHERE id = %s"
        cursor.execute(sql, (id,))
        localizacao = cursor.fetchone()

        cursor.close()
        conexao.close()
        return localizacao

    #metodo para atualizar localizacao
    @classmethod
    def update(cls, rua, prateleira, andar, id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE localizacao SET rua = %s, prateleira = %s, andar = %s WHERE id = %s"
            cursor.execute(sql, ( rua, prateleira, andar, id))
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


    #metodo para excluir localizacao
    @classmethod
    def delete(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM localizacao WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()