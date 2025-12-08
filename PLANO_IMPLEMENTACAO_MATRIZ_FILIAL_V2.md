# 🚀 Plano de Implementação: Cadastro Inteligente Matriz/Filial V2

## 📊 Visão Geral

Implementar sistema automático de identificação e cadastro de empresas matriz/filial usando a **raiz do CNPJ** como chave do grupo empresarial, com sincronização inteligente de produtos (INSERT + UPDATE).

---

## 🎯 Objetivos

1. ✅ **Zero configuração manual** - sistema decide 100% automaticamente
2. ✅ **Raiz CNPJ como chave** - primeiros 8 dígitos identificam grupo
3. ✅ **Sincronização completa** - INSERT novos + UPDATE existentes
4. ✅ **Relacionamento direto** - matriz_id (FK) ao invés de cnpj_matriz (string)

---

## 📋 Fase 1: Alteração do Banco de Dados

### 1.1 Nova Estrutura da Tabela `empresas`

```sql
-- Remover coluna antiga (se necessário migrar dados primeiro)
-- ALTER TABLE empresas DROP COLUMN cnpj_matriz;

-- Adicionar novas colunas
ALTER TABLE empresas 
    ADD COLUMN cnpj_raiz CHAR(8) NOT NULL AFTER cnpj,
    ADD COLUMN is_matriz BOOLEAN DEFAULT 0 AFTER simples,
    ADD COLUMN matriz_id INT NULL AFTER is_matriz,
    ADD INDEX idx_cnpj_raiz (cnpj_raiz),
    ADD INDEX idx_matriz_id (matriz_id),
    ADD CONSTRAINT fk_matriz 
        FOREIGN KEY (matriz_id) REFERENCES empresas(id) 
        ON DELETE SET NULL;
```

### 1.2 Script de Migração de Dados Existentes

```sql
-- Calcular cnpj_raiz para registros existentes
UPDATE empresas SET cnpj_raiz = LEFT(cnpj, 8);

-- Identificar matrizes (primeira empresa de cada raiz)
UPDATE empresas e1
SET is_matriz = 1
WHERE id = (
    SELECT MIN(id) 
    FROM (SELECT id, cnpj_raiz FROM empresas) e2 
    WHERE e2.cnpj_raiz = e1.cnpj_raiz
);

-- Atribuir matriz_id para filiais
UPDATE empresas e1
SET matriz_id = (
    SELECT id 
    FROM (SELECT id, cnpj_raiz FROM empresas WHERE is_matriz = 1) e2
    WHERE e2.cnpj_raiz = e1.cnpj_raiz
)
WHERE is_matriz = 0;

-- Para matrizes, matriz_id = próprio id
UPDATE empresas SET matriz_id = id WHERE is_matriz = 1;
```

---

## 📋 Fase 2: Atualização dos Models

### 2.1 Arquivo: `empresaFsModel.py`

```python
from ...config.db.base import Base
from sqlalchemy import Column, Integer, String, CHAR, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class EmpresaFsModel(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(CHAR(14), nullable=False, unique=True, index=True)
    cnpj_raiz = Column(CHAR(8), nullable=False, index=True)
    razao_social = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    simples = Column(Boolean, nullable=True)
    is_matriz = Column(Boolean, default=False)
    matriz_id = Column(Integer, ForeignKey('empresas.id'), nullable=True, index=True)
    aliq_espec = Column(Boolean, default=False)
    
    # Relacionamentos
    matriz = relationship("EmpresaFsModel", remote_side=[id], backref="filiais")
```

---

## 📋 Fase 3: Lógica de Cadastro Automático

### 3.1 Arquivo: `empresaRepository.py`

