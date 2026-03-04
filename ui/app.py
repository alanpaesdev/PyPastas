import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from config.i18n_loader import I18nLoader
from core.architect import FolderArchitect

class LifeOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeOS 7.0 - Universal Framework")
        self.root.geometry("650x680") # Janela um pouco mais alta
        self.selected_path = tk.StringVar()
        self.root_folder_var = tk.StringVar(value="Paes_LifeOS") # Pasta 0 (Root Namespace)
        self.lang_var = tk.StringVar()
        self.year_vars = {}
        
        # Injeção de Dependência
        self.translations_db = I18nLoader.load_locales("config/locales")

        self._build_ui()

    def _build_ui(self):
        # Cabeçalho e Idioma
        tk.Label(self.root, text="LifeOS 7.0: Automação Universal", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(pady=5)
        tk.Label(lang_frame, text="Idioma / Language:").pack(side="left", padx=5)
        
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, state="readonly", width=20)
        idiomas_disponiveis = list(self.translations_db.keys())
        self.lang_combo['values'] = idiomas_disponiveis
        if idiomas_disponiveis:
            self.lang_combo.current(0)
        self.lang_combo.pack(side="left")

        # NOVO: O "Container" Principal (A Pasta 0)
        tk.Label(self.root, text="0. Nome da Pasta Principal (Root Workspace):", font=("Helvetica", 10, "bold"), fg="#333333").pack(pady=(15, 2))
        tk.Entry(self.root, textvariable=self.root_folder_var, width=50).pack(pady=5)

        # Diretório Base
        ttk.Button(self.root, text="1. Escolher Local de Instalação", command=self.browse).pack(pady=10)
        tk.Entry(self.root, textvariable=self.selected_path, width=75, state='readonly').pack(pady=5, padx=20)

        # Matriz de Anos
        tk.Label(self.root, text="2. Anos Anteriores Opcionais (Fluxo/Mídia):", font=("Helvetica", 10, "bold")).pack(pady=10)
        grid_frame = ttk.Frame(self.root)
        grid_frame.pack(pady=5)

        current_year = datetime.now().year
        for i, year in enumerate(range(2000, current_year + 1)):
            is_current_year = (year == current_year)
            var = tk.BooleanVar(value=is_current_year)
            cb = tk.Checkbutton(grid_frame, text=str(year), variable=var)
            if is_current_year:
                cb.config(state="disabled")
            cb.grid(row=i // 6, column=i % 6, padx=10, pady=2, sticky="w")
            self.year_vars[year] = var

        # Botões de Ação Rápida
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Selecionar Todos", command=self.select_all).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_all).pack(side="left", padx=5)

        # Gatilho
        self.status_label = tk.Label(self.root, text="Aguardando seleção do diretório...", fg="gray")
        self.status_label.pack(pady=10)
        self.btn_deploy = ttk.Button(self.root, text="3. Gerar Estrutura", command=self.deploy, state='disabled')
        self.btn_deploy.pack(pady=10)

    def select_all(self):
        for var in self.year_vars.values():
            var.set(True)

    def clear_all(self):
        current_year = datetime.now().year
        for year, var in self.year_vars.items():
            if year != current_year: 
                var.set(False)

    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_path.set(folder)
            self.btn_deploy.configure(state='normal')
            self.status_label.config(text="Pronto para o Deploy", fg="green")

    def deploy(self):
        base_path = self.selected_path.get()
        root_folder_name = self.root_folder_var.get().strip()
        selected_lang = self.lang_var.get()
        
        # Validação de segurança
        if not base_path:
            return messagebox.showwarning("Aviso", "Selecione um local de instalação primeiro.")

        # A MÁGICA ACONTECE AQUI: Cria o encapsulamento da "Pasta 0"
        # Se o usuário digitar algo, junta. Se deixar em branco, usa a raiz.
        target_path = os.path.join(base_path, root_folder_name) if root_folder_name else base_path

        selected_years = [year for year, var in self.year_vars.items() if var.get()]
        lang_data = self.translations_db[selected_lang]
        
        # Envia para a regra de negócios o novo caminho encapsulado
        success, message = FolderArchitect.build_structure(target_path, lang_data, selected_years)

        if success:
            messagebox.showinfo("Deploy Concluído", f"Sucesso!\nSistema criado em: {target_path}")
        else:
            messagebox.showerror("Erro de I/O", f"Falha no Deploy: {message}")