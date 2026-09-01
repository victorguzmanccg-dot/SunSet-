BEGIN;
--
-- Create model Mesa
--
CREATE TABLE "restaurante_mesa" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "numero" integer unsigned NOT NULL UNIQUE CHECK ("numero" >= 0), "capacidad" integer unsigned NOT NULL CHECK ("capacidad" >= 0), "estado" varchar(10) NOT NULL);
--
-- Create model Platillo
--
CREATE TABLE "restaurante_platillo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(100) NOT NULL, "descripcion" text NOT NULL, "precio" decimal NOT NULL, "categoria" varchar(10) NOT NULL, "disponible" bool NOT NULL, "imagen" varchar(100) NULL);
--
-- Create model Comanda
--
CREATE TABLE "restaurante_comanda" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "estado" varchar(10) NOT NULL, "total" decimal NOT NULL, "fecha" datetime NOT NULL, "mesero_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "mesa_id" bigint NOT NULL REFERENCES "restaurante_mesa" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model PerfilUsuario
--
CREATE TABLE "restaurante_perfilusuario" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rol" varchar(10) NOT NULL, "usuario_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model DetalleComanda
--
CREATE TABLE "restaurante_detallecomanda" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer unsigned NOT NULL CHECK ("cantidad" >= 0), "subtotal" decimal NOT NULL, "comanda_id" bigint NOT NULL REFERENCES "restaurante_comanda" ("id") DEFERRABLE INITIALLY DEFERRED, "platillo_id" bigint NOT NULL REFERENCES "restaurante_platillo" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Reserva
--
CREATE TABLE "restaurante_reserva" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fecha_hora" datetime NOT NULL, "num_personas" integer unsigned NOT NULL CHECK ("num_personas" >= 0), "estado" varchar(10) NOT NULL, "cliente_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "mesa_id" bigint NOT NULL REFERENCES "restaurante_mesa" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "restaurante_comanda_mesero_id_35c92b16" ON "restaurante_comanda" ("mesero_id");
CREATE INDEX "restaurante_comanda_mesa_id_120558f7" ON "restaurante_comanda" ("mesa_id");
CREATE INDEX "restaurante_detallecomanda_comanda_id_487a82c0" ON "restaurante_detallecomanda" ("comanda_id");
CREATE INDEX "restaurante_detallecomanda_platillo_id_15a8ff56" ON "restaurante_detallecomanda" ("platillo_id");
CREATE INDEX "restaurante_reserva_cliente_id_dd4f7c54" ON "restaurante_reserva" ("cliente_id");
CREATE INDEX "restaurante_reserva_mesa_id_d3291a31" ON "restaurante_reserva" ("mesa_id");
COMMIT;
