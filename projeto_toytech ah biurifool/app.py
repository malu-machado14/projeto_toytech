from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.produto import Produto
from models.fornecedor import Fornecedor
from models.funcionario import Funcionario
from models.sensor import Sensor
from models.localizacao import Localizacao
from models.solicitador import Solicitador
from models.solicitacao_entrada import SolicitacaoEntrada
from models.solicitacao_saida import SolicitacaoSaida
from models.item_solicitacao_entrada import ItemSolicitacaoEntrada
from models.item_solicitacao_saida import ItemSolicitacaoSaida
from models.estoque import Estoque


app = Flask(__name__)
app.secret_key = "chave_secreta"


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_produto_form():
    return {
        "id": to_int(request.form.get("id", "").strip()),
        "nome": request.form.get("nome", "").strip(),
        "descricao": str(request.form.get("descricao", "").strip()),
        "localizacao_produto": to_int(request.form.get("nome", "").strip()),
        "fornecedor_id": to_int(request.form.get("nome", "").strip()),
        "imagem": str(request.form.get("imagem","").strip()),
        "preco": to_float(request.form.get("preco",0))
    }
def get_fornecedor_form():
    return {
        "id": to_int(request.form.get("id", "").strip()),
        "nome": request.form.get("nome", "").strip(),
        "cnpj": request.form.get("cnpj", "").strip(),
        "telefone": request.form.get("telefone","").strip()
    }

def get_funcionario_form():
    return {
        "id": to_int(request.form.get("id", "").strip()),
        "nome": request.form.get("nome", "").strip(),
        "cpf": request.form.get("cpf", "").strip(),
        "telefone": request.form.get("telefone","").strip(),
        "email": request.form.get("email", "").strip(),
        "senha": request.form.get("senha","").strip(),
        "cargo": request.form.get("cargo","").strip()
    }


def get_solicitador_form():
    return {
        "id": to_int(request.form.get("id", "").strip()),
        "nome": request.form.get("nome", "").strip(),
        "cnpj": request.form.get("cnpj", "").strip(),
        "telefone":request.form.get("telefone","").strip(),
        "senha": request.form.get("senha","").strip(),
    }

def get_sensor_form():
    return {
        "id": to_int(request.form.get("id","").strip()),
        "modelo_sensor": request.form.get("modelo_sensor", "").strip(),
        "descricao_funcao_sensor": request.form.get("descricao_funcao_sensor", "").strip(),
        "fornecedor_id": to_int(request.form.get("fornecedor_id","").strip()),
        "altura_sensor": request.form.get("altura_sensor", "").strip(),
        "largura_sensor": request.form.get("largura_sensor", "").strip(),
        "tipo": request.form.get("tipo","").strip(),    
    }

def get_localizacao_form():
    return {
        "id": to_int(request.form.get("id", "").strip()),
        "prateleira": request.form.get("prateleira", "").strip(),
        "andar": request.form.get("andar","").strip(),
        "rua": request.form.get("rua","").strip()
    }

def get_solicitacao_entrada_form():
    return {
        "id_operacao_e": to_int(request.form.get("id_operacao_e", "").strip()),
        "data_solicitacao_entrada": request.form.get("data_solicitacao_entrada", "").strip(),
        "id_funcionario": to_int(request.form.get("id_funcionario","").strip()),
        "id_fornecedor": to_int(request.form.get("id_fornecedor","").strip()),
        "observacao": str(request.form.get("observacao","").strip())
        }

def get_estoque_form():
    return{
        "estoque_id": to_int(request.form.get("estoque_id","").strip()),
        "produto_id": to_int(request.form.get("produto_id","").strip()),
        "produto_quantidade": to_int(request.form.get("produto_quantidade", "").strip())
    }

def get_item_solicitacao_entrada_form():
    return {
        "id_item_e": to_int(request.form.get("id_item_e", "").strip()),
        "id_operacao_e": to_int(request.form.get("id_operacao_e", "").strip()),
        "estoque_id": to_int(request.form.get("estoque_id","").strip())
    }