```python
from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        sql = text("""
            SELECT 
                e.id, 
                e.razao_social, 
                e.cnpj, 
                e.cnpj_raiz,
                e.uf, 
                e.simples, 
                e.aliq_espec,
                e.is_matriz,
                e.matriz_id,
                m.razao_social as matriz_razao_social,
                m.cnpj as matriz_cnpj
            FROM empresas e
            LEFT JOIN empresas m ON e.matriz_id = m.id
        """)
        result = self.session.execute(sql).mappings().all()
        return [dict(row) for row in result]

    def insert(self, razao_social: str, cnpj: str, uf: str, simples: bool, aliq_espec: int = 0):
        # 1. Verificar se CNPJ já existe
        check_sql = text("SELECT id FROM empresas WHERE cnpj = :cnpj")
        exists = self.session.execute(check_sql, {"cnpj": cnpj}).first()

        if exists:
            return {
                "status": "erro", 
                "mensagem": "Empresa já cadastrada."
            }

        # 2. Extrair raiz do CNPJ
        cnpj_raiz = cnpj[:8]

        # 3. Buscar matriz existente com a mesma raiz
        matriz_sql = text("""
            SELECT id FROM empresas 
            WHERE cnpj_raiz = :cnpj_raiz AND is_matriz = 1
        """)
        matriz = self.session.execute(matriz_sql, {"cnpj_raiz": cnpj_raiz}).first()

        # 4. Determinar se é matriz ou filial
        if matriz:
            # É FILIAL - matriz já existe
            is_matriz = False
            matriz_id = matriz.id
            tipo_msg = "filial"
        else:
            # É MATRIZ - primeira empresa dessa raiz
            is_matriz = True
            matriz_id = None  # Será atualizado após insert
            tipo_msg = "matriz"

        # 5. Inserir empresa
        insert_sql = text("""
            INSERT INTO empresas 
            (razao_social, cnpj, cnpj_raiz, uf, simples, aliq_espec, is_matriz, matriz_id)
            VALUES 
            (:razao_social, :cnpj, :cnpj_raiz, :uf, :simples, :aliq_espec, :is_matriz, :matriz_id)
        """)
        
        result = self.session.execute(insert_sql, {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "cnpj_raiz": cnpj_raiz,
            "uf": uf,
            "simples": simples,
            "aliq_espec": aliq_espec,
            "is_matriz": is_matriz,
            "matriz_id": matriz_id
        })
        
        novo_id = result.lastrowid

        # 6. Se for matriz, atualizar matriz_id para o próprio id
        if is_matriz:
            update_sql = text("UPDATE empresas SET matriz_id = :id WHERE id = :id")
            self.session.execute(update_sql, {"id": novo_id})

        self.session.commit()

        return {
            "status": "ok",
            "tipo": tipo_msg,
            "id": novo_id,
            "mensagem": f"Empresa cadastrada como {tipo_msg.upper()}"
        }
```

---

## 📋 Fase 4: Sincronização Inteligente de Produtos

### 4.1 Problema Atual: `INSERT IGNORE`

```python
# ❌ PROBLEMA: Não atualiza dados existentes!
INSERT IGNORE INTO produtos (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id)
VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id)
```

### 4.2 Nova Solução: `INSERT ... ON DUPLICATE KEY UPDATE`

```python
# ✅ SOLUÇÃO: Insere novos OU atualiza existentes
INSERT INTO produtos (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id)
VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id)
ON DUPLICATE KEY UPDATE
    produto = VALUES(produto),
    ncm = VALUES(ncm),
    aliquota = VALUES(aliquota),
    categoriaFiscal = VALUES(categoriaFiscal)
```

### 4.3 Arquivo: `produtoRepository.py` (ATUALIZADO)

