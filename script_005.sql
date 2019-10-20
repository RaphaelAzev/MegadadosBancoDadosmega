USE `mydb` ;

CREATE TABLE IF NOT EXISTS `mydb`.`usuario_curte_post` (
  `User_idUser` INT NOT NULL,
  `Post_idPost` INT NOT NULL,
  `estado` INT NOT NULL,
  PRIMARY KEY (`User_idUser`, `Post_idPost`),
  INDEX `fk_usuario_curte_post_Post1_idx` (`Post_idPost` ASC) VISIBLE,
  INDEX `fk_usuario_curte_post_User1_idx` (`User_idUser` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_curte_post_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `mydb`.`User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_usuario_curte_post_Post1`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `mydb`.`Post` (`idPost`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
