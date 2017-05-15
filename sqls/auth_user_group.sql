--Super Usuario Staff ; username: admin ; password: root --
INSERT INTO "auth_user" ("password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES ('pbkdf2_sha256$20000$jnVso10F6use$MtoBpRTWfN9TJnAa5jsZkOpsHTS4FMExWkCO+NE0nJo=', '2016-5-30 18:38:02.053', 't', 'admin', '', '', '', 't', 't', '2016-5-19 21:54:57.233');


--Grupos Necesarios--
INSERT INTO "auth_group" ("name") VALUES ('pcin');
INSERT INTO "auth_group" ("name") VALUES ('empleado');
INSERT INTO "auth_group" ("name") VALUES ('administrador');
INSERT INTO "auth_group" ("name") VALUES ('configurador');
INSERT INTO "auth_group" ("name") VALUES ('recursos_humanos');
