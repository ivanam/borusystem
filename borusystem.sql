SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


TRUNCATE TABLE `administrador_permisosvistas`;
TRUNCATE TABLE `altacarta_carta`;
INSERT INTO `altacarta_carta` (`id`, `nombre`, `vigente`, `fecha`) VALUES
(1, 'Boru carta generica', 1, '2013-11-21');

TRUNCATE TABLE `altacarta_carta_secciones`;
INSERT INTO `altacarta_carta_secciones` (`id`, `carta_id`, `seccioncarta_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 7),
(8, 1, 8),
(9, 1, 9),
(10, 1, 10),
(11, 1, 11),
(12, 1, 12),
(13, 1, 13),
(14, 1, 14),
(15, 1, 15),
(16, 1, 16),
(17, 1, 17),
(18, 1, 18);

TRUNCATE TABLE `altacarta_seccioncarta`;
INSERT INTO `altacarta_seccioncarta` (`id`, `nombre`, `categoria`, `activo`, `cartavigente_id`, `imagen`) VALUES
(1, 'Picadas', 'P', 1, 1, 'platos.png'),
(2, 'Pizzas', 'P', 1, 1, 'pizzas.png'),
(3, 'Vinos Blancos', 'B', 1, 1, 'vinos.png'),
(4, 'Porron 330cm', 'B', 1, 1, 'bebidas.png'),
(5, 'Cerveza Tirada', 'B', 1, 1, 'cervezas.png'),
(6, 'Gaseosas', 'B', 1, 1, 'gaseosas.png'),
(7, 'Aguas y Jugos', 'B', 1, 1, 'jugos.png'),
(8, 'Menues del Dia', 'D', 1, 1, 'default.png'),
(9, 'Menues Ejecutivos', 'E', 1, 1, 'default.png'),
(10, 'Ensaladas', 'P', 1, 1, 'default.png'),
(11, 'Vino Tinto', 'B', 1, 1, 'vinos.png'),
(12, 'Clasiqueros', 'P', 1, 1, 'platos.png'),
(13, 'Pescados', 'P', 1, 1, 'pescados.png'),
(14, 'Postres', 'P', 1, 1, 'postres.png'),
(15, 'Bien Argentino', 'P', 1, 1, 'default.png'),
(16, 'Verano 2013', 'P', 1, 1, 'platoscalientes.png'),
(17, 'Tragos', 'B', 1, 1, 'copas.png'),
(18, 'clasicos', 'P', 1, 1, 'default.png');

TRUNCATE TABLE `altacarta_seccioncarta_bebidas`;
INSERT INTO `altacarta_seccioncarta_bebidas` (`id`, `seccioncarta_id`, `bebida_id`) VALUES
(21, 3, 21),
(22, 3, 22),
(23, 3, 23),
(24, 3, 24),
(12, 4, 12),
(13, 4, 13),
(14, 4, 14),
(15, 4, 15),
(16, 4, 16),
(17, 4, 17),
(18, 4, 18),
(19, 4, 19),
(20, 4, 20),
(1, 5, 1),
(3, 5, 3),
(9, 5, 9),
(10, 5, 10),
(11, 5, 11),
(2, 6, 2),
(30, 6, 30),
(31, 6, 31),
(4, 7, 4),
(5, 7, 5),
(6, 7, 6),
(7, 7, 7),
(8, 7, 8),
(25, 11, 25),
(26, 11, 26),
(27, 11, 27),
(28, 11, 28),
(29, 11, 29),
(32, 17, 32),
(33, 17, 33),
(34, 17, 34),
(35, 17, 35),
(36, 17, 36),
(37, 17, 37),
(38, 17, 38),
(39, 17, 39),
(40, 17, 40),
(41, 17, 41),
(42, 17, 42);

TRUNCATE TABLE `altacarta_seccioncarta_menuesd`;
INSERT INTO `altacarta_seccioncarta_menuesd` (`id`, `seccioncarta_id`, `deldia_id`) VALUES
(1, 8, 1),
(2, 8, 2),
(3, 8, 3);

TRUNCATE TABLE `altacarta_seccioncarta_menuese`;
INSERT INTO `altacarta_seccioncarta_menuese` (`id`, `seccioncarta_id`, `ejecutivo_id`) VALUES
(1, 9, 1);

TRUNCATE TABLE `altacarta_seccioncarta_platoss`;
INSERT INTO `altacarta_seccioncarta_platoss` (`id`, `seccioncarta_id`, `plato_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(3, 2, 3),
(28, 2, 28),
(29, 2, 29),
(30, 2, 30),
(31, 2, 31),
(32, 2, 32),
(33, 2, 33),
(34, 2, 34),
(35, 2, 35),
(36, 2, 36),
(37, 2, 37),
(38, 2, 38),
(39, 2, 39),
(40, 2, 40),
(10, 10, 10),
(11, 10, 11),
(12, 10, 12),
(13, 10, 13),
(14, 10, 14),
(15, 10, 15),
(16, 10, 16),
(17, 10, 17),
(18, 12, 18),
(19, 12, 19),
(7, 13, 7),
(8, 13, 8),
(9, 13, 9),
(46, 14, 46),
(47, 14, 47),
(48, 14, 48),
(49, 14, 49),
(50, 14, 50),
(51, 14, 51),
(41, 15, 41),
(42, 15, 42),
(43, 15, 43),
(44, 15, 44),
(45, 15, 45),
(20, 16, 20),
(21, 16, 21),
(22, 16, 22),
(23, 16, 23),
(24, 16, 24),
(25, 16, 25),
(26, 16, 26),
(27, 16, 27);

TRUNCATE TABLE `altamesa_mesa`;
INSERT INTO `altamesa_mesa` (`id`, `tipo`, `capacidad`, `ocupada`, `activo`, `sector_id`) VALUES
(1, '3', '10', 0, 1, 1),
(2, '2', '5', 0, 1, 1),
(3, '1', '3', 0, 1, 2),
(4, '2', '6', 0, 1, 2),
(5, '3', '8', 0, 1, 3),
(6, '2', '2', 0, 1, 3),
(7, '2', '4', 0, 1, 4),
(8, '3', '6', 0, 1, 4),
(9, '3', '8', 0, 1, 5),
(10, '2', '3', 0, 1, 5),
(11, '2', '4', 0, 1, 5),
(12, '2', '5', 0, 1, 5),
(13, '3', '15', 1, 1, 6),
(14, '2', '5', 0, 1, 6),
(15, '1', '5', 0, 1, 6),
(16, '2', '5', 0, 1, 3);




TRUNCATE TABLE `altamesa_sector`;
INSERT INTO `altamesa_sector` (`id`, `descripcion`, `tipo`, `activo`) VALUES
(1, 'Sector 1', 'NF', 0),
(2, 'Sector 2', 'NF', 1),
(3, 'Sector 3', 'F', 1),
(4, 'Sector 4', 'F', 1),
(5, 'Sector 5', 'NF', 1),
(6, 'Sector Vip', 'NF', 1);

TRUNCATE TABLE `altamesa_sector_mesas`;
TRUNCATE TABLE `auth_group`;
TRUNCATE TABLE `auth_group_permissions`;
TRUNCATE TABLE `auth_permission`;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add log entry', 7, 'add_logentry'),
(20, 'Can change log entry', 7, 'change_logentry'),
(21, 'Can delete log entry', 7, 'delete_logentry'),
(22, 'Can add permisos vistas', 8, 'add_permisosvistas'),
(23, 'Can change permisos vistas', 8, 'change_permisosvistas'),
(24, 'Can delete permisos vistas', 8, 'delete_permisosvistas'),
(25, 'Es Administrador', 8, 'is_admin'),
(26, 'Es Cajero', 8, 'is_cajero'),
(27, 'Es Mozo', 8, 'is_mozo'),
(28, 'Can add plato', 9, 'add_plato'),
(29, 'Can change plato', 9, 'change_plato'),
(30, 'Can delete plato', 9, 'delete_plato'),
(31, 'Can add bebida', 10, 'add_bebida'),
(32, 'Can change bebida', 10, 'change_bebida'),
(33, 'Can delete bebida', 10, 'delete_bebida'),
(34, 'Can add del dia', 11, 'add_deldia'),
(35, 'Can change del dia', 11, 'change_deldia'),
(36, 'Can delete del dia', 11, 'delete_deldia'),
(37, 'Can add ejecutivo', 12, 'add_ejecutivo'),
(38, 'Can change ejecutivo', 12, 'change_ejecutivo'),
(39, 'Can delete ejecutivo', 12, 'delete_ejecutivo'),
(40, 'Can add seccion carta', 13, 'add_seccioncarta'),
(41, 'Can change seccion carta', 13, 'change_seccioncarta'),
(42, 'Can delete seccion carta', 13, 'delete_seccioncarta'),
(43, 'Can add carta', 14, 'add_carta'),
(44, 'Can change carta', 14, 'change_carta'),
(45, 'Can delete carta', 14, 'delete_carta'),
(46, 'Can add sector', 15, 'add_sector'),
(47, 'Can change sector', 15, 'change_sector'),
(48, 'Can delete sector', 15, 'delete_sector'),
(49, 'Can add mesa', 16, 'add_mesa'),
(50, 'Can change mesa', 16, 'change_mesa'),
(51, 'Can delete mesa', 16, 'delete_mesa'),
(52, 'Can add personal', 17, 'add_personal'),
(53, 'Can change personal', 17, 'change_personal'),
(54, 'Can delete personal', 17, 'delete_personal'),
(55, 'Can add detalle comanda', 18, 'add_detallecomanda'),
(56, 'Can change detalle comanda', 18, 'change_detallecomanda'),
(57, 'Can delete detalle comanda', 18, 'delete_detallecomanda'),
(58, 'Can add comanda', 19, 'add_comanda'),
(59, 'Can change comanda', 19, 'change_comanda'),
(60, 'Can delete comanda', 19, 'delete_comanda'),
(61, 'Can add detalle preticket', 20, 'add_detallepreticket'),
(62, 'Can change detalle preticket', 20, 'change_detallepreticket'),
(63, 'Can delete detalle preticket', 20, 'delete_detallepreticket'),
(64, 'Can add preticket', 21, 'add_preticket'),
(65, 'Can change preticket', 21, 'change_preticket'),
(66, 'Can delete preticket', 21, 'delete_preticket'),
(67, 'Can add detalle pago', 22, 'add_detallepago'),
(68, 'Can change detalle pago', 22, 'change_detallepago'),
(69, 'Can delete detalle pago', 22, 'delete_detallepago'),
(70, 'Can add pago', 23, 'add_pago'),
(71, 'Can change pago', 23, 'change_pago'),
(72, 'Can delete pago', 23, 'delete_pago'),
(73, 'Can add detalle factura', 24, 'add_detallefactura'),
(74, 'Can change detalle factura', 24, 'change_detallefactura'),
(75, 'Can delete detalle factura', 24, 'delete_detallefactura'),
(76, 'Can add factura', 25, 'add_factura'),
(77, 'Can change factura', 25, 'change_factura'),
(78, 'Can delete factura', 25, 'delete_factura');

TRUNCATE TABLE `auth_user`;
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `direccion`, `telefono`, `tipoDoc`, `numeroDoc`, `turno`) VALUES
(1, 'pbkdf2_sha256$10000$1tUhq87KigNF$fPbwQXZXoeA2Be5Qf7Hb7YJB8GaE5oVxu6yHGZOx75E=', '2013-12-30 13:33:17', 1, 'admin', '', '', 'admin@admin.com', 1, 1, '2013-12-01 13:25:06', NULL, NULL, 'DNI', NULL, 'Noche'),
(4, 'pbkdf2_sha256$10000$Q7eVPlNJRvSI$XDfpBaM4i8JCusBHZSVIOJPG4fyKm7UULcy1xgjfDq0=', '2013-12-17 12:23:35', 0, 'andres', 'Andres', 'Martinovic', 'andres@hotmail.com', 0, 1, '2013-12-02 18:38:14', NULL, NULL, 'DNI', NULL, 'Noche'),
(5, 'pbkdf2_sha256$10000$19Ms1UoaNssI$Ar5eg4iehFrpSuMHrT2zXe/dvmpxN9SZrLlCYciDGzc=', '2013-12-02 19:03:37', 0, 'walter', 'Walter', 'Etchart', 'walter@hotmail.com', 0, 1, '2013-12-02 18:38:37', NULL, NULL, 'DNI', NULL, 'Noche'),
(6, 'pbkdf2_sha256$10000$2XK38sioP1X1$QAgQy2qK4QKiGtK19aU4PetU7BbrwQ77j69cAovZ5dY=', '2013-12-03 05:01:40', 0, 'ivana', 'Ivana', 'Moyano', 'ivana@hotmail.com', 0, 1, '2013-12-02 18:38:59', NULL, NULL, 'DNI', NULL, 'Noche'),
(7, 'pbkdf2_sha256$10000$bIu4SBBTXOTs$FvRiUje0WBqiVuTrj2zc0+lOh2h9+95HHWLHR3AZNjs=', '2013-12-26 09:37:02', 0, 'gaston', 'Gaston', 'Mura', 'gaston@hotmail.com', 0, 1, '2013-12-02 18:43:13', 'Los aromos 232', '4422306', 'DNI', '27042881', 'Noche'),
(8, 'pbkdf2_sha256$10000$MQZbn6lLq2dy$D4bsskCQVOZj4F9754np/iPkEzAiAjQjaY+qcpwRx5U=', '2013-12-02 18:44:02', 0, 'jose', 'Jose', 'Marrone', 'jose@hotmail.com', 0, 1, '2013-12-02 18:44:02', 'Italia 21', '4455789', 'DNI', '21055887', 'Tarde'),
(9, 'pbkdf2_sha256$10000$JhjOgmVM6kwA$L5LH4/Pd5pajqNQuDzrI50/1rjv2lsuw3duCUhgNmPs=', '2013-12-03 05:01:14', 0, 'mozo', 'Mozo', 'Boru', 'mozo@hotmail.com', 0, 1, '2013-12-02 18:44:58', 'Belgrano 125', '44444444444', 'DNI', '11111111', 'Tarde'),
(10, 'pbkdf2_sha256$10000$hjE32g18Dep1$R9fSsoDERYKt3SgOzTIThgjFsryYC85YUfP0HVb/Isw=', '2013-12-02 18:46:33', 0, 'ivanam', 'ivana', 'moyano', 'ivana@hotmail.com', 0, 1, '2013-12-02 18:46:33', 'San martin 145', '44785214', 'DNI', '33145789', 'Noche'),
(11, 'pbkdf2_sha256$10000$vLxX4kls4kMK$Anm6s0ohBlmFJJR+Kt1Lp+rQFcsORBDXRFXgXTBRexc=', '2013-12-02 19:03:46', 0, 'walterm', 'Walter', 'Etchart', 'walter@hotmail.com', 0, 0, '2013-12-02 18:47:10', 'Martin Fierro 1457', '15478965', 'DNI', '36145789', 'Noche'),
(12, 'pbkdf2_sha256$10000$ooGPTfI1FDe2$S43bAvybdeSAr/wWiUziu5ffJVPZ20esaIQP6o8wdqs=', '2013-12-02 18:48:00', 0, 'andresm', 'Andres', 'Martinovic', 'andres@hotmail.com', 0, 1, '2013-12-02 18:48:00', 'Novaro 145', '154789654', 'DNI', '36457892', 'Tarde'),
(13, '1234', '2013-12-03 20:46:56', 0, 'claudio', 'claudio', 'jaramillo', 'admin@admin.com', 0, 1, '2013-12-03 20:46:56', 'Centro de computos', '256447854', 'DNI', '12345678', 'Noche');