def get_solicitacao_saida_form():
    return {
        "id_operacao_s": to_int(request.form.get("id_operacao_s", "").strip()),
        "data_solicitacao_saida": request.form.get("data", "").strip(),
        "observacao": request.form.get("observacao","").strip(),
        "funcionario_id": to_int(request.form.get("funcionario_id","").strip()),
        "solicitador_id": to_int(request.form.get("solicitador_id","").strip())
    }

def get_item_solicitacao_saida_form():
    return {
        "id_item_s": to_int(request.form.get("id_item_s", "").strip()),
        "id_operacao_s": to_int(request.form.get("id_operacao_s", "").strip()),
        "estoque_id": to_int(request.form.get("estoque_id","").strip())
    }

EXTENSOES_PERMITIDAS = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


def imagem_permitida(tipo_arquivo):
    return tipo_arquivo in EXTENSOES_PERMITIDAS

@app.route("/")
def inicial():
    return render_template("loginbs.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        try:
            funcionario_dados = Funcionario.find_by_email(email)

            if funcionario_dados and funcionario_dados["senha"] == senha:
                session["funcionario_id"] = funcionario_dados["id"]
                session["funcionario_nome"] = funcionario_dados["nome"]
                session["funcionario_cargo"] = funcionario_dados["cargo"]
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Email ou senha inválidos, Você já se cadastrou?", "danger")
                return render_template("fun.html")
        except Exception as e:
            flash(f"erro ao tentar fazer login: {e}", "erro")
            return render_template("fun.html")
    return render_template("fun.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("inicial"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/produto/listar")
def listar_produto():
    return render_template("lista_produto.html", produtos=Produto.find_all())

@app.route("/produto/listar/<string:nome>")
def listar_produto_name(nome):
    return render_template("lista_produto.html", produtos=Produto.find_by_name(nome))

@app.route("/produto/listar/<float:preco>", methods = ["GET"])
def listar_produto_preco(preco):
    produto = Produto.find_by_price(preco)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("listar_produto"))
    return render_template("lista_produto.html", produto=produto)

@app.route("/produto/novo", methods = ["GET"])
def novo_produto():
    return render_template("produto.html", produto=None)

@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    dados = get_produto_form()
    produto = Produto(**dados)
    erros = produto.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("produto.html", produto=dados)

    try:
        produto.insert()
        flash("Produto cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listar_produto"))
    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "erro")
        return render_template("produto.html", produto=dados)

@app.route("/produto/listar/<int:id>", methods = ["GET"])
def listar_produto_id(id):
    produto = Produto.find_by_id(id)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("listar_produto"))
    return render_template("lista_produto.html", produto=produto)


@app.route("/produto/atualizar/<int:id>", methods=["POST"])
def atualizar_produto(id):
    dados = get_produto_form()
    dados["id"] = id
    dados["fornecedor_id"] = to_int(request.form.get("fornecedor_id"))
    dados["localizacao_produto"] = to_int(request.form.get("localizacao_produto"))

    produto = Produto(**dados)
    erros = produto.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("produto.html", produto=dados)

    try:
        if not Produto.find_by_id(id):
            flash("Produto não encontrado.", "erro")
            return redirect(url_for("listar_produto"))

        produto.update(
        dados["nome"], 
        dados["descricao"],  
        dados["imagem"],
        dados["preco"],
         id )
        flash("Produto atualizado com sucesso.", "sucesso")
        return redirect(url_for("listar_produto"))
    except Exception as e:
        flash(f"Erro ao atualizar produto: {e}", "erro")
        return render_template("produto.html", produto=dados)

