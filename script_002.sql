USE `mydb` ;

ALTER TABLE User_mencao_Post
ADD COLUMN Ativo VARCHAR(45) NOT NULL;

ALTER TABLE Post_Passaro
ADD COLUMN Ativo VARCHAR(45) NOT NULL;

ALTER TABLE Post_visualizar_User
ADD COLUMN Ativo VARCHAR(45) NOT NULL;