TRUNCATE TABLE `auth_user_groups`;
TRUNCATE TABLE `auth_user_user_permissions`;
INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(5, 4, 25),
(4, 5, 26),
(3, 6, 26),
(6, 7, 27),
(7, 8, 27),
(8, 9, 27),
(9, 10, 27),
(10, 11, 27),
(11, 12, 27),
(12, 13, 27);

TRUNCATE TABLE `comanda_comanda`;
INSERT INTO `comanda_comanda` (`id`, `tipo_comanda`, `fecha`, `hora`, `cantidadC`, `mozo_id`, `vista`, `finalizada`, `cerrada`, `factura_id`, `preticket_id`) VALUES
(1, 'C', '2013-12-03', '17:52:16', '4', 1, 1, 1, 1, NULL, 1),
(2, 'P', '2013-12-03', '05:55:17', '5', 1, 1, 1, 1, 2, NULL),
(4, 'P', '2013-12-03', '05:59:19', '4', 1, 0, 0, 0, NULL, NULL),
(5, 'C', '2013-12-09', '10:23:57', '4', 1, 1, 1, 1, NULL, 2),
(7, 'C', '2013-12-09', '10:28:55', '1', 1, 0, 0, 0, NULL, NULL),
(8, 'C', '2013-12-09', '10:31:51', '1', 1, 0, 0, 0, NULL, NULL),
(9, 'C', '2013-12-17', '09:12:13', '7', 1, 1, 1, 1, NULL, 3),
(10, 'P', '2013-12-26', '06:37:23', '4', 7, 1, 1, 1, 5, NULL);

