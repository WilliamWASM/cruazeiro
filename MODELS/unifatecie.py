from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
import os
class Unifatecie:
    def __init__(self,ies_offers):
        self.offers = ies_offers

    def _load_dataframes(self):
        self.offers = sma(self.offers).load_not_header()

    def _separate_tables_in_df(self):
        titles = self.offers[self.offers[0].astype(str).str.startswith(("CURSOS", "DESCRIÇÃO"), na=False)].index.tolist()
        titles.append(len(self.offers))
        self.tables = {}

        for i in range(len(titles) - 1):
            init_title = self.offers.iloc[titles[i], 0]
            header = self.offers.iloc[titles[i] + 1].tolist()
            data = self.offers.iloc[titles[i] + 2:titles[i + 1]]

            data.columns = header
            data = data.dropna(how='all').dropna(axis=1, how='all')

            self.tables[init_title] = data.reset_index(drop=True)
    
    def _concat_offers_df(self):
        self.offers_concatened = dfu.concat_multiples_dataframes([self.tables['CURSOS GRUPO BASE'],self.tables['CURSOS GRUPO I'],
                                                                  self.tables['CURSOS GRUPO II'],self.tables['CURSOS GRUPO III'],
                                                                  self.tables['CURSOS GRUPO IV'],self.tables['CURSOS GRUPO V']])
        
    def _rename_columns(self):
        self.offers_concatened = self.offers_concatened.rename(columns={
            'Curso': 'Nome do Curso',
            'Modalidade': 'Grau',
            'Plano de Pagamento': 'Duração do Curso',
            'VALOR BRUTO': 'Mensalidade sem desconto',
            'VALOR COM 83%': 'Mensalidade com desconto'
        })
    
    def _treatment_columns(self):
        self.offers_concatened = dfu.replace_series(self.offers_concatened,'Plano de Pagamento',' Mensalidades','')
        kinds = {'Tecnólogo': 'Tecnólogo (graduação)',
                  'Bacharelado': 'Bacharelado (graduação)',
                  'Licenciatura': 'Licenciatura (graduação)'}
        self.offers_concatened = self._multiple_replaces(self.offers_concatened,'Modalidade',kinds)

    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe