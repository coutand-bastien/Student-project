--                                       
--  CREATE USERS                                       
--

-- User (SELECT) some stuff on the user and right tables
CREATE USER 'worker_view'@'%' IDENTIFIED BY 'worker_view';

-- User (SELECT, INSERT, UPDATE) some stuff on the user and right tables
CREATE USER 'worker_add'@'%' IDENTIFIED BY 'worker_add';

-- User (SELECT, DELETE) some stuff on the user and right tables
CREATE USER 'worker_del'@'%' IDENTIFIED BY 'worker_del';

-- User for the app (SELECT, INSERT, DELETE, UPDATE) on the user and right tables
CREATE USER 'app'@'%' IDENTIFIED BY 'app';
GRANT ALL PRIVILEGES ON db_app.* TO 'app'@'%';

FLUSH PRIVILEGES;