```python
import pandas as pd
from sqlalchemy import text

class ProdutoRepository:
    def __init__(self, session):
        self.session = session

    def getEmpresa(self, empresa_id: int):
        query = text("""
            SELECT codigo, produto, ncm, aliquota, categoriaFiscal
            FROM cadastro_tributacao
            WHERE empresa_id = :empresa_id
        """)
        return pd.read_sql_query(query, self.session.bind, params={"empresa_id": empresa_id})

    def inserirDados(self, df: pd.DataFrame, empresa_id: int):
        """
        Sincroniza produtos com INSERT + UPDATE automático.
        - Produtos novos: INSERT
        - Produtos existentes: UPDATE com novos valores
        """
        if df.empty:
            print("[INFO] Nenhum dado encontrado para inserção.")
            return

        df["empresa_id"] = empresa_id

        # Query com INSERT ON DUPLICATE KEY UPDATE
        upsert_query = text("""
            INSERT INTO produtos (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id)
            VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id)
            ON DUPLICATE KEY UPDATE
                produto = VALUES(produto),
                ncm = VALUES(ncm),
                aliquota = VALUES(aliquota),
                categoriaFiscal = VALUES(categoriaFiscal),
                empresa_id = VALUES(empresa_id)
        """)

        dados = df.to_dict(orient="records")

        # Executar em lote
        self.session.execute(upsert_query, dados)
        self.session.commit()

        print(f"[SUCESSO] {len(dados)} produtos sincronizados (novos inseridos + existentes atualizados).")
```

---

## 📋 Fase 5: Atualização do Service de Transferência

### 5.1 Arquivo: `transferDataService.py` (ATUALIZADO)

```python
from ...repositories.transferRepo.empresaRepository import EmpresaRepository
from ...repositories.transferRepo.produtoRepository import ProdutoRepository
from ...services.sync.validacaoTransferService import ValidacaoTransferService

class TransferDataService:
    def __init__(self, sessionICMS, sessionExportacao):
        self.repoEmpresaIcms = EmpresaRepository(sessionICMS)
        self.repoEmpresaExport = EmpresaRepository(sessionExportacao)
        self.repoProdutoIcms = ProdutoRepository(sessionICMS)
        self.repoProdutoExport = ProdutoRepository(sessionExportacao)
        self.validador = ValidacaoTransferService()

    def sincronizarEmpresa(self, empresaIdDestino: int):
        # 1. Buscar empresa no banco exportacao
        empresaDestino = self.repoEmpresaExport.getID(empresaIdDestino)
        if not empresaDestino:
            print("[ERRO] Empresa não encontrada no banco exportacaofortes.")
            return

        cnpj = empresaDestino["cnpj"]
        is_matriz = empresaDestino.get("is_matriz", False)
        matriz_id = empresaDestino.get("matriz_id")
        empresaIdExport = empresaDestino["id"]

        print(f"[INFO] Empresa destino: {empresaDestino['razao_social']} ({cnpj})")

        # 2. Determinar CNPJ para buscar produtos (sempre da matriz)
        if is_matriz:
            cnpj_busca = cnpj
            print(f"[INFO] Empresa é MATRIZ. Buscando produtos próprios.")
        else:
            # Buscar CNPJ da matriz
            matriz_sql = text("SELECT cnpj FROM empresas WHERE id = :matriz_id")
            matriz_result = self.repoEmpresaExport.session.execute(
                matriz_sql, {"matriz_id": matriz_id}
            ).first()
            
            if not matriz_result:
                print(f"[ERRO] Matriz não encontrada (ID: {matriz_id}).")
                return
            
            cnpj_busca = matriz_result.cnpj
            print(f"[INFO] Empresa é FILIAL. Buscando produtos da matriz: {cnpj_busca}")

        # 3. Mapear para empresa no ICMS
        empresaOrigem = self.repoEmpresaIcms.getCnpj(cnpj_busca)
        if not empresaOrigem:
            print(f"[ERRO] Empresa com CNPJ {cnpj_busca} não encontrada no apuradoricms.")
            return

        empresa_id_icms = empresaOrigem["id"]
        print(f"[INFO] Empresa origem encontrada com ID: {empresa_id_icms}")

        # 4. Buscar produtos do ICMS
        df = self.repoProdutoIcms.getEmpresa(empresa_id_icms)
        if df.empty:
            print("[INFO] Nenhum produto encontrado para transferir.")
            return

        print(f"[INFO] {len(df)} produtos encontrados.")

        # 5. Validar dados
        dfValidado = self.validador.validar(df)
        if dfValidado.empty:
            print("[ERRO] Nenhum dado válido para transferir após validação.")
            return
        
        # 6. Sincronizar produtos (INSERT + UPDATE)
        df["empresa_id"] = empresaIdExport
        self.repoProdutoExport.inserirDados(dfValidado, empresaIdExport)

        tipo = "matriz" if is_matriz else "filial"
        print(f"[SUCESSO] Produtos sincronizados para {tipo} {empresaDestino['razao_social']}.")
```

