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
                e.is_matriz,
                e.matriz_id,
                m.razao_social as matriz_razao_social,
                m.cnpj as matriz_cnpj
            FROM empresas e
            LEFT JOIN empresas m ON e.matriz_id = m.id
        """)
        result = self.session.execute(sql).mappings().all()
        return [dict(row) for row in result]

    def insert(self, razao_social: str, cnpj: str, uf: str, simples: bool):
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
            (razao_social, cnpj, cnpj_raiz, uf, simples, is_matriz, matriz_id)
            VALUES 
            (:razao_social, :cnpj, :cnpj_raiz, :uf, :simples, :is_matriz, :matriz_id)
        """)
        
        result = self.session.execute(insert_sql, {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "cnpj_raiz": cnpj_raiz,
            "uf": uf,
            "simples": simples,
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