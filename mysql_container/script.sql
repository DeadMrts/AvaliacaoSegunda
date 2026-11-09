CREATE TABLE tarefas (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(120) NOT NULL);
INSERT INTO tarefas (titulo) VALUES ('Estudar volumes');
SELECT * FROM tarefas;
