USE `mydb` ;
DROP TRIGGER IF EXISTS delecao_post_passaro;
DROP TRIGGER IF EXISTS delecao_post_mencao;
DROP TRIGGER IF EXISTS delecao_post_vizualizacao;

DELIMITER //
CREATE TRIGGER delecao_post_passaro AFTER UPDATE ON Post
FOR EACH ROW
BEGIN
    IF NOT (New.Ativo <=> Old.Ativo) THEN
        UPDATE 
            Post_Passaro

        SET 
            Post_Passaro.Ativo = 'False'

        WHERE   
        Post_Passaro.Post_idPost = New.idPost;

    END IF;
END //

DELIMITER ##
CREATE TRIGGER delecao_post_mencao AFTER UPDATE ON Post
FOR EACH ROW
BEGIN
    IF NOT (New.Ativo <=> Old.Ativo) THEN
        UPDATE 
            User_mencao_Post
        SET 
            User_mencao_Post.Ativo = 'False'
        WHERE   
            User_mencao_Post.Post_idPost = New.idPost;
    END IF;
END ##


DELIMITER ||
CREATE TRIGGER delecao_post_vizualizacao AFTER UPDATE ON Post
FOR EACH ROW
BEGIN
    IF NOT (New.Ativo <=> Old.Ativo) THEN
        UPDATE 
            Post_visualizar_User
        SET 
            Post_visualizar_User.Ativo = 'False'
        WHERE   
            Post_visualizar_User.Post_idPost = New.idPost;
    END IF;
END ||