@app.route("/produto/excluir/<int:id>", methods = ["POST"])
def excluir_produto(id):
    try:
        Produto.delete(id)
        flash("Produto excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "erro")
        return redirect(url_for("listar_produto"))
    
@app.route("/sensor/lista")
def listar_sensor():
    return render_template("lista_sensor.html", sensor=Sensor.find_all())

@app.route("/sensor/lista/<string:modelo_sensor>")
def listar_sensor_modelo(modelo_sensor):
    return render_template("lista_sensor.html", sensor=Sensor.find_by_name(modelo_sensor))

@app.route("/sensor/novo", methods = ["GET"])
def novo_sensor():
    return render_template("sensor.html", sensor=None)

@app.route("/sensor/salvar", methods=["POST"])
def salvar_sensor():
    dados = get_sensor_form()
    sensor = Sensor(**dados)
    erros = sensor.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("sensor.html", sensor=dados)

    try:
        sensor.insert()
        flash("O sensor foi cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listar_sensor"))
    except Exception as e:
        flash(f"Erro ao cadastrar o sensor: {e}", "erro")
        return render_template("sensor.html", sensor=dados)

@app.route("/sensor/listar/<int:id>", methods = ["GET"])
def listar_sensor_id(id):
    sensor = Sensor.find_by_id(id)
    if not sensor:
        flash("Sensor não encontrado.", "erro")
        return redirect(url_for("listar_sensor"))
    return render_template("lista_sensor.html", sensor=sensor)

@app.route("/sensor/atualizar/<int:id>", methods=["POST"])
def atualizar_sensor(id):
    dados = get_sensor_form()
    dados["id"] = id
    dados["fornecedor_id"] = to_int(request.form.get("fornecedor_id"))

    sensor = Sensor(**dados)
    erros = sensor.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("sensor.html", sensor=dados)

    try:
        if not Sensor.find_by_id(id):
            flash("Sensor não encontrado.", "erro")
            return redirect(url_for("listar_sensor"))

        sensor.update(
        dados["modelo_sensor"], 
        dados["descricao_funcao_sensor"], 
        dados["fornecedor_id"],
        dados["altura_sensor"], 
        dados["largura_sensor"], 
        dados["tipo"],id)
        flash("Sensor atualizado com sucesso.", "sucesso")
        return redirect(url_for("listar_sensor"))
    except Exception as e:
        flash(f"Erro ao atualizar sensor: {e}", "erro")
        return render_template("sensor.html", sensor=dados)

@app.route("/sensor/excluir/<int:id>", methods = ["POST"])
def excluir_sensor(id):
    try:
        Sensor.delete(id)
        flash("Sensor foi excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir o sensor: {e}", "erro")
    return redirect(url_for("listar_sensor"))

@app.route("/fornecedor/lista")
def listar_fornecedor():
    return render_template("lista_fornecedor.html", fornecedor=Fornecedor.find_all())

@app.route("/fornecedor/lista/<string:nome>")
def listar_fornecedor_nome(nome):
    return render_template("lista_fornecedor.html", fornecedor=Fornecedor.find_by_name(nome))

@app.route("/fornecedor/novo", methods = ["GET"])
def novo_fornecedor():
    return render_template("for.html", fornecedor=None)

@app.route("/fornecedor/listar/<int:id>", methods = ["GET"])
def findbyid_fornecedor(id):
    fornecedor = Fornecedor.find_by_id(id)

    if not fornecedor:
        return {"erro": "Fornecedor não encontrado"}, 404
    return render_template("lista_fornecedor.html")
        
@app.route("/fornecedor/salvar", methods=["POST"])
def salvar_fornecedor():
    dados = get_fornecedor_form()
    fornecedor = Fornecedor(**dados)
    erros = fornecedor.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("for.html", fornecedor=dados)

    try:
        fornecedor.insert()
        flash("Fornecedor cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listar_fornecedor"))
    except Exception as e:
        flash(f"Erro ao cadastrar fornecedor: {e}", "erro")
        return render_template("for.html", fornecedor=dados)


