DROP DATABASE IF EXISTS tranqueira;
CREATE DATABASE tranqueira;
USE tranqueira;

CREATE TABLE perigo (
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(20) UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE comida (
	id INT NOT NULL AUTO_INCREMENT,
	nome VARCHAR(30) UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE comida_perigo (
    id_comida INT NOT NULL,
    id_perigo INT NOT NULL,
    PRIMARY KEY (id_comida, id_perigo),
    CONSTRAINT fk_comida FOREIGN KEY (id_comida)
        REFERENCES comida (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_perigo FOREIGN KEY (id_perigo)
        REFERENCES perigo (id)
        ON DELETE CASCADE
)
