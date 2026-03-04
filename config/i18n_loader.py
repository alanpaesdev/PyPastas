import os
import json
import glob

class I18nLoader:
    @staticmethod
    def load_locales(locales_dir="config/locales"):
        """
        Varre o diretório de locales e carrega todos os arquivos JSON de tradução.
        Retorna um dicionário onde a chave é o 'language_name' (ex: 'Italiano')
        e o valor é o conteúdo completo do JSON.
        """
        translations = {}
        
        # 1. Validação de Rota (O diretório existe?)
        if not os.path.exists(locales_dir):
            print(f"[System Warning] Diretório de idiomas não encontrado: {locales_dir}")
            return translations

        # 2. Varredura Inteligente (Pega apenas arquivos .json)
        json_files = glob.glob(os.path.join(locales_dir, "*.json"))

        for file_path in json_files:
            try:
                # O encoding 'utf-8' é vital para ler acentos do Português e Italiano
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # 3. Validação de Contrato (O arquivo tem o que precisamos?)
                    if "language_name" in data and "structure" in data:
                        lang_name = data["language_name"]
                        translations[lang_name] = data
                    else:
                        print(f"[Data Warning] Arquivo ignorado (falta 'language_name' ou 'structure'): {file_path}")
            
            except json.JSONDecodeError:
                # Captura erros de digitação no JSON (ex: faltou uma vírgula)
                print(f"[Critical Error] Falha de sintaxe no JSON: {file_path}")
            except Exception as e:
                # Fallback para erros de permissão de leitura, etc.
                print(f"[System Error] Falha inesperada ao ler {file_path}: {e}")

        return translations