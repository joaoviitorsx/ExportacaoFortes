CREATE DATABASE IF NOT EXISTS exportacaofortes;
USE exportacaofortes;

-- Tabela de empresas
CREATE TABLE IF NOT EXISTS empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cnpj CHAR(14) NOT NULL,
    razao_social VARCHAR(100) NOT NULL,
	uf varchar(2) not null,
    simples boolean,
    aliq_espec boolean default false,
    UNIQUE KEY unq_cnpj (cnpj)
);

alter table empresas add column aliq_espec boolean default false;
select * from empresas;

-- Registro 0000
CREATE TABLE IF NOT EXISTS registro_0000 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    reg VARCHAR(10),
    cod_ver VARCHAR(10),
    cod_fin VARCHAR(10),
    dt_ini DATE,
    dt_fin DATE,
    nome VARCHAR(100),
    cnpj CHAR(14),
    cpf CHAR(11),
    uf CHAR(2),
    ie VARCHAR(20),
    cod_num VARCHAR(20),
    im VARCHAR(20),
    suframa VARCHAR(20),
    ind_perfil VARCHAR(10),
    ind_ativ VARCHAR(10),
    filial VARCHAR(10),
    periodo VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_empresa (empresa_id)
);

-- Registro 0150
CREATE TABLE IF NOT EXISTS registro_0150 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    reg VARCHAR(10),
    cod_part VARCHAR(60),
    nome VARCHAR(100),
    cod_pais VARCHAR(10),
    cnpj CHAR(14),
    cpf CHAR(11),
    ie VARCHAR(20),
    cod_mun VARCHAR(20),
    suframa VARCHAR(20),
    ende VARCHAR(100),
    num VARCHAR(20),
    compl VARCHAR(20),
    bairro VARCHAR(50),
    uf CHAR(2),
    tipo_pessoa CHAR(1),
    periodo VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_empresa (empresa_id)
);

-- Registro 0200
CREATE TABLE IF NOT EXISTS registro_0200 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    reg VARCHAR(10),
    cod_item VARCHAR(60),
    descr_item VARCHAR(255),
    cod_barra VARCHAR(60),
    cod_ant_item VARCHAR(60),
    unid_inv VARCHAR(10),
    tipo_item VARCHAR(10),
    cod_ncm VARCHAR(20),
    ex_ipi VARCHAR(10),
    cod_gen VARCHAR(10),
    cod_list VARCHAR(10),
    aliq_icms DECIMAL(5,2),
    cest CHAR(7),
    periodo VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_empresa (empresa_id)
);

-- Registro C100
CREATE TABLE IF NOT EXISTS registro_c100 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    periodo VARCHAR(10),
    reg VARCHAR(10),
    ind_oper CHAR(1),
    ind_emit CHAR(1),
    cod_part VARCHAR(60),
    cod_mod VARCHAR(10),
    cod_sit VARCHAR(10),
    ser VARCHAR(10),
    num_doc VARCHAR(20),
    chv_nfe VARCHAR(60),
    dt_doc DATE,
    dt_e_s DATE,
    vl_doc DECIMAL(15,2),
    ind_pgto VARCHAR(5),
    vl_desc DECIMAL(15,2),
    vl_abat_nt DECIMAL(15,2),
    vl_merc DECIMAL(15,2),
    ind_frt VARCHAR(5),
    vl_frt DECIMAL(15,2),
    vl_seg DECIMAL(15,2),
    vl_out_da DECIMAL(15,2),
    vl_bc_icms DECIMAL(15,2),
    vl_icms DECIMAL(15,2),
    vl_bc_icms_st DECIMAL(15,2),
    vl_icms_st DECIMAL(15,2),
    vl_ipi DECIMAL(15,2),
    vl_pis DECIMAL(15,2),
    vl_cofins DECIMAL(15,2),
    vl_pis_st DECIMAL(15,2),
    vl_cofins_st DECIMAL(15,2),
    filial VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_empresa (empresa_id)
);

-- Registro C170
CREATE TABLE IF NOT EXISTS registro_c170 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    periodo VARCHAR(10),
    reg VARCHAR(10),
    num_item VARCHAR(10),
    cod_item VARCHAR(60),
    descr_compl VARCHAR(255),
    qtd DECIMAL(15,4),
    unid VARCHAR(10),
    vl_item DECIMAL(15,2),
    vl_desc DECIMAL(15,2),
    ind_mov VARCHAR(5),
    cst_icms VARCHAR(10),
    cfop VARCHAR(10),
    cod_nat VARCHAR(11),
    vl_bc_icms DECIMAL(15,2),
    aliq_icms DECIMAL(5,2),
    vl_icms DECIMAL(15,2),
    vl_bc_icms_st DECIMAL(15,2),
    aliq_st DECIMAL(5,2),
    vl_icms_st DECIMAL(15,2),
    ind_apur VARCHAR(5),
    cst_ipi VARCHAR(10),
    cod_enq VARCHAR(10),
    vl_bc_ipi DECIMAL(15,2),
    aliq_ipi DECIMAL(5,2),
    vl_ipi DECIMAL(15,2),
    cst_pis VARCHAR(10),
    vl_bc_pis DECIMAL(15,2),
    aliq_pis DECIMAL(5,2),
    quant_bc_pis DECIMAL(15,4),
    aliq_pis_reais DECIMAL(15,4),
    vl_pis DECIMAL(15,2),
    cst_cofins VARCHAR(10),
    vl_bc_cofins DECIMAL(15,2),
    aliq_cofins DECIMAL(5,2),
    quant_bc_cofins DECIMAL(15,4),
    aliq_cofins_reais DECIMAL(15,4),
    vl_cofins DECIMAL(15,2),
    cod_cta VARCHAR(255),
    vl_abat_nt DECIMAL(15,2),
    c100_id INT,
    filial VARCHAR(10),
    ind_oper VARCHAR(5),
    cod_part VARCHAR(60),
    num_doc VARCHAR(20),
    chv_nfe VARCHAR(60),
    ncm VARCHAR(44) DEFAULT '',
    mercado VARCHAR(15) DEFAULT '',
    aliquota VARCHAR(10) DEFAULT '',
    resultado VARCHAR(20),
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_empresa (empresa_id)
);

