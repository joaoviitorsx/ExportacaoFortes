# 🚀 Exportacao Fortes

Sistema desktop para conversão de arquivos SPED Fiscal (EFD ICMS/IPI) para o formato **Fortes Fiscal (.fs)**, facilitando a importação de notas fiscais e movimentações tributárias.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-GUI-purple.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração](#-configuração)
- [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🎯 Sobre o Projeto

O **ExportacaoFortes** é uma solução desenvolvida para automatizar a conversão de dados fiscais do formato SPED (Sistema Público de Escrituração Digital) para o formato proprietário do sistema **Fortes Fiscal**.

### Problema Resolvido

Empresas que utilizam o Fortes Fiscal precisam importar manualmente dados de notas fiscais e movimentações tributárias. Este sistema automatiza esse processo através de:

1. **Leitura de arquivos SPED** (formato .txt)
2. **Validação e processamento** dos registros fiscais
3. **Transformação ETL** dos dados
4. **Geração do arquivo .fs** compatível com Fortes Fiscal

---

## ✨ Funcionalidades

### 📥 Importação de Dados

- ✅ Leitura de arquivos SPED Fiscal (registros 0000, 0150, 0200, C100, C170, C190)
- ✅ Validação de CNPJs via integração com API externa
- ✅ Detecção automática de codificação de arquivo (UTF-8, ISO-8859-1, etc.)
- ✅ Processamento em lote de múltiplos arquivos

### 🔄 Processamento

- ✅ Pipeline ETL (Extract, Transform, Load) robusto
- ✅ Validação de integridade dos dados fiscais
- ✅ Cálculo automático de alíquotas e tributação
- ✅ Soft delete para auditoria de dados
- ✅ Cache inteligente para otimização de performance

### 📤 Exportação

- ✅ Geração de arquivos .fs (Fortes Fiscal)
- ✅ Registros suportados: CAB, PAR, PRO, UND, NFM, PNM, INM, SNM
- ✅ Formatação automática conforme especificação Fortes
- ✅ Tratamento de substituição tributária (ST)
- ✅ Cálculo de rateio de frete, seguro e outras despesas

### 🎨 Interface Gráfica

- ✅ Interface moderna construída com Flet
- ✅ Upload de arquivos drag-and-drop
- ✅ Barra de progresso em tempo real
- ✅ Notificações visuais de status
- ✅ Cadastro e gerenciamento de empresas

---

## 🛠️ Tecnologias Utilizadas

### Backend

| Tecnologia | Descrição |
|------------|-----------|
| **Python 3.9+** | Linguagem principal |
| **SQLAlchemy** | ORM para banco de dados |
| **PyMySQL** | Driver MySQL |
| **Pandas** | Manipulação de dados |
| **python-dotenv** | Gerenciamento de variáveis de ambiente |

### Frontend

| Tecnologia | Descrição |
|------------|-----------|
| **Flet** | Framework GUI multiplataforma |
| **Asyncio** | Processamento assíncrono |

### Banco de Dados

| Banco | Uso |
|-------|-----|
| **MySQL** | Armazenamento principal (ExportacaoFortes) |
| **MySQL** | Integração com Apurador ICMS |

### Build & Deploy

| Ferramenta | Descrição |
|------------|-----------|
| **PyInstaller** | Criação de executável standalone |

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura **MVC (Model-View-Controller)** com separação clara de responsabilidades:

```
ExportacaoFortes/
├── back/                    # Backend (Business Logic)
│   └── src/
│       ├── config/          # Configurações de BD
│       ├── controllers/     # Controladores
│       ├── models/          # Modelos ORM
│       ├── repositories/    # Camada de dados
│       ├── services/        # Lógica de negócio
│       └── utils/           # Utilitários
│
└── front/                   # Frontend (GUI)
    └── src/
        ├── components/      # Componentes reutilizáveis
        ├── routes/          # Rotas da aplicação
        ├── views/           # Telas da aplicação
        └── utils/           # Utilitários frontend
```

### Padrões Utilizados

- **Repository Pattern**: Abstração da camada de dados
- **Service Layer**: Lógica de negócio isolada
- **ETL Pipeline**: Processamento estruturado de dados
- **Builder Pattern**: Construção de registros .fs

---

## 📦 Pré-requisitos

- **Python 3.9+**
- **MySQL 5.7+** ou **MariaDB 10.3+**
- **Git** (para clonar o repositório)
- **pip** (gerenciador de pacotes Python)

---

### Fluxo de uso

1. **Cadastrar Empresa**: Acesse a tela de cadastro e adicione os dados da empresa
2. **Selecionar Empresa**: Escolha a empresa na lista
3. **Upload do SPED**: Arraste ou selecione o arquivo SPED (.txt)
4. **Processar**: Clique em "Processar Arquivo"
5. **Aguardar**: Acompanhe o progresso na barra de status
6. **Download**: Baixe o arquivo .fs gerado

### Registros SPED Suportados

| Registro | Descrição |
|----------|-----------|
| **0000** | Abertura do Arquivo Digital e Identificação da Entidade |
| **0150** | Cadastro de Participantes |
| **0200** | Cadastro de Itens (Produtos e Serviços) |
| **C100** | Documento - Nota Fiscal (código 01), Nota Fiscal Avulsa (código 1B), Nota Fiscal de Produtor (código 04) e NF-e (código 55) |
| **C170** | Itens do Documento (Código 01, 1B, 04 e 55) |
| **C190** | Registro Analítico do Documento (Código 01, 1B, 04 e 55) |

### Registros Fortes Gerados

| Registro | Descrição |
|----------|-----------|
| **CAB** | Cabeçalho do arquivo |
| **PAR** | Participantes (Fornecedores) |
| **PRO** | Produtos |
| **UND** | Unidades de Medida |
| **NFM** | Notas Fiscais (Cabeçalho) |
| **PNM** | Produtos da Nota Fiscal |
| **INM** | Totalizadores por CFOP |
| **SNM** | Sumarização por Alíquota |

---

## 📁 Estrutura do Projeto

```
ExportacaoFortes/
│
├── app.py                          # Entry point da aplicação
├── requirements.txt                # Dependências Python
├── fortes.spec                     # Configuração PyInstaller
├── .env                            # Variáveis de ambiente (não versionado)
├── exportacaofortes-bd.sql         # Script de criação do BD
│
├── back/                           # Backend
│   └── src/
│       ├── config/db/              # Configurações de banco de dados
│       │   ├── base.py
│       │   ├── conexaoFS.py
│       │   └── conexaoICMS.py
│       │
│       ├── controllers/            # Controladores
│       │   ├── empresaController.py
│       │   └── fsController.py
│       │
│       ├── models/                 # Models ORM
│       │   ├── fs/                 # Models do banco FS
│       │   └── icms/               # Models do banco ICMS
│       │
│       ├── repositories/           # Camada de acesso a dados
│       │   ├── camposRepo/         # Repositórios de campos FS
│       │   ├── empresaRepo/
│       │   ├── fornecedoresRepo/
│       │   ├── registrosRepo/      # Repositórios SPED
│       │   └── transferRepo/
│       │
│       ├── services/               # Lógica de negócio
│       │   ├── cnpjRegister/       # Validação de CNPJ
│       │   ├── etl/                # Pipeline ETL
│       │   ├── exportar/           # Geração de arquivo .fs
│       │   ├── fornecedor/
│       │   ├── fs/                 # Serviços de exportação FS
│       │   │   ├── CAB/
│       │   │   ├── PAR/
│       │   │   ├── PRO/
│       │   │   ├── UND/
│       │   │   ├── NFM/
│       │   │   ├── PNM/
│       │   │   ├── INM/
│       │   │   └── SNM/
│       │   └── sync/
│       │
│       └── utils/                  # Utilitários
│           ├── aliquota.py
│           ├── cache.py
│           ├── cnpj.py
│           ├── fsFormat.py
│           ├── sanitizacao.py
│           └── validadores.py
│
└── front/                          # Frontend
    └── src/
        ├── assets/                 # Recursos (ícones, imagens)
        │   └── icone.ico
        │
        ├── components/             # Componentes reutilizáveis
        │   ├── actionButton.py
        │   ├── card.py
        │   ├── fileUpload.py
        │   ├── header.py
        │   ├── notificacao.py
        │   └── progressBar.py
        │
        ├── routes/                 # Rotas da aplicação
        │   ├── empresaRoute.py
        │   └── fsRoute.py
        │
        ├── utils/                  # Utilitários frontend
        │   ├── cnpjFormatador.py
        │   └── path.py
        │
        └── views/                  # Telas da aplicação
            ├── cadastroView.py
            ├── empresaView.py
            └── mainView.py
```