@app.route("/fornecedor/atualizar/<int:id>", methods=["POST"])
def atualizar_fornecedor(id):
    dados = get_fornecedor_form()
    dados["id"] = id 

    fornecedor = Fornecedor(**dados)
    erros = fornecedor.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("for.html", fornecedor=dados)

    try:
        if not Fornecedor.find_by_id(id):
            flash("Fornecedor não encontrado.", "erro")
            return redirect(url_for("listar_fornecedor"))

        fornecedor.update(
        dados["nome"], 
        dados["cnpj"], 
        dados["telefone"],id)
        flash("Fornecedor atualizado com sucesso.", "sucesso")
        return redirect(url_for("listar_fornecedor"))
    except Exception as e:
        flash(f"Erro ao atualizar fornecedor: {e}", "erro")
        return render_template("for.html", fornecedor=dados)

@app.route("/fornecedor/excluir/<int:id>", methods = ["POST"])
def excluir_fornecedor(id):
    try:
        Fornecedor.delete(id)
        flash("Fornecedor excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir fornecedor: {e}", "erro")
    return redirect(url_for("listar_fornecedor"))

@app.route("/funcionario/lista")
def listar_funcionario():
    return render_template("lista_funcionario.html", funcionario=Funcionario.find_all())

@app.route("/funcionario/lista/<string:nome>")
def listar_funcionario_nome(nome):
    return render_template("lista_funcionario.html", funcionario=Funcionario.find_by_name(nome))

@app.route("/funcionario/novo", methods = ["GET"])
def novo_funcionario():
    return render_template("fun.html", funcionario=None)

@app.route("/funcionario/<int:id>", methods = ["GET"])
def findbyid_funcionario(id):
    funcionario = Funcionario.find_by_id(id)

    if not funcionario:
        return {"erro": "Funcionario não encontrado"}, 404 
    return render_template("lista_funcionario.html", funcionario = Funcionario.find_by_id(id))

@app.route("/funcionario/salvar", methods=["POST"])
def salvar_funcionario():
    dados = get_funcionario_form()
    funcionario = Funcionario(**dados)
    erros = funcionario.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("fun.html", funcionario=dados)

    try:
        funcionario.insert()
        flash("Funcionario cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listar_funcionario"))
    except Exception as e:
        flash(f"Erro ao cadastrar funcionario: {e}", "erro")
        return render_template("fun.html", funcionario=dados)

@app.route("/funcionario/listar/<string:cargo>", methods = ["GET"])
def listar_cargo_funcionario(cargo):
    funcionario = Funcionario.find_by_cargo(cargo)
    if not funcionario:
        flash("Cargo de funcionario não encontrado.", "erro")
        return redirect(url_for("listar_funcionario"))
    return render_template("lista_funcionario.html", funcionario=funcionario)

@app.route("/funcionario/atualizar/<int:id>", methods=["POST"])
def atualizar_funcionario(id):
    dados = get_funcionario_form()
    dados["id"] = id

    funcionario = Funcionario(**dados)
    erros = funcionario.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("fun.html", funcionario=dados)

    try:
        if not Funcionario.find_by_id(id):
            flash("Funcionario não encontrado.", "erro")
            return redirect(url_for("listar_funcionario"))

        funcionario.update(
            dados["nome"], 
            dados["cpf"],  
            dados["email"], 
            dados["senha"],
            dados["telefone"],
            dados["cargo"], id)
        flash("Funcionario atualizado com sucesso.", "sucesso")
        return redirect(url_for("listar_funcionario"))
    except Exception as e:
        flash(f"Erro ao atualizar funcionario: {e}", "erro")
        return render_template("fun.html", funcionario=dados)
    
@app.route("/funcionario/excluir/<int:id>", methods = ["POST"])
def excluir_funcionario(id):
    try:
        Funcionario.delete(id)
        flash("Funcionario excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir funcionario: {e}", "erro")
    return redirect(url_for("listar_funcionario"))

@app.route("/solicitador/lista")
def listar_solicitador():
    return render_template("lista_solicitador.html", solicitador=Solicitador.find_all())

