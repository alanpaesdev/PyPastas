import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class LifeOSUniversal:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeOS 7.0 - Universal Framework")
        self.root.geometry("520x380")
        self.selected_path = tk.StringVar()

        # UI Estilizada
        tk.Label(root, text="LifeOS 7.0: Automação Universal", font=("Helvetica", 14, "bold")).pack(pady=20)
        
        ttk.Button(root, text="1. Escolher Local de Instalação", command=self.browse).pack(pady=5)
        tk.Entry(root, textvariable=self.selected_path, width=60, state='readonly').pack(pady=5, padx=20)

        self.status_label = tk.Label(root, text="Aguardando seleção...", fg="gray")
        self.status_label.pack(pady=10)

        self.btn_deploy = ttk.Button(root, text="2. Gerar Estrutura Completa", command=self.deploy, state='disabled')
        self.btn_deploy.pack(pady=20)

    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_path.set(folder)
            self.btn_deploy.configure(state='normal')
            self.status_label.config(text="Pronto para o Deploy", fg="green")

    def deploy(self):
        base = self.selected_path.get()
        current_year = datetime.now().year
        months = {1:"01_JAN", 2:"02_FEVEREIRO", 3: "03_MARCO", 4:"04_ABRIL", 5:"05_MAIO", 6:"06_JUNHO", 
                  7:"07_JULHO", 8:"08_AGOSTO", 9:"09_SETEMBRO", 10:"10_OUTUBRO", 11:"11_NOVEMBRO", 12:"12_DEZEMBRO"}

        # Arquitetura Refatorada: Alta Coesão no Domínio Financeiro e Nomes Universais
        structure = {
            "01_IDENTIDADE": ["DOCUMENTOS"],
            "02_FINANCEIRO": ["NOTAS_FISCAIS","HABITACAO", "ALIMENTACAO", "CONTAS_CONSUMO", "NOTAS_FISCAIS", "SEGUROS", "IMPOSTOS", "PATRIMONIO"],
            "03_SAUDE": ["EXAMES", "RECEITAS_MEDICAS", "VACINAS"],
            "04_VEICULOS": ["DOCUMENTACAO", "MANUTENCAO", "MULTAS"],
            "05_DESENVOLVIMENTO": ["ESTUDOS", "CARREIRA", "CURSOS"],
            "06_PROJETOS": ["ATIVOS", "ARQUIVADOS"],
            "07_MEMORIA": ["FOTOS","VIDEOS", "LEGADO"]
        }

        try:
            # 1. Deploy dos Domínios e Subdomínios
            for principal, subs in structure.items():
                p_path = os.path.join(base, principal)
                for s in subs:
                    os.makedirs(os.path.join(p_path, s), exist_ok=True)

            # 2. Geração do Histórico Financeiro e de Imagens (2000 - Hoje)
            for year in range(2000, current_year + 1):
                # O FLUXO MENSAL entra como o "motor" dentro do Financeiro
                for m_name in months.values():
                    fluxo_path = os.path.join(base, "02_FINANCEIRO", "FLUXO_MENSAL", str(year), m_name)
                    os.makedirs(fluxo_path, exist_ok=True)
                
                # Memória Visual Anual
                os.makedirs(os.path.join(base, "07_MEMORIA", "FOTOS", str(year)), exist_ok=True)

            messagebox.showinfo("Deploy Realizado", "Estrutura Universal LifeOS 7.0 (Refatorada) criada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro de Deploy", f"Falha na execução: {e}")

if __name__ == "__main__":
    app = tk.Tk()
    LifeOSUniversal(app)
    app.mainloop()