TRUNCATE TABLE `comanda_comanda_detalles`;
INSERT INTO `comanda_comanda_detalles` (`id`, `comanda_id`, `detallecomanda_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 2, 4),
(5, 5, 5),
(6, 5, 6),
(7, 5, 7),
(8, 5, 8),
(9, 9, 9),
(10, 9, 10),
(11, 10, 11),
(12, 10, 12),
(13, 10, 13),
(14, 10, 14),
(15, 10, 15),
(16, 10, 16),
(17, 10, 17),
(18, 10, 18);

TRUNCATE TABLE `comanda_comanda_mesas`;
INSERT INTO `comanda_comanda_mesas` (`id`, `comanda_id`, `mesa_id`) VALUES
(2, 1, 2),
(1, 1, 5),
(3, 2, 11),
(4, 2, 12),
(6, 5, 3),
(7, 5, 10),
(5, 5, 16),
(8, 9, 1),
(9, 10, 2);

TRUNCATE TABLE `comanda_detallecomanda`;
INSERT INTO `comanda_detallecomanda` (`id`, `cantidadP`, `entregado`, `platos_id`, `bebidas_id`, `menuD_id`, `menuE_id`, `precioXunidad`, `descuento`) VALUES
(1, '2', 0, 18, NULL, NULL, NULL, '95.00', NULL),
(2, '2', 0, 19, NULL, NULL, NULL, '85.00', NULL),
(3, '3', 0, NULL, 3, NULL, NULL, '64.80', '10'),
(4, '2', 0, NULL, 10, NULL, NULL, '45.00', NULL),
(5, '1', 0, NULL, NULL, NULL, 1, '285.00', '0'),
(6, '1', 0, NULL, NULL, 3, NULL, '150.00', '0'),
(7, '1', 0, NULL, 12, NULL, NULL, '25.00', NULL),
(8, '1', 0, NULL, 14, NULL, NULL, '35.00', NULL),
(9, '1', 0, 41, NULL, NULL, NULL, '75.00', NULL),
(10, '2', 0, 42, NULL, NULL, NULL, '150.00', NULL),
(11, '1', 0, NULL, 4, NULL, NULL, '25.00', NULL),
(12, '1', 0, NULL, 8, NULL, NULL, '25.00', NULL),
(13, '1', 0, NULL, 1, NULL, NULL, '9.00', '10'),
(14, '1', 0, NULL, 30, NULL, NULL, '15.00', NULL),
(15, '1', 0, NULL, 31, NULL, NULL, '13.00', NULL),
(16, '1', 0, NULL, 12, NULL, NULL, '25.00', NULL),
(17, '1', 0, NULL, 15, NULL, NULL, '45.00', NULL),
(18, '1', 0, NULL, 17, NULL, NULL, '45.00', NULL);

TRUNCATE TABLE `comanda_detallefactura`;
INSERT INTO `comanda_detallefactura` (`id`, `cantidad`, `precioXunidad`, `detalleComanda_id`, `detallePreticket_id`, `descuento`) VALUES
(1, '2', '95.00', NULL, 1, NULL),
(2, '2', '85.00', NULL, 2, NULL),
(3, '3', '64.80', 3, NULL, '10'),
(4, '2', '45.00', 4, NULL, NULL),
(5, '1', '285.00', NULL, 3, '0'),
(6, '1', '150.00', NULL, 4, '0'),
(7, '1', '25.00', NULL, 5, NULL),
(8, '1', '35.00', NULL, 6, NULL),
(9, '1', '75.00', NULL, 7, NULL),
(10, '2', '150.00', NULL, 8, NULL),
(11, '1', '25.00', 11, NULL, NULL),
(12, '1', '25.00', 12, NULL, NULL),
(13, '1', '9.00', 13, NULL, '10'),
(14, '1', '15.00', 14, NULL, NULL),
(15, '1', '13.00', 15, NULL, NULL),
(16, '1', '25.00', 16, NULL, NULL),
(17, '1', '45.00', 17, NULL, NULL),
(18, '1', '45.00', 18, NULL, NULL);

TRUNCATE TABLE `comanda_detallepago`;
INSERT INTO `comanda_detallepago` (`id`, `importe`, `tipoPago`) VALUES
(1, '360.00', 'E'),
(2, '284.40', 'E'),
(3, '495.00', 'E'),
(4, '375.00', 'E'),
(5, '202.00', 'E');

TRUNCATE TABLE `comanda_detallepreticket`;
INSERT INTO `comanda_detallepreticket` (`id`, `cantidad`, `precioXunidad`, `platos_id`, `bebidas_id`, `menuD_id`, `menuE_id`, `detalleComanda_id`, `descuento`) VALUES
(1, '2', '95.00', 18, NULL, NULL, NULL, 1, NULL),
(2, '2', '85.00', 19, NULL, NULL, NULL, 2, NULL),
(3, '1', '285.00', NULL, NULL, NULL, 1, 5, '0'),
(4, '1', '150.00', NULL, NULL, 3, NULL, 6, '0'),
(5, '1', '25.00', NULL, 12, NULL, NULL, 7, NULL),
(6, '1', '35.00', NULL, 14, NULL, NULL, 8, NULL),
(7, '1', '75.00', 41, NULL, NULL, NULL, 9, NULL),
(8, '2', '150.00', 42, NULL, NULL, NULL, 10, NULL);

TRUNCATE TABLE `comanda_factura`;
INSERT INTO `comanda_factura` (`id`, `fecha`, `hora`, `tipo`, `total_factura`, `comanda_id`, `preticket_id`, `pago_id`) VALUES
(1, '2013-12-03', '17:54:26', 'C', '360.00', NULL, 1, 1),
(2, '2013-12-03', '05:55:55', 'C', '284.40', 2, NULL, 2),
(3, '2013-12-09', '10:26:33', 'C', '495.00', NULL, 2, 3),
(4, '2013-12-17', '09:12:58', 'C', '375.00', NULL, 3, 4),
(5, '2013-12-26', '06:38:18', 'C', '202.00', 10, NULL, 5);

TRUNCATE TABLE `comanda_factura_detalle`;
INSERT INTO `comanda_factura_detalle` (`id`, `factura_id`, `detallefactura_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 2, 4),
(5, 3, 5),
(6, 3, 6),
(7, 3, 7),
(8, 3, 8),
(9, 4, 9),
(10, 4, 10),
(11, 5, 11),
(12, 5, 12),
(13, 5, 13),
(14, 5, 14),
(15, 5, 15),
(16, 5, 16),
(17, 5, 17),
(18, 5, 18);

