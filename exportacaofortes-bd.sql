-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: exportacaofortes
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cnpj` char(14) NOT NULL,
  `razao_social` varchar(100) NOT NULL,
  `uf` varchar(2) NOT NULL,
  `simples` tinyint(1) DEFAULT NULL,
  `aliq_espec` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_cnpj` (`cnpj`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fornecedores`
--

DROP TABLE IF EXISTS `fornecedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornecedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int DEFAULT NULL,
  `cod_part` varchar(60) DEFAULT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `cnpj` varchar(20) DEFAULT NULL,
  `uf` varchar(5) DEFAULT NULL,
  `cnae` varchar(20) DEFAULT NULL,
  `decreto` varchar(10) DEFAULT NULL,
  `simples` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chave_cod_part_empresa` (`empresa_id`,`cod_part`),
  KEY `idx_empresa` (`empresa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38643 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int DEFAULT NULL,
  `codigo` varchar(60) DEFAULT NULL,
  `produto` varchar(255) DEFAULT NULL,
  `ncm` varchar(20) DEFAULT NULL,
  `aliquota` varchar(10) DEFAULT NULL,
  `categoriaFiscal` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chave_codigo_empresa` (`empresa_id`,`codigo`),
  KEY `idx_empresa` (`empresa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=992385 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro_0000`
--

DROP TABLE IF EXISTS `registro_0000`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_0000` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int DEFAULT NULL,
  `reg` varchar(10) DEFAULT NULL,
  `cod_ver` varchar(10) DEFAULT NULL,
  `cod_fin` varchar(10) DEFAULT NULL,
  `dt_ini` date DEFAULT NULL,
  `dt_fin` date DEFAULT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `cnpj` char(14) DEFAULT NULL,
  `cpf` char(11) DEFAULT NULL,
  `uf` char(2) DEFAULT NULL,
  `ie` varchar(20) DEFAULT NULL,
  `cod_num` varchar(20) DEFAULT NULL,
  `im` varchar(20) DEFAULT NULL,
  `suframa` varchar(20) DEFAULT NULL,
  `ind_perfil` varchar(10) DEFAULT NULL,
  `ind_ativ` varchar(10) DEFAULT NULL,
  `filial` varchar(10) DEFAULT NULL,
  `periodo` varchar(10) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=686 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro_0150`
--

DROP TABLE IF EXISTS `registro_0150`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_0150` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int DEFAULT NULL,
  `reg` varchar(10) DEFAULT NULL,
  `cod_part` varchar(60) DEFAULT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `cod_pais` varchar(10) DEFAULT NULL,
  `cnpj` char(14) DEFAULT NULL,
  `cpf` char(11) DEFAULT NULL,
  `ie` varchar(20) DEFAULT NULL,
  `cod_mun` varchar(20) DEFAULT NULL,
  `suframa` varchar(20) DEFAULT NULL,
  `ende` varchar(100) DEFAULT NULL,
  `num` varchar(20) DEFAULT NULL,
  `compl` varchar(60) DEFAULT NULL,
  `bairro` varchar(50) DEFAULT NULL,
  `uf` char(2) DEFAULT NULL,
  `tipo_pessoa` char(1) DEFAULT NULL,
  `periodo` varchar(10) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44585 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro_0200`
--

DROP TABLE IF EXISTS `registro_0200`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_0200` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int DEFAULT NULL,
  `reg` varchar(10) DEFAULT NULL,
  `cod_item` varchar(60) DEFAULT NULL,
  `descr_item` varchar(255) DEFAULT NULL,
  `cod_barra` varchar(60) DEFAULT NULL,
  `cod_ant_item` varchar(60) DEFAULT NULL,
  `unid_inv` varchar(10) DEFAULT NULL,
  `tipo_item` varchar(10) DEFAULT NULL,
  `cod_ncm` varchar(20) DEFAULT NULL,
  `ex_ipi` varchar(10) DEFAULT NULL,
  `cod_gen` varchar(10) DEFAULT NULL,
  `cod_list` varchar(10) DEFAULT NULL,
  `aliq_icms` decimal(5,2) DEFAULT NULL,
  `cest` char(7) DEFAULT NULL,
  `periodo` varchar(10) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=965395 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro_c100`
--

DROP TABLE IF EXISTS `registro_c100`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_c100` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int DEFAULT NULL,
  `periodo` varchar(10) DEFAULT NULL,
  `reg` varchar(10) DEFAULT NULL,
  `ind_oper` char(1) DEFAULT NULL,
  `ind_emit` char(1) DEFAULT NULL,
  `cod_part` varchar(60) DEFAULT NULL,
  `cod_mod` varchar(10) DEFAULT NULL,
  `cod_sit` varchar(10) DEFAULT NULL,
  `ser` varchar(10) DEFAULT NULL,
  `num_doc` varchar(20) DEFAULT NULL,
  `chv_nfe` varchar(60) DEFAULT NULL,
  `doc_key` varchar(120) DEFAULT NULL,
  `dt_doc` date DEFAULT NULL,
  `dt_e_s` date DEFAULT NULL,
  `vl_doc` decimal(15,2) DEFAULT NULL,
  `ind_pgto` varchar(5) DEFAULT NULL,
  `vl_desc` decimal(15,2) DEFAULT NULL,
  `vl_abat_nt` decimal(15,2) DEFAULT NULL,
  `vl_merc` decimal(15,2) DEFAULT NULL,
  `ind_frt` varchar(5) DEFAULT NULL,
  `vl_frt` decimal(15,2) DEFAULT NULL,
  `vl_seg` decimal(15,2) DEFAULT NULL,
  `vl_out_da` decimal(15,2) DEFAULT NULL,
  `vl_bc_icms` decimal(15,2) DEFAULT NULL,
  `vl_icms` decimal(15,2) DEFAULT NULL,
  `vl_bc_icms_st` decimal(15,2) DEFAULT NULL,
  `vl_icms_st` decimal(15,2) DEFAULT NULL,
  `vl_ipi` decimal(15,2) DEFAULT NULL,
  `vl_pis` decimal(15,2) DEFAULT NULL,
  `vl_cofins` decimal(15,2) DEFAULT NULL,
  `vl_pis_st` decimal(15,2) DEFAULT NULL,
  `vl_cofins_st` decimal(15,2) DEFAULT NULL,
  `filial` varchar(10) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3977092 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro_c170`
--

DROP TABLE IF EXISTS `registro_c170`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_c170` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int NOT NULL,
  `periodo` varchar(10) DEFAULT NULL,
  `reg` varchar(10) DEFAULT NULL,
  `num_item` varchar(10) DEFAULT NULL,
  `cod_item` varchar(60) DEFAULT NULL,
  `descr_compl` varchar(255) DEFAULT NULL,
  `qtd` decimal(15,4) DEFAULT NULL,
  `unid` varchar(10) DEFAULT NULL,
  `vl_item` decimal(15,2) DEFAULT NULL,
  `vl_desc` decimal(15,2) DEFAULT NULL,
  `ind_mov` varchar(5) DEFAULT NULL,
  `cst_icms` varchar(10) DEFAULT NULL,
  `cfop` varchar(10) DEFAULT NULL,
  `cod_nat` varchar(11) DEFAULT NULL,
  `vl_bc_icms` decimal(15,2) DEFAULT NULL,
  `aliq_icms` decimal(5,2) DEFAULT NULL,
  `vl_icms` decimal(15,2) DEFAULT NULL,
  `vl_bc_icms_st` decimal(15,2) DEFAULT NULL,
  `aliq_st` decimal(5,2) DEFAULT NULL,
  `vl_icms_st` decimal(15,2) DEFAULT NULL,
  `ind_apur` varchar(5) DEFAULT NULL,
  `cst_ipi` varchar(10) DEFAULT NULL,
  `cod_enq` varchar(10) DEFAULT NULL,
  `vl_bc_ipi` decimal(15,2) DEFAULT NULL,
  `aliq_ipi` decimal(5,2) DEFAULT NULL,
  `vl_ipi` decimal(15,2) DEFAULT NULL,
  `cst_pis` varchar(10) DEFAULT NULL,
  `vl_bc_pis` decimal(15,2) DEFAULT NULL,
  `aliq_pis` decimal(5,2) DEFAULT NULL,
  `quant_bc_pis` decimal(15,4) DEFAULT NULL,
  `aliq_pis_reais` decimal(15,4) DEFAULT NULL,
  `vl_pis` decimal(15,2) DEFAULT NULL,
  `cst_cofins` varchar(10) DEFAULT NULL,
  `vl_bc_cofins` decimal(15,2) DEFAULT NULL,
  `aliq_cofins` decimal(5,2) DEFAULT NULL,
  `quant_bc_cofins` decimal(15,4) DEFAULT NULL,
  `aliq_cofins_reais` decimal(15,4) DEFAULT NULL,
  `vl_cofins` decimal(15,2) DEFAULT NULL,
  `cod_cta` varchar(255) DEFAULT NULL,
  `vl_abat_nt` decimal(15,2) DEFAULT NULL,
  `c100_id` int DEFAULT NULL,
  `filial` varchar(10) DEFAULT NULL,
  `ind_oper` varchar(5) DEFAULT NULL,
  `cod_part` varchar(60) DEFAULT NULL,
  `num_doc` varchar(20) DEFAULT NULL,
  `chv_nfe` varchar(60) DEFAULT NULL,
  `ncm` varchar(44) DEFAULT '',
  `mercado` varchar(15) DEFAULT '',
  `aliquota` varchar(10) DEFAULT '',
  `resultado` varchar(20) DEFAULT NULL,
  `doc_key` varchar(120) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`),
  KEY `idx_doc_key_c170` (`empresa_id`,`doc_key`),
  KEY `fk_c170_c100` (`c100_id`),
  CONSTRAINT `fk_c170_c100` FOREIGN KEY (`c100_id`) REFERENCES `registro_c100` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=945792 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro_c190`
--

DROP TABLE IF EXISTS `registro_c190`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_c190` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int NOT NULL,
  `periodo` varchar(10) NOT NULL,
  `c100_id` int DEFAULT NULL,
  `reg` varchar(10) DEFAULT 'C190',
  `cst_icms` varchar(3) DEFAULT NULL,
  `cfop` varchar(10) DEFAULT NULL,
  `aliq_icms` decimal(7,2) DEFAULT NULL,
  `vl_opr` decimal(15,2) DEFAULT NULL,
  `vl_bc_icms` decimal(15,2) DEFAULT NULL,
  `vl_icms` decimal(15,2) DEFAULT NULL,
  `vl_bc_icms_st` decimal(15,2) DEFAULT NULL,
  `vl_icms_st` decimal(15,2) DEFAULT NULL,
  `vl_red_bc` decimal(15,2) DEFAULT NULL,
  `vl_ipi` decimal(15,2) DEFAULT NULL,
  `cod_obs` varchar(10) DEFAULT NULL,
  `doc_key` varchar(120) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_empresa` (`empresa_id`),
  KEY `idx_c100` (`c100_id`),
  KEY `idx_doc_key_c190` (`empresa_id`,`doc_key`),
  CONSTRAINT `fk_c190_c100` FOREIGN KEY (`c100_id`) REFERENCES `registro_c100` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6513930 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-03 14:02:50