@app.route("/solicitador/lista/<string:nome>")
def listar_solicitador_nome(nome):
    return render_template("lista_solicitador.html", solicitador=Solicitador.find_by_name(nome))

@app.route("/solicitador/novo")
def novo_solicitador():
    return render_template("cad_sol.html")

@app.route("/solicitador/<int:id>", methods = ["GET"])
def findbyid_solicitador(id):
    solicitador = Solicitador.find_by_id(id)

    if not solicitador:
        return {"erro": "Solicitador não encontrado"}, 404
    return render_template("lista_solicitador.html")

@app.route("/solicitador/salvar", methods=["POST"])
def salvar_solicitador():
    dados = get_solicitador_form()
    solicitador = Solicitador(**dados)
    erros = solicitador.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("cad_sol.html", solicitador=dados)

    try:
        solicitador.insert()
        flash("Solicitador cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listar_solicitador"))
    except Exception as e:
        flash(f"Erro ao cadastrar solicitador: {e}", "erro")
        return render_template("cad_sol.html", solicitador=dados)

@app.route("/solicitador/listar/<int:id>", methods = ["GET"])
def listar_solicitador_id(id):
    solicitador = Solicitador.find_by_id(id)
    if not solicitador:
        flash("Solicitador não encontrado.", "erro")
        return redirect(url_for("listar_solicitador", solicitador = solicitador))
    return render_template("lista_solicitador.html", solicitador=solicitador)


@app.route("/solicitador/atualizar/<int:id>", methods=["POST"])
def atualizar_solicitador(id):
    dados = get_solicitador_form()
    dados["id"] = id

    solicitador = Solicitador(**dados)
    erros = solicitador.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("cad_sol.html", solicitador=dados)

    try:
        if not Solicitador.find_by_id(id):
            flash("Solicitador não foi encontrado.", "erro")
            return redirect(url_for("listar_solicitador"))

        solicitador.update(
        dados["nome"], 
        dados["cnpj"], 
        dados["telefone"],
        dados["senha"], id)
        flash("Solicitador atualizado com sucesso.", "sucesso")
        return redirect(url_for("listar_solicitador"))
    except Exception as e:
        flash(f"Erro ao atualizar solicitador: {e}", "erro")
        return render_template("cad_sol.html", solicitador=dados)

@app.route("/solicitador/excluir/<int:id>", methods = ["POST"])
def excluir_solicitador(id):
    try:
        Solicitador.delete(id)
        flash("Solicitador excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir solicitador: {e}", "erro")
    return redirect(url_for("listar_solicitador"))

@app.route("/localizacao/lista")
def listar_localizacao():
    return render_template("lista_localizacao.html", localizacao=Localizacao.find_all())

@app.route("/localizacao/lista/<string:rua>")
def listar_localizacao_rua(rua):
    return render_template("lista_localizacao.html", localizacao=Localizacao.find_by_name(rua))

@app.route("/localizacao/novo")
def nova_localizacao():
    return render_template("localizacao.html")

@app.route("/localizacao/salvar", methods=["POST"])
def salvar_localizacao():
    dados = get_localizacao_form()
    localizacao = Localizacao(**dados)
    erros = localizacao.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("localizacao.html", localizacao=dados)

    try:
        localizacao.insert()
        flash("Localização cadastrada com sucesso.", "sucesso")
        return redirect(url_for("listar_localizacao"))
    except Exception as e:
        flash(f"Erro ao cadastrar localizacao: {e}", "erro")
        return render_template("localizacao.html", localizacao=dados)

@app.route("/localizacao/listar/<int:id>", methods = ["GET"])
def listar_localizacao_id(id):
    localizacao = Localizacao.find_by_id(id)
    if not localizacao:
        flash("Localização não encontrada.", "erro")
        return redirect(url_for("listar_localizacao"))
    return render_template("lista_localizacao.html", localizacao=localizacao)