TRUNCATE TABLE `comanda_pago`;
INSERT INTO `comanda_pago` (`id`, `fecha`, `hora`, `total`, `detalles_id`) VALUES
(1, '2013-12-03', '17:54:36', '360.00', NULL),
(2, '2013-12-03', '05:56:50', '284.40', NULL),
(3, '2013-12-09', '10:26:44', '495.00', NULL),
(4, '2013-12-17', '09:13:04', '375.00', NULL),
(5, '2013-12-26', '06:53:17', '202.00', NULL);

TRUNCATE TABLE `comanda_preticket`;
INSERT INTO `comanda_preticket` (`id`, `fecha`, `hora`, `total_preticket`, `comanda_id`, `factura_id`) VALUES
(1, '2013-12-03', '17:54:03', '360.00', 1, 1),
(2, '2013-12-09', '10:26:18', '495.00', 5, 3),
(3, '2013-12-17', '09:12:53', '375.00', 9, 4);

TRUNCATE TABLE `comanda_preticket_detalles`;
INSERT INTO `comanda_preticket_detalles` (`id`, `preticket_id`, `detallepreticket_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 2, 4),
(5, 2, 5),
(6, 2, 6),
(7, 3, 7),
(8, 3, 8);

TRUNCATE TABLE `django_admin_log`;
INSERT INTO `django_admin_log` (`id`, `action_time`, `user_id`, `content_type_id`, `object_id`, `object_repr`, `action_flag`, `change_message`) VALUES
(1, '2013-12-02 18:37:34', 1, 3, '3', 'andres', 3, ''),
(2, '2013-12-02 18:37:34', 1, 3, '2', 'Gaston', 3, ''),
(3, '2013-12-02 18:38:15', 1, 3, '4', 'andres', 1, ''),
(4, '2013-12-02 18:38:37', 1, 3, '5', 'walter', 1, ''),
(5, '2013-12-02 18:38:59', 1, 3, '6', 'ivana', 1, ''),
(6, '2013-12-02 18:39:58', 1, 3, '6', 'ivana', 2, 'Modifica password, first_name, last_name, email y user_permissions.'),
(7, '2013-12-02 18:40:52', 1, 3, '5', 'walter', 2, 'Modifica password, first_name, last_name, email y user_permissions.'),
(8, '2013-12-02 18:42:13', 1, 3, '4', 'andres', 2, 'Modifica password, first_name, last_name, email y user_permissions.');

TRUNCATE TABLE `django_content_type`;
INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'content type', 'contenttypes', 'contenttype'),
(5, 'session', 'sessions', 'session'),
(6, 'site', 'sites', 'site'),
(7, 'log entry', 'admin', 'logentry'),
(8, 'permisos vistas', 'Administrador', 'permisosvistas'),
(9, 'plato', 'producto', 'plato'),
(10, 'bebida', 'producto', 'bebida'),
(11, 'del dia', 'producto', 'deldia'),
(12, 'ejecutivo', 'producto', 'ejecutivo'),
(13, 'seccion carta', 'altacarta', 'seccioncarta'),
(14, 'carta', 'altacarta', 'carta'),
(15, 'sector', 'altamesa', 'sector'),
(16, 'mesa', 'altamesa', 'mesa'),
(17, 'personal', 'Mozo', 'personal'),
(18, 'detalle comanda', 'comanda', 'detallecomanda'),
(19, 'comanda', 'comanda', 'comanda'),
(20, 'detalle preticket', 'comanda', 'detallepreticket'),
(21, 'preticket', 'comanda', 'preticket'),
(22, 'detalle pago', 'comanda', 'detallepago'),
(23, 'pago', 'comanda', 'pago'),
(24, 'detalle factura', 'comanda', 'detallefactura'),
(25, 'factura', 'comanda', 'factura');

TRUNCATE TABLE `django_session`;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1063h2hjhq0lxxttd3g0puwyz6unflpi', 'NWQyMTk3YWQyMzU1MWNiOGFkMDg4YTJmMTdkMTgwNzg2NmQ0NWEyMTqAAn1xAS4=', '2013-12-31 16:19:46'),
('gq7tdt131g24p6hawqso750a27kf2nx5', 'OGJkYmI0MWFhNTdkZWUyZmM4MGI5MDAxZWZiOTU5Y2I1MzYyODY2NTqAAn1xAShVFWxpc3RhUHJvZHVjdG9zTWVudURpYV1VG2xpc3RhUHJvZHVjdG9zTWVudUVqZWN1dGl2b11xAihYAgAAADUxcQNYAQAAADJYAQAAADNlVRJfYXV0aF91c2VyX2JhY2tlbmRVKWRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kVQ1fYXV0aF91c2VyX2lkigEBdS4=', '2014-01-09 09:44:11'),
('js0i5b25pvgx1qu6z3oe7bcj9r6roxaq', 'NmU1NjU3ZWY2MmU1ODY3MTgzMTRkMTkzODQzNjExZWMwZTBjYmVjYjqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==', '2014-01-13 13:33:18'),
('tg4oqh59v1sfcdewt9xsz0aq1ks9dnna', 'NmU1NjU3ZWY2MmU1ODY3MTgzMTRkMTkzODQzNjExZWMwZTBjYmVjYjqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==', '2014-01-09 09:32:20');

TRUNCATE TABLE `django_site`;
INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

TRUNCATE TABLE `mozo_personal`;
TRUNCATE TABLE `producto_bebida`;
INSERT INTO `producto_bebida` (`id`, `nombre`, `precio`, `stock`, `activo`, `seccion_id`, `marca`, `enPromocion`, `descuento`) VALUES
(1, 'Coca-cola', '10.00', '42', 1, 6, 'Coca-cola', 1, '10'),
(2, 'Fanta', '12.00', '45', 1, 6, 'Coca-cola', 0, '0'),
(3, 'Artesanal', '72.00', '7', 1, 5, 'Artesanal', 1, '10'),
(4, 'jugo de naranja', '25.00', '13', 1, 7, 'Pindapoi', 0, NULL),
(5, 'Agua gasificada', '13.00', '20', 1, 7, 'Villa del Sur', 0, NULL),
(6, 'Agua sin Gasificar', '13.00', '55', 1, 7, 'Villa del Sur', 0, NULL),
(7, 'Agua Saborizada', '15.00', '50', 1, 7, 'H2O', 0, NULL),
(8, 'Jugo Exprimido', '25.00', '49', 1, 7, 'Boru', 0, NULL),
(9, 'Quilmes Cristal', '40.00', '150', 1, 5, 'Quilmes', 1, '10'),
(10, 'Draig', '45.00', '148', 1, 5, 'Draig', 0, NULL),
(11, 'Warsteiner', '45.00', '50', 1, 5, 'Warsteiner', 0, NULL),
(12, 'Budweiser', '25.00', '46', 1, 4, 'Budweiser', 0, NULL),
(13, 'Imperial', '35.00', '50', 1, 4, 'Imperial', 0, NULL),
(14, 'Quilmes Stout', '35.00', '49', 1, 4, 'Quilmes Stout', 0, NULL),
(15, 'Heineken', '45.00', '49', 1, 4, 'Heineken', 0, NULL),
(16, 'Stella Artois', '50.00', '50', 1, 4, 'Stella Artois', 0, NULL),
(17, 'Corona', '45.00', '49', 1, 4, 'Corona', 0, NULL),
(18, 'Negra Modelo', '40.00', '20', 1, 4, 'Negra Modelo', 0, NULL),
(19, 'Guinnes', '25.00', '20', 1, 4, 'Guinnes', 0, NULL),
(20, 'Antares', '50.00', '45', 1, 4, 'Antares', 0, NULL),
(21, 'Trumpeter', '120.00', '10', 1, 3, 'Trumpeter', 0, NULL),
(22, 'Finca la Linda', '110.00', '10', 1, 3, 'Finca la Linda', 0, NULL),
(23, 'Navarro Correa', '100.00', '15', 1, 3, 'Navarro Correa', 0, NULL),
(24, 'San Felipe Roble', '85.00', '25', 1, 3, 'San Felipe Roble', 0, NULL),
(25, 'Latitud 33', '75.00', '35', 1, 11, 'Latitud 33', 0, NULL),
(26, 'Don Valentin Lacrado', '70.00', '40', 1, 11, 'Don Valentin Lacrado', 0, NULL),
(27, 'Benjamin Nieto', '55.00', '50', 1, 11, 'Benjamin Nieto', 0, NULL),
(28, 'Alamos', '110.00', '25', 1, 11, 'Alamos', 1, '10'),
(29, 'Etchart Cafayate', '50.00', '45', 1, 11, 'Etchart Cfayate', 0, NULL),
(30, 'Sprite', '15.00', '99', 1, 6, 'Coca-cola', 0, NULL),
(31, 'Paso de los Toros', '13.00', '38', 1, 6, 'Coca-cola', 0, NULL),
(32, 'Fernet con Coca', '60.00', '60', 1, 17, 'Branca', 0, NULL),
(33, 'Daiquiri', '55.00', '20', 1, 17, 'Varios', 0, NULL),
(34, 'Margarita', '50.00', '15', 1, 17, 'Varios', 0, NULL),
(35, 'Pinia Colada', '40.00', '20', 1, 17, 'Varios', 0, NULL),
(36, 'Mojito', '45.00', '15', 1, 17, 'Varios', 0, NULL),
(37, 'Tequila', '50.00', '20', 1, 17, 'Varios', 0, NULL),
(38, 'Cuba Libre', '58.00', '15', 1, 17, 'Varios', 0, NULL),
(39, 'New Age', '70.00', '50', 1, 17, 'New Age', 0, NULL),
(40, 'Frizze', '90.00', '60', 1, 17, 'Frizze', 0, NULL),
(41, 'Vodka', '80.00', '50', 1, 17, 'Absolute', 0, NULL),
(42, 'Whiskey', '90.00', '50', 1, 17, 'Caballo Blanco', 0, NULL);

TRUNCATE TABLE `producto_deldia`;
INSERT INTO `producto_deldia` (`id`, `nombre`, `precio`, `stock`, `activo`, `seccion_id`, `descripcion`, `fecha_Inicio`) VALUES
(1, 'Menu Manianero', '100.00', '9', 1, 8, 'Un menu que te da la energia necesaria para empezar el dia.', '2013-12-04'),
(2, 'Variadito Crepuscular', '315.00', '10', 1, 8, 'Variado de pizzas, picadas y menues bien argentos.', '2013-12-02'),
(3, 'pizza libre', '150.00', '49', 1, 8, '', '2013-12-03');

TRUNCATE TABLE `producto_deldia_platos`;
INSERT INTO `producto_deldia_platos` (`id`, `deldia_id`, `plato_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(5, 2, 4),
(4, 2, 40),
(6, 2, 41),
(7, 3, 1),
(8, 3, 35);

TRUNCATE TABLE `producto_ejecutivo`;
INSERT INTO `producto_ejecutivo` (`id`, `nombre`, `precio`, `stock`, `activo`, `seccion_id`, `descripcion`, `fecha_Inicio`, `fecha_fin`) VALUES
(1, 'Mariscos de Alto Vuelo', '285.00', '4', 1, 9, 'Un rejunte de mariscos, rabas y otras finas hierbas.', '2013-12-02', '2013-12-31');

TRUNCATE TABLE `producto_ejecutivo_platos`;
INSERT INTO `producto_ejecutivo_platos` (`id`, `ejecutivo_id`, `plato_id`) VALUES
(1, 1, 7),
(2, 1, 8),
(3, 1, 14);

TRUNCATE TABLE `producto_plato`;
INSERT INTO `producto_plato` (`id`, `nombre`, `precio`, `stock`, `activo`, `seccion_id`, `descripcion`, `enPromocion`, `descuento`) VALUES
(1, 'Fugazetta', '65.00', '16', 1, 2, 'Tomate, mozarella, cebolla', 0, NULL),
(2, 'Napolitana al Verdeo', '75.00', '10', 1, 2, 'Tomate, jamon, mozarella, verdeo, oregano.', 1, '10'),
(3, 'Mozzarella', '55.00', '22', 1, 2, 'Mozzarella, jamon y salsa.', 0, NULL),
(4, 'Boru Fiambres', '110.00', '25', 1, 1, 'Salamin, queso, jamon, aceitunas....', 0, NULL),
(5, 'Boru Hot', '160.00', '12', 1, 1, 'Milanesas, pollo, mini muzza...', 0, NULL),
(6, 'Antipasto', '45.00', '10', 1, 1, 'Picles, pepinillos, salame de milan...', 0, NULL),
(7, 'Mariscos', '190.00', '17', 1, 13, 'Vieras, bastones de pescado, escabeche de pesacado...', 0, NULL),
(8, 'Rabas', '60.00', '13', 1, 13, 'Rabas Fritas', 0, NULL),
(9, 'Langostino', '60.00', '20', 1, 13, 'Langostino a la romana.', 0, NULL),
(10, 'Ensalada Sencilla', '20.00', '15', 1, 10, 'Solo dos ingredientes', 0, NULL),
(11, 'Ensalada Mixta', '25.00', '20', 1, 10, 'Solo tres ingredientes', 0, NULL),
(12, 'Ensalada de Rucula', '35.00', '20', 1, 10, 'Rucula, ajo, parmesano.', 0, NULL),
(13, 'Ensalada Waldorf', '45.00', '25', 1, 10, 'Manzana verde, nuece, apio, crema.', 0, NULL),
(14, 'Ensalada Completa', '50.00', '20', 1, 10, 'Tomate, lechuga, cebolla, zanahoria, huevos, jamon, queso y palmitos.', 0, NULL),
(15, 'Ensalada Cesar', '55.00', '15', 1, 10, 'Lechga, pollo, huevo, parmesano, anchoas.', 0, NULL),
(16, 'Ensalada Boru', '65.00', '20', 1, 10, 'Tomate, mix de verdes, crocante de pollo y queso en hebras.', 0, NULL),
(17, 'Wok de Mar', '75.00', '13', 1, 10, 'Mix de verdes, queso en hebras, salteado de mar, ajo y perejil.', 0, NULL),
(18, 'Lomo Boru', '95.00', '13', 1, 12, 'Lomo en reduccion de cerveza negra, hongos de pino, panceta acompaniada de papas rusticas.', 0, NULL),
(19, 'Roll de Pollo', '85.00', '15', 1, 12, 'Pollo relleno de jamon, queso y final hiervas.', 0, NULL),
(20, 'Pesca del Dia', '80.00', '20', 1, 16, 'Pesaca del dia mechada con panceta ahumada.', 0, NULL),
(21, 'Lomo en Croute', '90.00', '15', 1, 16, 'Ternera con crocante de hierbas.', 0, NULL),
(22, 'Dijon', '85.00', '25', 1, 16, 'Carne de cerdo con salsa de mostaza de dijon.', 0, NULL),
(23, 'Tempura de Pollo', '80.00', '15', 1, 16, 'Pollo morinado enn tempura de cerveza.', 0, NULL),
(24, 'Brochettas', '85.00', '20', 1, 16, 'Brochettas de lomo y papas torneadas envueltas en panceta ahumada.', 0, NULL),
(25, 'Sorrentino Mediterraneo', '75.00', '23', 1, 16, 'Sorrentino de jamon y queson con salsa mediterranea.', 0, NULL),
(26, 'Sorrentino Parmesano', '70.00', '15', 1, 16, 'Sorrentino de calabaza y queso parmesano.', 0, NULL),
(27, 'Especial de Nioquis Rellenos', '65.00', '20', 1, 16, 'Nioquis de papa y queso, con salsa de verdeo.', 0, NULL),
(28, 'Especial Huevo Duro', '80.00', '12', 1, 2, 'Tomate, jamon, mozzarella, huevos duros.', 0, NULL),
(29, 'Especial Provolone', '85.00', '14', 1, 2, 'Tomate, jamon, mozzarella, provolone y morrones.', 0, NULL),
(30, 'Nortenia', '84.00', '12', 1, 2, 'Tomate, jamon, mozzarella, panceta, verdeo y choclo.', 0, NULL),
(31, 'Agridulce', '70.00', '5', 1, 2, 'Tomate, jamon, mozzarella, anana, cereza y caramelo.\r\n', 0, NULL),
(32, 'Marina', '92.00', '10', 1, 2, 'Tomate, jamon, mozzarella, salteado de mar.', 0, NULL),
(33, 'Capresse', '80.00', '7', 1, 2, 'Tomate, jamon, mozzarella, albhaca y aceitunas negras.', 0, NULL),
(34, 'Palmito', '82.00', '10', 1, 2, 'Tomate, jamon, mozzarella, palmitos.', 0, NULL),
(35, 'Boru', '85.00', '15', 1, 2, 'Tomate, jamon, mozzarella, cebolla, salchichas, huevo revueto.', 0, NULL),
(36, 'Ruca', '92.00', '10', 1, 2, 'Tomate, jamon, mozzarella, rucula y queso parmesano.', 0, NULL),
(37, 'Roquefort', '75.00', '15', 1, 2, 'Tomate, jamon, mozzarella, queso roquefort.', 0, NULL),
(38, 'Espaniola', '72.00', '10', 1, 2, 'Tomate, jamon, mozzarella, chorizo colorado.', 0, NULL),
(39, 'Cuatro Quesos', '85.00', '12', 1, 2, 'Tomate, jamon, mozzarella, cuatro quesos.', 0, NULL),
(40, 'Panamericana', '95.00', '10', 1, 2, 'Tomate, jamon, mozzarella, panceta y huevos fritos.', 0, NULL),
(41, 'Costeleta Argenta', '75.00', '9', 1, 15, 'Costeleta de ternera, con pure o papas fritas.', 0, NULL),
(42, 'Milanesa Super Boru', '150.00', '7', 1, 15, 'Milanesa de ternera, muzarella, morron, huevo frito, panceta y pure de papas o papas fritas.', 0, NULL),
(43, 'Milanesa Super Napolitana', '140.00', '3', 1, 15, 'Milanesa de ternera, muzarella, oregano y pure de papas o papas fritas.', 0, NULL),
(44, 'Milanesa Super Suiza', '140.00', '2', 1, 15, 'Milanesa de ternera, muzarella, salsa blanca y pure de papas o papas fritas.', 0, NULL),
(45, 'Lomito Boru', '75.00', '10', 1, 15, 'Lomito de ternera, jamon, queso, tomate, lechuga, huevo, panceta, cebolla y papas fritas..', 0, NULL),
(46, 'Copa Roja', '60.00', '15', 1, 14, 'Helado americano con frutos rojos..', 0, NULL),
(47, 'Banana Split', '60.00', '20', 1, 14, 'Banana, 5 bochas de helado y crema chantilly.', 0, NULL),
(48, 'Don Pedro', '45.00', '15', 1, 14, 'Dulce de leche, nueces, americana, crema chantilly y whiskey.', 0, NULL),
(49, 'Tibio de Peras y Manzanas', '40.00', '12', 1, 14, 'Cubos de manzana y peras, salteados en manteca y anis.', 0, NULL),
(50, 'Crepes de Manzana', '35.00', '20', 1, 14, 'Panqueque de manzana, caramelo, azucar y ron.', 0, NULL),
(51, 'Flan', '30.00', '30', 1, 14, 'Con dulce de leche o crema.', 0, NULL);
SET FOREIGN_KEY_CHECKS=1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