---

## 📋 Fase 6: Atualização do Repository de Transferência

### 6.1 Arquivo: `transferRepo/empresaRepository.py`

```python
from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def getID(self, empresa_id: int):
        query = text("""
            SELECT 
                id, 
                cnpj, 
                cnpj_raiz,
                razao_social, 
                is_matriz,
                matriz_id 
            FROM empresas 
            WHERE id = :id
        """)
        return self.session.execute(query, {"id": empresa_id}).mappings().first()

    def getCnpj(self, cnpj: str):
        query = text("SELECT id, cnpj, razao_social FROM empresas WHERE cnpj = :cnpj")
        return self.session.execute(query, {"cnpj": cnpj}).mappings().first()
```

---

## 📋 Fase 7: Atualização do Controller e Routes

### 7.1 Arquivo: `empresaController.py`

```python
from ..config.db.conexaoFS import getSessionFS
from ..repositories.empresaRepo.empresaRepository import EmpresaRepository
from ..services.cnpjRegister.cnpjService import CnpjService

class EmpresaController:
    def __init__(self):
        self.session = getSessionFS()
        self.repo = EmpresaRepository(self.session)

    def listarEmpresas(self):
        return self.repo.get_all()

    def cadastrarEmpresas(self, razao_social: str, cnpj: str, uf: str, simples: bool, aliq_espec: int = 0):
        # REMOVIDO: cnpj_matriz - sistema decide automaticamente
        return self.repo.insert(razao_social, cnpj, uf, simples, aliq_espec)
    
    def buscarCnpj(self, cnpj: str):
        return CnpjService.consultarCnpj(cnpj)
```

### 7.2 Arquivo: `empresaRoute.py`

```python
from back.src.controllers.empresaController import EmpresaController
from back.src.utils.validadores import removedorCaracteres

class EmpresaRoute:
    @staticmethod
    def listarEmpresas():
        try:
            controller = EmpresaController()
            return controller.listarEmpresas()
        except Exception as e:
            print(f"[ERRO] Falha ao listar empresas: {e}")
            return []

    @staticmethod
    def cadastrarEmpresa(dados: dict):
        try:
            controller = EmpresaController()
            cnpjLimpo = removedorCaracteres(dados["cnpj"])
            
            # REMOVIDO: cnpj_matriz - cadastro 100% automático
            return controller.cadastrarEmpresas(
                dados["razao_social"],
                cnpjLimpo,
                dados["uf"],
                dados["simples"],
                dados.get("aliq_espec", 0)
            )
        except Exception as e:
            print(f"[ERRO] Falha ao cadastrar empresa: {e}")
            return None

    @staticmethod
    def buscarCnpj(cnpj: str):
        try:
            controller = EmpresaController()
            return controller.buscarCnpj(cnpj)
        except Exception as e:
            print(f"[ERRO] Falha ao buscar CNPJ: {e}")
            return None
```

---

## 📋 Fase 8: Atualização da Interface (Frontend)

### 8.1 Arquivo: `cadastroView.py` (SIMPLIFICADO)

```python
# REMOVER checkbox e campo cnpj_matriz
# Interface volta a ser simples - sistema decide tudo

def CadastroView(page: ft.Page) -> ft.View:
    # ... (manter código existente)
    
    # REMOVER:
    # - is_filial_checkbox
    # - cnpj_matriz_input
    # - on_filial_change
    
    def salvar(e):
        if not empresa_dados:
            notificacao(page, "Erro", "Nenhuma empresa carregada.", tipo="erro")
            return

        # REMOVIDO: lógica de cnpj_matriz
        # Sistema decide automaticamente

        try:
            resultado = EmpresaRoute.cadastrarEmpresa(empresa_dados)
            if resultado and resultado.get("status") == "erro":
                notificacao(page, "Info", resultado.get("mensagem"), tipo="info")
            elif resultado and resultado.get("status") == "ok":
                tipo = resultado.get("tipo", "empresa")
                msg = f"Empresa cadastrada como {tipo.upper()}!"
                notificacao(page, "Sucesso", msg, tipo="sucesso")
                page.go("/")
            else:
                notificacao(page, "Erro", "Erro ao cadastrar empresa.", tipo="erro")
        except Exception as ex:
            notificacao(page, "Erro", str(ex), tipo="erro")
```

