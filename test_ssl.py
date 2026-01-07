"""
Script de teste para verificar configuração SSL antes de gerar o executável
"""
import sys
import ssl
import certifi
import os

def testar_certificados():
    print("=" * 60)
    print("TESTE DE CONFIGURAÇÃO SSL")
    print("=" * 60)
    
    # 1. Verificar certifi instalado
    print("\n1. Verificando certifi...")
    try:
        cert_path = certifi.where()
        print(f"   ✓ Certifi encontrado: {cert_path}")
        print(f"   ✓ Arquivo existe: {os.path.exists(cert_path)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        return False
    
    # 2. Verificar SSL context
    print("\n2. Verificando SSL Context...")
    try:
        ssl_context = ssl.create_default_context(cafile=cert_path)
        print(f"   ✓ SSL Context criado com sucesso")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        return False
    
    # 3. Testar requisição HTTPS
    print("\n3. Testando requisição HTTPS...")
    try:
        import aiohttp
        import asyncio
        
        async def testar_requisicao():
            timeout = aiohttp.ClientTimeout(total=10)
            ssl_ctx = ssl.create_default_context(cafile=cert_path)
            connector = aiohttp.TCPConnector(ssl=ssl_ctx)
            
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.get('https://minhareceita.org/27865757000102') as response:
                    return response.status
        
        status = asyncio.run(testar_requisicao())
        print(f"   ✓ Requisição HTTPS funcionou! Status: {status}")
    except Exception as e:
        print(f"   ✗ Erro na requisição: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("TODOS OS TESTES PASSARAM! ✓")
    print("O executável deve funcionar corretamente.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    sucesso = testar_certificados()
    sys.exit(0 if sucesso else 1)
