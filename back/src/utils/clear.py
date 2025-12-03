def clear(self):
        try:
            if self.session:
                self.session.close()
                print("[DEBUG] Sessão do banco de dados fechada")
        except Exception as e:
            print(f"[DEBUG] Erro ao fechar sessão: {e}")
        finally:
            self.session = None
            self.exportar = None