@app.route("/localizacao/atualizar/<int:id>", methods=["POST"])
def atualizar_localizacao(id):
    dados = get_localizacao_form()
    dados["id"] = id

    localizacao = Localizacao(**dados)
    erros = localizacao.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("localizacao.html", localizacao=dados)

    try:
        if not Localizacao.find_by_id(id):
            flash("Sensor não encontrado.", "erro")
            return redirect(url_for("listar_localizacao"))

        localizacao.update(
        dados["rua"], 
        dados["prateleira"], 
        dados["andar"],
        id)
        flash("Localização atualizada com sucesso.", "sucesso")
        return redirect(url_for("listar_localizacao"))
    except Exception as e:
        flash(f"Erro ao atualizar localização: {e}", "erro")
        return render_template("localizacao.html", localizacao=dados)

@app.route("/localizacao/excluir/<int:id>", methods = ["POST"])
def excluir_localizacao(id):
    try:
        Localizacao.delete(id)
        flash("Localização excluída com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir localização: {e}", "erro")
    return redirect(url_for("listar_localizacao"))

@app.route("/estoque", methods = ["GET"])
def listar_estoque():
   return render_template("lista_estoque.html", estoque=Estoque.find_all_stock())

@app.route("/estoque/salvar", methods=["POST"])
def salvar_estoque():
    dados = get_estoque_form()
    estoque = Estoque(**dados)
    erros = estoque.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("lista_estoque.html", estoque=dados)
    try:
        estoque.insert()
        flash("Campos do estoque cadastrados com sucesso.", "sucesso")
        return redirect(url_for("listar_estoque"))
    except Exception as e:
        flash(f"Erro ao cadastrar campos: {e}", "erro")
        return render_template("lista_estoque.html", estoque=dados)

@app.route("/estoque/lista/<int:produto_id>", methods = ["GET"])
def listar_produto_by_id(produto_id):
   return render_template("lista_estoque.html", estoque=Estoque.find_product_by_id_stock(produto_id))

@app.route("/solicitacao_entrada")
def listar_solicitacao_entrada():
    return render_template("mov_solicitacao_entrada.html", solicitacao_entrada=SolicitacaoEntrada.find_all_with_product())

@app.route("/solicitacao_entrada/novo", methods = ["GET"])
def novo_solicitacao_entrada():
    return render_template("mov_solicitacao_entrada.html", solicitacao_entrada=None)

@app.route("/solicitacao_entrada/salvar", methods=["POST"])
def salvar_solicitacao_entrada():
    dados = get_solicitacao_entrada_form()
    solicitacao_e = SolicitacaoEntrada(**dados)
    erros = solicitacao_e.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("mov_solicitacao_entrada.html", solicitacao_entrada=dados)

    try:
        solicitacao_e.insert()
        flash("Solicitação de entrada aceita com sucesso.", "sucesso")
        return redirect(url_for("solicitacao_entrada"))
    except Exception as e:
        flash(f"Erro ao solicitar entrada: {e}", "erro")
        return render_template("mov_solicitacao_entrada.html", solicitacao_entrada=dados)

@app.route("/solicitacao_saida")
def listar_solicitacao_saida():
    return render_template("mov_solicitacao_saida.html", solicitacao_saida=SolicitacaoSaida.find_all_with_product())

@app.route("/solicitacao_saida/novo", methods = ["GET"])
def novo_solicitacao_saida():
    return render_template("mov_solicitacao_saida.html", solicitacao_saida=None)

@app.route("/solicitacao_saida/salvar", methods=["POST"])
def salvar_solicitacao_saida():
    dados = get_solicitacao_saida_form()
    solicitacao_s = SolicitacaoSaida(**dados)
    erros = solicitacao_s.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("mov_solicitacao_saida.html", solicitacao_saida=dados)

    try:
        solicitacao_s.insert()
        flash("Solicitação de saida aceita com sucesso.", "sucesso")
        return redirect(url_for("solicitacao_saida"))
    except Exception as e:
        flash(f"Erro ao solicitar saida: {e}", "erro")
        return render_template("mov_solicitacao_saida.html", solicitacao_saida=dados)

