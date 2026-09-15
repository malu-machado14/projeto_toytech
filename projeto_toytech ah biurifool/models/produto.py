#imports
from core.crud import Crud
from core.conexao import Database
from core.validar import Validador

#classe que representa o produto
class Produto(Crud):
    table = "produto"
    #lista de campos da tabela
    fields = [
        "id",
        "nome",
        "descricao",
        "fornecedor_id",
        "localizacao_produto",
        "imagem",
        "preco"
    ]

    #metodo para inicializar o objeto com valores iniciais
    def __init__(self, nome, descricao,
                 localizacao_produto, preco, fornecedor_id, imagem = None, id=None):
        #atribui os valores aos objetos
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.fornecedor_id = fornecedor_id
        self.localizacao_produto = localizacao_produto
        self.imagem = imagem
        self.preco = preco

    #valida os dados do produto
    def validate(self):
        #lista de possiveis erros
        erros = [
         Validador.required(self.nome, "nome"),
         Validador.required(self.descricao, "descricao"),
         Validador.non_negative(self.imagem, "imagem"),
         Validador.non_negative(self.preco, "preco"),
         Validador.not_have_upper(self.nome, "nome")
        ]
        #retorna os erros
        return [erro for erro in erros if erro]

    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO produto
        (nome, descricao, imagem, preco, fornecedor_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            self.nome,
            self.descricao,
            self.imagem,
            self.preco,
            self.fornecedor_id
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

        sql = "SELECT * FROM produto"
        cursor.execute(sql,)
        produto = cursor.fetchall()

        cursor.close()
        conexao.close()
        return produto

    @classmethod
    def find_by_name(cls, nome):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produto WHERE nome LIKE %s ORDER BY nome"
        cursor.execute(sql, (f"%{nome}%",))
        produto = cursor.fetchall()

        cursor.close()
        conexao.close()
        return produto
    
    @classmethod
    def find_by_price(cls, preco):
        #conexao com o banco
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produto WHERE preco = %s ORDER BY preco"
        cursor.execute(sql, (f"%{preco}%",))
        produto = cursor.fetchall()

        cursor.close()
        conexao.close()
        return produto

    @classmethod
    def find_by_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produto WHERE id = %s"
        cursor.execute(sql, (id,))
        produto = cursor.fetchone()

        cursor.close()
        conexao.close()
        return produto

#metodo para atualizar um produto

    @classmethod
    def update(cls, nome, descricao, imagem, preco, id, connection=None):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE produto SET nome = %s, descricao = %s,imagem = %s, preco = %s WHERE id = %s"
            cursor.execute(sql, ( nome, descricao, imagem, preco, id))
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

    #metodo para deletar um produto
    @classmethod
    def delete(cls,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM produto WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()