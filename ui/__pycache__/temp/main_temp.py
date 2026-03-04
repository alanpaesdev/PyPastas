import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class FolderBot:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Organizational Intelligence - Multi-Year Architect")
        self.root.geometry("500x550")
        self.selected_path = tk.StringVar()
        self.year_vars = {}

        # 1. Título
        tk.Label(root, text="Arquitetura de Pastas Financeiras", font=("Helvetica", 14, "bold")).pack(pady=10)

        # 2. Seleção de Caminho
        ttk.Button(root, text="1. Selecionar Localização Raiz", command=self.browse_folder).pack(pady=5)
        tk.Entry(root, textvariable=self.selected_path, width=60, state='readonly').pack(pady=5, padx=20)

        # 3. Painel de Seleção de Anos (2000 até hoje)
        tk.Label(root, text="2. Selecione os Anos:", font=("Helvetica", 10, "bold")).pack(pady=5)
        
        # Frame com Scrollbar para os anos
        container = ttk.Frame(root)
        container.pack(fill="both", expand=True, padx=40, pady=5)
        
        canvas = tk.Canvas(container, height=200)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        current_year = datetime.now().year
        for year in range(2000, current_year + 1):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(scrollable_frame, text=str(year), variable=var)
            cb.pack(anchor="w")
            self.year_vars[year] = var

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 4. Botão de Gatilho
        self.btn_create = ttk.Button(root, text="3. Criar Estruturas Selecionadas", command=self.create_folders, state='disabled')
        self.btn_create.pack(pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Selecione o diretório raiz")
        if folder:
            self.selected_path.set(folder)
            self.btn_create.configure(state='normal')

    def create_folders(self):
        base_path = self.selected_path.get()
        selected_years = [year for year, var in self.year_vars.items() if var.get()]

        if not selected_years:
            messagebox.showwarning("Aviso", "Por favor, selecione ao menos um ano.")
            return

        root_folder = "FINANCEIRO"
        months = {
            1: "JANEIRO", 2: "FEVEREIRO", 3: "MARCO", 4: "ABRIL",
            5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
            9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"
        }
        categories = ["01_NOTAS_FISCAIS", "02_EXTRATOS", "03_PAGAMENTOS", "04_CONTABILIDADE"]

        try:
            for year in selected_years:
                for month_num, month_name in months.items():
                    # NOVO PADRÃO: MM_NOMEDOMES (Ex: 02_FEVEREIRO)
                    month_folder_name = f"{month_num:02d}_{month_name}"
                    
                    for category in categories:
                        full_path = os.path.join(base_path, root_folder, str(year), month_folder_name, category)
                        os.makedirs(full_path, exist_ok=True)
            
            messagebox.showinfo("Sucesso", f"Estrutura criada para {len(selected_years)} anos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na criação: {e}")

if __name__ == "__main__":
    app_root = tk.Tk()
    FolderBot(app_root)
    app_root.mainloop()