@app.route("/item_solicitacao_entrada", methods = ["GET"])
def listar_itens_e():
   return render_template("mov_solicitacao_entrada.html", item_s_e=ItemSolicitacaoEntrada.find_all_with_product())

@app.route("/item_solicitacao_entrada/inserir", methods = ["POST"])
def inserir_itens():
    dados = get_item_solicitacao_entrada_form()
    item_s_entrada = ItemSolicitacaoEntrada(**dados)
    erros = item_s_entrada.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("mov_solicitacao_entrada.html", item_solicitacao_entrada=dados)
    try:
        item_s_entrada.insert()
        flash("Itens cadastrados com sucesso.", "sucesso")
        return redirect(url_for("listar_itens_e"))
    except Exception as e:
        flash(f"Erro ao cadastrar os itens {e}", "erro")
        return render_template("mov_solicitacao_entrada.html", item_solicitacao_entrada=dados)

'''@app.route("/item_solicitacao_entrada/atualizar/<int:id>", methods=["POST"])
def atualizar_itens(id_operacao_e):
    dados = get_sensor_form()
    dados["id_operacao_e"] = id_operacao_e
    dados["fornecedor_id"] = to_int(request.form.get("fornecedor_id"))
    dados["funcionario_id"] = to_int(request.form.get("funcionario_id"))

    item_solicitacao_e = ItemSolicitacaoEntrada(**dados)
    erros = item_solicitacao_e.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("mov_solicitacao_entrada.html", item_solicitacao_e=dados)

    try:
        if not ItemSolicitacaoEntrada.find_by_id(id_operacao_e):
            flash("Sensor não encontrado.", "erro")
            return redirect(url_for("listar_itens_e"))

        ItemSolicitacaoEntrada.update(id_operacao_e)
        flash("Sensor atualizado com sucesso.", "sucesso")
        return redirect(url_for("sensor"))
    except Exception as e:
        flash(f"Erro ao atualizar sensor: {e}", "erro")
        return render_template("sensor.html", sensor=dados)'''
    
@app.route("/item_solicitacao_saida", methods = ["GET"])
def listar_itens_s():
   return render_template("mov_solicitacao_saida.html", item_s_s=ItemSolicitacaoSaida.find_all_with_product())

@app.route("/item_solicitacao_saida/inserir", methods = ["POST"])
def inserir_itens_s():
    dados = get_item_solicitacao_saida_form()
    item_s_saida = ItemSolicitacaoSaida(**dados)
    erros = item_s_saida.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("mov_solicitacao_saida.html", item_solicitacao_saida=dados)
    try:
        item_s_saida.insert()
        flash("Itens cadastrados com sucesso.", "sucesso")
        return redirect(url_for("listar_itens_s"))
    except Exception as e:
        flash(f"Erro ao cadastrar os itens {e}", "erro")
        return render_template("mov_solicitacao_saida.html", item_solicitacao_saida=dados)

'''@app.route("/sensor/atualizar/<int:id>", methods=["POST"])
def atualizar_sensor(id):
    dados = get_sensor_form()
    dados["id"] = id
    dados["fornecedor_id"] = to_int(request.form.get("fornecedor_id"))

    sensor = Sensor(**dados)
    erros = sensor.validate()
    
    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("sensor.html", sensor=dados)

    try:
        if not Sensor.find_by_id(id):
            flash("Sensor não encontrado.", "erro")
            return redirect(url_for("sensor"))

        sensor.update(id)
        flash("Sensor atualizado com sucesso.", "sucesso")
        return redirect(url_for("sensor"))
    except Exception as e:
        flash(f"Erro ao atualizar sensor: {e}", "erro")
        return render_template("sensor.html", sensor=dados)'''

if __name__ == "__main__":
    app.run(debug=True)
''