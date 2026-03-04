import os
from datetime import datetime

class FolderArchitect:
    @staticmethod
    def build_structure(base_path, lang_data, selected_years):
        structure = lang_data.get("structure", {})
        months = lang_data.get("months", [])
        archive_name = lang_data.get("archive_dir", "HISTORICO") # O nome da pasta de Cold Storage
        
        # Carrega as regras de volume
        rules = lang_data.get("partition_rules", {})
        yearly_rules = rules.get("yearly", [])
        yearly_monthly_rules = rules.get("yearly_monthly", [])

        # Lógica de Data Tiering (Hot vs Cold Storage)
        current_year = datetime.now().year
        hot_years = [current_year, current_year - 1, current_year - 2] # Ex: 2026, 2025, 2024

        # Função Interna para injetar os anos/meses baseado nas regras
        def _apply_time_partitions(target_path, folder_name):
            if folder_name in yearly_monthly_rules or folder_name in yearly_rules:
                for year in selected_years:
                    # Roteamento Inteligente: Hot ou Cold Storage?
                    if year in hot_years:
                        year_path = os.path.join(target_path, str(year))
                    else:
                        year_path = os.path.join(target_path, archive_name, str(year))
                    
                    os.makedirs(year_path, exist_ok=True)
                    
                    # Injeta os meses se for regra de alto volume
                    if folder_name in yearly_monthly_rules:
                        for month in months:
                            os.makedirs(os.path.join(year_path, month), exist_ok=True)

        # Função Recursiva: Lê dicionários {} e listas [] infinitamente
        def _build_tree(current_path, node):
            if isinstance(node, dict):
                for folder_name, sub_node in node.items():
                    new_path = os.path.join(current_path, folder_name)
                    os.makedirs(new_path, exist_ok=True)
                    _apply_time_partitions(new_path, folder_name)
                    _build_tree(new_path, sub_node)
            
            elif isinstance(node, list):
                for folder_name in node:
                    new_path = os.path.join(current_path, folder_name)
                    os.makedirs(new_path, exist_ok=True)
                    _apply_time_partitions(new_path, folder_name)

        try:
            # 1. Constrói a árvore universal (com as regras de negócio e Cold Storage)
            _build_tree(base_path, structure)

            # 2. Constrói a regra especial de Mídia (MEDIA > [ANO] > FOTOS/VIDEOS)
            if "media_root" in lang_data and "media_subdirs" in lang_data:
                memory_root = list(structure.keys())[6] 
                media_base = os.path.join(base_path, memory_root, lang_data["media_root"])
                
                for year in selected_years:
                    # Aplica a mesma regra de Data Tiering para as mídias
                    if year in hot_years:
                        year_path = os.path.join(media_base, str(year))
                    else:
                        year_path = os.path.join(media_base, archive_name, str(year))
                        
                    for subdir in lang_data["media_subdirs"]:
                        os.makedirs(os.path.join(year_path, subdir), exist_ok=True)
            
            return True, "Estrutura gerada com Data Tiering e particionada com sucesso!"
        except Exception as e:
            return False, f"Erro crítico de I/O: {str(e)}"