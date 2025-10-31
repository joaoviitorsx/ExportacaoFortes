import time
from typing import List
from ....src.services.etl.leitorService import LeitorService
from ....src.services.etl.persistenciaService import PersistenciaService
from ....src.services.etl.softDeleteService import SoftDeleteService


class PipelineService:
    """
    Pipeline LINEAR para processamento de arquivos SPED Fiscal.
    Processa um arquivo por vez, garantindo consistência.
    """

    def __init__(self, session, empresa_id: int, arquivos: List[str]):
        self.session = session
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        
        self.leitor = LeitorService(session, empresa_id)
        self.persistencia = PersistenciaService(session)
        
        self.stats_global = {
            "tempo_inicio": None,
            "tempo_fim": None,
            "arquivos_processados": 0,
            "c100_total": 0,
            "c170_total": 0,
            "c190_total": 0,
            "notas_ignoradas_total": 0,
            "erros": []
        }

    def executar(self):
        """Executa o pipeline completo"""
        print(f"\n{'='*80}")
        print(f"🚀 PIPELINE SPED FISCAL - MODO LINEAR")
        print(f"{'='*80}")
        print(f"📁 Arquivos: {len(self.arquivos)}")
        print(f"🏢 Empresa:  {self.empresa_id}")
        print(f"{'='*80}\n")

        self.stats_global["tempo_inicio"] = time.time()

        # Soft delete prévio
        try:
            periodo = SoftDeleteService.extrairPeriodo(self.arquivos)
            print(f"🧹 Aplicando soft delete: período {periodo}")
            SoftDeleteService.softDelete(self.session, self.empresa_id, periodo)
            print(f"✅ Soft delete concluído\n")
        except Exception as e:
            print(f"⚠️ Erro no soft delete: {e}\n")

        # Processar cada arquivo sequencialmente
        for idx, arquivo in enumerate(self.arquivos, 1):
            print(f"\n{'─'*80}")
            print(f"📄 [{idx}/{len(self.arquivos)}] {arquivo}")
            print(f"{'─'*80}")
            
            try:
                # 1. Ler arquivo
                dados = self.leitor.ler_arquivo(arquivo)
                
                # 2. Salvar no banco
                stats = self.persistencia.salvar_arquivo(dados)
                
                # 3. Atualizar estatísticas
                self.stats_global["arquivos_processados"] += 1
                self.stats_global["c100_total"] += stats["c100"]
                self.stats_global["c170_total"] += stats["c170"]
                self.stats_global["c190_total"] += stats["c190"]
                self.stats_global["notas_ignoradas_total"] += stats["notas_ignoradas"]
                
                print(f"✅ Arquivo processado com sucesso!")
                
            except Exception as e:
                erro_msg = f"Erro ao processar {arquivo}: {e}"
                self.stats_global["erros"].append(erro_msg)
                print(f"❌ {erro_msg}")
                import traceback
                traceback.print_exc()

        # Estatísticas finais
        self.stats_global["tempo_fim"] = time.time()
        self._exibir_estatisticas()

        return self.stats_global

    def _exibir_estatisticas(self):
        """Exibe estatísticas finais consolidadas"""
        tempo_total = self.stats_global["tempo_fim"] - self.stats_global["tempo_inicio"]
        
        print(f"\n{'='*80}")
        print(f"📊 ESTATÍSTICAS FINAIS")
        print(f"{'='*80}")
        
        print(f"\n⏱️  Tempo:")
        print(f"   ├─ Total:                {tempo_total:.2f}s")
        if self.arquivos:
            print(f"   └─ Médio por arquivo:    {tempo_total/len(self.arquivos):.2f}s")
        
        print(f"\n📁 Arquivos:")
        print(f"   ├─ Total:                {len(self.arquivos)}")
        print(f"   ├─ Processados:          {self.stats_global['arquivos_processados']}")
        print(f"   └─ Com erro:             {len(self.stats_global['erros'])}")
        
        print(f"\n📋 Registros salvos:")
        print(f"   ├─ C100 (Notas):         {self.stats_global['c100_total']:,}")
        print(f"   ├─ C170 (Itens):         {self.stats_global['c170_total']:,}")
        print(f"   ├─ C190 (Totalizadores): {self.stats_global['c190_total']:,}")
        print(f"   └─ Notas ignoradas:      {self.stats_global['notas_ignoradas_total']:,}")
        
        if self.stats_global['c100_total'] > 0:
            print(f"\n📊 Médias:")
            print(f"   ├─ C170 por nota:        {self.stats_global['c170_total']/self.stats_global['c100_total']:.2f}")
            print(f"   └─ C190 por nota:        {self.stats_global['c190_total']/self.stats_global['c100_total']:.2f}")
        
        if self.stats_global['erros']:
            print(f"\n❌ Erros ({len(self.stats_global['erros'])}):")
            for i, erro in enumerate(self.stats_global['erros'], 1):
                print(f"   {i}. {erro}")
        
        print(f"\n{'='*80}\n")