-- Registro C190
CREATE TABLE IF NOT EXISTS registro_c190 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    periodo VARCHAR(10) NOT NULL,
    c100_id INT,
    reg VARCHAR(10) DEFAULT 'C190',
    cst_icms VARCHAR(3),
    cfop VARCHAR(10),
    aliq_icms DECIMAL(7,2),
    vl_opr DECIMAL(15,2),
    vl_bc_icms DECIMAL(15,2),
    vl_icms DECIMAL(15,2),
    vl_bc_icms_st DECIMAL(15,2),
    vl_icms_st DECIMAL(15,2),
    vl_red_bc DECIMAL(15,2),
    vl_ipi DECIMAL(15,2),
    cod_obs VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    INDEX idx_empresa (empresa_id),
    INDEX idx_c100 (c100_id)
);

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    codigo VARCHAR(60),
    produto VARCHAR(255),
    ncm VARCHAR(20),
    aliquota VARCHAR(10),
    categoriaFiscal VARCHAR(40),
    INDEX idx_empresa (empresa_id)
);

CREATE TABLE IF NOT EXISTS fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    cod_part VARCHAR(60),
    nome VARCHAR(100),
    cnpj VARCHAR(20),
    uf VARCHAR(5),
    cnae VARCHAR(20),
    decreto VARCHAR(10),
    simples VARCHAR(10),
    INDEX idx_empresa (empresa_id)
);

CREATE TABLE log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    empresa_id BIGINT NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    acao VARCHAR(255) NOT NULL,
    status ENUM('OK', 'ERRO', 'PENDENTE') DEFAULT 'OK',
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_empresa FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);


SELECT id, num_doc 
FROM c100
WHERE periodo = 08/2025
AND empresa_id = 1
AND ativo = 1;
              

select * from empresas;
alter table empresas drop column ativo;
select * from empresas;

SET SQL_SAFE_UPDATES = 0;

select * from produtos;


select * from `c100`;
select * from `0200`;

select * from `registro_0000`;
select * from `registro_0150`;
select * from `registro_0200`;
select * from `registro_c100`;
select * from `registro_c170`;
select * from `registro_c190`;
select * from produtos;
select * from fornecedores;

select * from empresas;

select count(*) from produtos;
select * from empresas;

select * from `registro_c100`;
select * from `registro_c190`;
select * from produtos;

SET SQL_SAFE_UPDATES = 0;

delete from `registro_0000`;
delete from `registro_0150`;
delete from `registro_0200`;
delete from `registro_c100`;
delete from `registro_c170`;
delete from `registro_c190`;
delete from produtos;

            
select * from registro_c100 where empresa_id = 1 and dt_doc is null;

SELECT
                c190.c100_id,
                c190.vl_opr,
                c190.vl_bc_icms_st,
                c190.aliq_icms,       
                c190.vl_icms_st       
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100 ON c190.c100_id = c100.id
            WHERE
                c190.empresa_id = 1;
                
                
SELECT
            c190.c100_id,
            c190.vl_opr,
            c190.vl_bc_icms_st,
            COALESCE(p.aliquota, c190.aliq_icms) as aliq_icms,       
            c190.vl_icms_st       
        FROM registro_c190 AS c190
        JOIN registro_c100 AS c100 ON c190.c100_id = c100.id
        LEFT JOIN registro_c170 AS c170 ON c170.c100_id = c100.id
        LEFT JOIN produtos AS p ON p.codigo = c170.cod_item AND p.empresa_id = c170.empresa_id
        WHERE
            c190.empresa_id = 1;
            
SELECT dt_ini, dt_fin, periodo FROM registro_0000 WHERE empresa_id = 1 LIMIT 1

select * from empresas;
insert into empresas(id, cnpj, razao_social, uf) values ("2", "32768826000272", "ATACADO DO VALE COMERCIO DE ALIMENTOS LTDA", "CE");
insert into empresas(id, cnpj, razao_social, uf) values ("1", "00092104000173", "JM SUPERMERCADO COMERCIO DE ALIMENTOS LTDA", "CE");