import os
import pandas as pd
import numpy as np
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from MODELS.Utilities.dicionarios import lista_cidades
from GUI.widgets.notifications import Notification

class CorrigirCidades:
    def __init__(self, xlsx_file):
        self.lista_cidades = lista_cidades
        self.df = sma(xlsx_file).load()
        base_name = os.path.basename(xlsx_file)
        dir_name = os.path.dirname(xlsx_file)
        new_name = "fixed_cities_" + base_name
        self.fixed_file = os.path.join(dir_name, new_name)

    def levenshtein_distance(self, s1, s2):
        len_s1, len_s2 = len(s1), len(s2)
        dp = np.zeros((len_s1 + 1, len_s2 + 1), dtype=int)

        for i in range(len_s1 + 1):
            dp[i][0] = i
        for j in range(len_s2 + 1):
            dp[0][j] = j

        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                if s1[i - 1] == s2[j - 1]:  
                    cost = 0  
                else:
                    cost = 1  
                
                dp[i][j] = min(dp[i - 1][j] + 1,        # Remoção
                            dp[i][j - 1] + 1,           # Inserção
                            dp[i - 1][j - 1] + cost)    # Substituição
        
        return dp[len_s1, len_s2]
    
    def encontrar_correspondente(self, word, word_list):
        if word in word_list:
            return word
        closest_word = min(word_list, key = lambda x: self.levenshtein_distance(word.lower(), x.lower()))
        return closest_word if closest_word.lower()!=word.lower() else word

    def fix_cities(self):
        if self.df is None:
            Notification.error("Erro ao carregar df","⚠️ Dados não carregados.")
            return
        for idx, row in self.df.iterrows():
            cidade, estado = row["city"], row["state"]
            cidades_estado = self.lista_cidades.get(estado, [])
            if cidades_estado:
                cidade_corrigida = self.encontrar_correspondente(cidade, cidades_estado)
                self.df.at[idx, "city"] = cidade_corrigida

    def executar(self):
        self.fix_cities()
        dfu.save_dataframe(self.df, self.fixed_file,"MSP_Cities_Fixed")
        Notification.info("Correção de Cidades", f"✅ Correção de cidades concluída. Arquivo salvo como: {self.fixed_file}")