---

## 📊 Comparativo: ANTES vs DEPOIS

### ❌ ANTES (cnpj_matriz)

| Aspecto | Implementação |
|---------|---------------|
| **Identificação** | Manual via checkbox |
| **Campo** | `cnpj_matriz` CHAR(14) |
| **Relacionamento** | String (duplicação) |
| **Validação** | Manual com query |
| **Sincronização** | `INSERT IGNORE` (sem update) |
| **UX** | 3 campos + validação |

### ✅ DEPOIS (matriz_id + cnpj_raiz)

| Aspecto | Implementação |
|---------|---------------|
| **Identificação** | Automática via raiz CNPJ |
| **Campo** | `matriz_id` INT + `is_matriz` BOOLEAN |
| **Relacionamento** | FK (integridade referencial) |
| **Validação** | Automática no insert |
| **Sincronização** | `ON DUPLICATE KEY UPDATE` |
| **UX** | 1 campo (CNPJ) - zero config |

---

## 🧪 Casos de Teste

### Teste 1: Primeira Empresa de um Grupo
```python
# Entrada
cadastrar_empresa(cnpj="12345678000199", ...)

# Resultado Esperado
{
    "status": "ok",
    "tipo": "matriz",
    "cnpj_raiz": "12345678",
    "is_matriz": True,
    "matriz_id": <próprio_id>
}
```

### Teste 2: Segunda Empresa do Mesmo Grupo
```python
# Entrada
cadastrar_empresa(cnpj="12345678000200", ...)

# Resultado Esperado
{
    "status": "ok",
    "tipo": "filial",
    "cnpj_raiz": "12345678",
    "is_matriz": False,
    "matriz_id": <id_da_matriz>
}
```

### Teste 3: Sincronização com UPDATE
```python
# Banco ICMS
Produto A: aliquota=18%

# Banco FS (antes)
Produto A: aliquota=12%

# Após Sincronização
Produto A: aliquota=18% ✅ (ATUALIZADO!)
```

---

## 📝 Checklist de Implementação

- [ ] **Fase 1**: Executar scripts SQL de alteração do banco
- [ ] **Fase 2**: Atualizar `empresaFsModel.py`
- [ ] **Fase 3**: Atualizar `empresaRepository.py`
- [ ] **Fase 4**: Atualizar `produtoRepository.py` (INSERT ON DUPLICATE)
- [ ] **Fase 5**: Atualizar `transferDataService.py`
- [ ] **Fase 6**: Atualizar `transferRepo/empresaRepository.py`
- [ ] **Fase 7**: Atualizar `empresaController.py` e `empresaRoute.py`
- [ ] **Fase 8**: Simplificar `cadastroView.py`
- [ ] **Teste**: Cadastrar matriz
- [ ] **Teste**: Cadastrar filial
- [ ] **Teste**: Sincronizar produtos (INSERT + UPDATE)
- [ ] **Teste**: Processar SPED da filial

---

## ⚠️ Observações Importantes

1. **Backup**: Fazer backup do banco antes de executar migrations
2. **Ordem**: Executar fases na sequência correta
3. **Testes**: Testar cada fase antes de prosseguir
4. **Rollback**: Manter scripts de rollback preparados

---

## 🎯 Resultado Final

✅ **Cadastro**: Digite CNPJ → Sistema decide matriz/filial automaticamente
✅ **Sincronização**: Produtos sempre atualizados (INSERT + UPDATE)
✅ **Zero configuração**: Sem checkboxes, sem campos extras
✅ **Integridade**: FK garantindo consistência
✅ **Performance**: Índices em cnpj_raiz e matriz_id
