CREATE TABLE usuario (
 id      SERIAL,
 nome    VARCHAR(30) NOT NULL,
 email   VARCHAR(256) UNIQUE NOT NULL,
 senha   CHAR(60) NOT NULL,
 PRIMARY KEY (id)
);

CREATE TABLE sessao (
 id    SERIAL,
 data_fim    TIMESTAMP,
 data_inicio    TIMESTAMP DEFAULT NOW(),
 usuario INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (id)
);

CREATE TABLE publicacao (
 id        SERIAL,
 titulo    VARCHAR(50) NOT NULL,
 subtitulo VARCHAR(60),
 texto     TEXT NOT NULL,
 data      DATE DEFAULT CURRENT_DATE,
 usuario   INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (id)
);

CREATE TABLE pergunta (
 id      SERIAL,
 texto   TEXT NOT NULL,
 data    DATE DEFAULT CURRENT_DATE,
 usuario INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (id)
);

CREATE TABLE resposta (
 id       SERIAL,
 texto    TEXT NOT NULL,
 data     DATE DEFAULT CURRENT_DATE,
 usuario  INT REFERENCES usuario(id) NOT NULL,
 pergunta INT REFERENCES pergunta(id) NOT NULL,
 PRIMARY KEY (id)
);

CREATE TABLE comentario (
 id         SERIAL,
 texto      TEXT NOT NULL,
 data       DATE DEFAULT CURRENT_DATE,
 usuario    INT REFERENCES usuario(id) NOT NULL,
 publicacao INT REFERENCES publicacao(id) NOT NULL,
 PRIMARY KEY (id)
);

CREATE TABLE anexo (
 id            SERIAL,
 nome          VARCHAR(50) NOT NULL,
 dados         BYTEA NOT NULL,
 posicao_texto INT NOT NULL,
 centralizacao CHAR(1) NOT NULL,
 extensao      VARCHAR(8),
 altura        SMALLINT,
 largura       SMALLINT,
 publicacao    INT REFERENCES publicacao(id),
 pergunta     INT REFERENCES pergunta(id),
 resposta    INT REFERENCES resposta(id),
 PRIMARY KEY (id)
);

CREATE TABLE positivo_publicacao (
 publicacao INT REFERENCES publicacao(id) NOT NULL,
 usuario    INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (publicacao, usuario)
);
CREATE TABLE positivo_comentario (
 comentario INT REFERENCES comentario(id) NOT NULL,
 usuario    INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (comentario, usuario)
);
CREATE TABLE positivo_pergunta (
 pergunta INT REFERENCES pergunta(id) NOT NULL,
 usuario  INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (pergunta, usuario)
);
CREATE TABLE positivo_resposta (
 resposta INT REFERENCES resposta(id) NOT NULL,
 usuario  INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (resposta, usuario)
);

CREATE TABLE favorita_publicacao (
 publicacao INT REFERENCES publicacao(id) NOT NULL,
 usuario    INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (publicacao, usuario)
);
CREATE TABLE favorita_pegunta (
 pergunta INT REFERENCES pergunta(id) NOT NULL,
 usuario  INT REFERENCES usuario(id) NOT NULL,
 PRIMARY KEY (pergunta, usuario)
);

INSERT INTO usuario(nome, email, senha) VALUES('joao', '189146@upf.br', 'senha');
INSERT INTO sessao(usuario) VALUES(1);
INSERT INTO pergunta(usuario, texto) VALUES(1, 'Como localizar a constelação de Orion?');
INSERT INTO pergunta(usuario, texto) VALUES(1, 'Quais planetas estão visíveis no céu nos meses de abril e maio?');
INSERT INTO resposta(pergunta, usuario, texto) VALUES(2, 1, 'Os planetas visíveis são X, Y e Z.');
SELECT * FROM usuario;
SELECT * FROM sessao;
SELECT * FROM pergunta;
SELECT * FROM resposta;
