from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
import os
from datetime import date

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
            if "CURSOS DE GRADUAÇÃO" in init_title:
                self.discount_df = init_title
            header = self.offers.iloc[titles[i] + 1].tolist()
            data = self.offers.iloc[titles[i] + 2:titles[i + 1]]
            data.columns = header
            data = data.dropna(how='all').dropna(axis=1, how='all')
            self.tables[init_title] = data.reset_index(drop=True)
    
    def _set_percentage_discount(self):
        discounts = self.tables[self.discount_df]
        for header in discounts.columns:
            if pd.isna(header) or header == "%":
                continue
        disc_str = str(discounts[header].iloc[-1])
        df_offer = self.tables[header]
        if "-" in disc_str:
            df_offer.loc['Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'] = discounts.iloc[-2,-1]
        else:
            df_offer.loc['Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'] = discounts.iloc[-1,-1]

    def _drop_extra_columns(self):
        for df in self.tables.keys():
            self.tables[df] = self.tables[df].drop(self.tables[df].columns[-4], axis=1)
            self.tables[df] = self.tables[df].drop(columns= ['Duração do Curso','PRÁTICA','ESTÁGIO','TCC'])

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
        })  
    
    def _treatment_columns(self):
        self.offers_concatened = dfu.replace_series(self.offers_concatened,'Plano de Pagamento',' Mensalidades','')
        kinds = {'Tecnólogo': 'Tecnólogo (graduação)',
                  'Bacharelado': 'Bacharelado (graduação)',
                  'Licenciatura': 'Licenciatura (graduação)'}
        self.offers_concatened = self._multiple_replaces(self.offers_concatened,'Modalidade',kinds)
    
    def _adjust_course_duration(self):
        self.offers_concatened['Duração do Curso'] = self.offers_concatened['Duração do Curso'].astype(int)
        self.offers_concatened['Duração do Curso'] = self.offers_concatened['Duração do Curso'] // 6

    def get_date_actually(self):
        today = date.today()
        return today.strftime("%d/%m/%Y")

    def _add_extra_columns(self):
        self.offers_concatened['Nome da IES'] = 'UniFatecie'
        self.offers_concatened['ID da IES'] = 231
        self.offers_concatened['Nome do Campus'] = 'todos'
        self.offers_concatened['ID do Campus'] = 'todos'
        self.offers_concatened['Modalidade'] = 'EaD'
        self.offers_concatened['Turno'] = 'Virtual'
        self.offers_concatened['Tipo de duração do curso'] = 'Semestre'
        self.offers_concatened['Qual valor usar?\n% ou R$'] = 'porcentagem'
        self.offers_concatened['LIMITADA?'] = 'FALSE'
        self.offers_concatened['Semestre de Ingresso'] = 'Início Imediato'
        self.offers_concatened.loc[:, 'Data de Início da Oferta'] = self.get_date_actually()

    def load(self):
        self._load_dataframes()
        self._separate_tables_in_df()
        self._set_percentage_discount()
        self._drop_extra_columns()
        self._concat_offers_df()
        self._rename_columns()
        self._treatment_columns()
        self._adjust_course_duration()
        self._add_extra_columns()

    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe