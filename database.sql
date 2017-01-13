DROP DATABASE IF EXISTS mpc;
DELETE FROM mysql.user WHERE user = 'mpc';

CREATE DATABASE mpc default character set utf8 default collate utf8_general_ci;
GRANT ALL PRIVILEGES ON mpc.* TO mpc@localhost IDENTIFIED BY 'mpc' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON mpc.* TO mpc@"%" IDENTIFIED BY 'mpc' WITH GRANT OPTION;
UPDATE mysql.user SET Super_Priv='Y' WHERE user='mpc' AND host='%';
UPDATE mysql.user SET Super_Priv='Y' WHERE user='mpc' AND host='localhost';
FLUSH PRIVILEGES;