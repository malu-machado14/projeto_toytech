CREATE DATABASE Toytech_bd;
USE Toytech_bd;

CREATE TABLE fornecedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14),
    telefone VARCHAR(20)
);

CREATE TABLE funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    email VARCHAR(50),
    senha VARCHAR(20),
    telefone VARCHAR(20) NOT NULL,
    cargo VARCHAR(30) NOT NULL
);

CREATE TABLE solicitador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14),
    senha VARCHAR(20),
    telefone VARCHAR(20)
);


CREATE TABLE localizacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rua VARCHAR(30),
    prateleira VARCHAR(30),
    andar VARCHAR(30)
    );


CREATE TABLE sensor (
  id INT AUTO_INCREMENT PRIMARY KEY,
  modelo_sensor VARCHAR(45),
  descricao_funcao_sensor TEXT,
  fornecedor_id INT NOT NULL,
  altura_sensor FLOAT,
  largura_sensor FLOAT,
  tipo VARCHAR(60),
  CONSTRAINT fk_fornecedor_sensor FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id)
);

CREATE TABLE dados_sensor (
  sensor_id INT NOT NULL,
  dados TEXT,
  CONSTRAINT fk_sensor_id FOREIGN KEY (sensor_id) REFERENCES sensor(id)
);

CREATE TABLE solicitacao_entrada (
    id_operacao_e INT AUTO_INCREMENT PRIMARY KEY,
    data_solicitacao_entrada DATETIME NOT NULL,
    funcionario_id INT NOT NULL,
    fornecedor_id INT NOT NULL,
    observacao VARCHAR(255),
    CONSTRAINT fk_funcionario_se FOREIGN KEY (funcionario_id) REFERENCES funcionario(id),
    CONSTRAINT fk_fornecedor_se FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id)
);


CREATE TABLE solicitacao_saida (
    id_operacao_s INT AUTO_INCREMENT PRIMARY KEY,
    data_solicitacao_saida DATETIME NOT NULL,
    observacao VARCHAR(255),
    funcionario_id INT NOT NULL,
    solicitador_id INT NOT NULL,
    CONSTRAINT fk_funcionario_ss FOREIGN KEY (funcionario_id) REFERENCES funcionario(id),
    CONSTRAINT fk_solicitador_ss FOREIGN KEY (solicitador_id) REFERENCES solicitador(id)
);

CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    fornecedor_id INT NOT NULL,
    localizacao_produto INT NOT NULL,
    imagem LONGBLOB,
    preco DECIMAL(10,2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_fornecedor_p FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id),
    CONSTRAINT fk_localizacao_pr FOREIGN KEY (localizacao_produto) REFERENCES localizacao(id)
);

CREATE TABLE estoque (
	estoque_id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    produto_quantidade INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES produto(id)
);

CREATE TABLE item_solicitacao_entrada (
    id_item_e INT AUTO_INCREMENT PRIMARY KEY,
    id_operacao_e INT(6),
    estoque_id INT(6),
    CONSTRAINT fk_solicitacao_entrada FOREIGN KEY (id_operacao_e) REFERENCES solicitacao_entrada(id_operacao_e), 
    CONSTRAINT fk_estoque_ise FOREIGN KEY (estoque_id) REFERENCES estoque(estoque_id)
);


CREATE TABLE item_solicitacao_saida (
    id_item_s INT AUTO_INCREMENT PRIMARY KEY,
    id_operacao_s INT(6),
    estoque_id INT(6),
	CONSTRAINT fk_solicitacao_saida FOREIGN KEY (id_operacao_s) REFERENCES solicitacao_saida(id_operacao_s),
    CONSTRAINT fk_estoque_iss FOREIGN KEY (estoque_id) REFERENCES estoque(estoque_id)
);
