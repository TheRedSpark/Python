CREATE TABLE `Selma`.`Users` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `User_Id` INT NULL,
  `Username` VARCHAR(45) NULL,
  `Username_Selma` VARCHAR(100) NULL,
  `Password_Selma` VARCHAR(150) NULL,
  `Email` VARCHAR(150) NULL,
  `Results_Num` SMALLINT NULL DEFAULT 0,
  `Results_Update` TINYINT NULL DEFAULT 0,
  `Speichern_Prüfungen` TINYINT NULL DEFAULT 0,
  `Push` TINYINT NULL DEFAULT 0,
  `Push_Toggle` TINYINT NULL DEFAULT 1,
  PRIMARY KEY (`idUser`));