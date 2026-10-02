-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-10-2026 a las 23:06:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ejercicios_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juego_adivina`
--

CREATE TABLE `juego_adivina` (
  `id` int(11) NOT NULL,
  `numero_secreto` int(11) NOT NULL,
  `intentos_totales` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `juego_adivina`
--

INSERT INTO `juego_adivina` (`id`, `numero_secreto`, `intentos_totales`, `fecha`) VALUES
(1, 5, 5, '2026-10-02 18:39:46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_par_impar`
--

CREATE TABLE `registro_par_impar` (
  `id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `resultado` varchar(10) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_tablas`
--

CREATE TABLE `registro_tablas` (
  `id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_tablas`
--

INSERT INTO `registro_tablas` (`id`, `numero`, `fecha`) VALUES
(1, 8, '2026-10-02 18:37:41');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `juego_adivina`
--
ALTER TABLE `juego_adivina`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `registro_par_impar`
--
ALTER TABLE `registro_par_impar`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `registro_tablas`
--
ALTER TABLE `registro_tablas`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `juego_adivina`
--
ALTER TABLE `juego_adivina`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `registro_par_impar`
--
ALTER TABLE `registro_par_impar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `registro_tablas`
--
ALTER TABLE `registro_tablas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
