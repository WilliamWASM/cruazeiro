from .excel_file.SheetManipulation import SheetManipulation as sma
from .excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
import os
from datetime import date
import re

class Unifatecie:
    def __init__(self,ies_offers):
        self.offers = ies_offers
        self._load_dataframes()
        self._separate_tables_in_df()

    def _load_dataframes(self):
        self.offers = sma(self.offers).load_not_header()

    def _separate_tables_in_df(self):
        titles = self.offers[self.offers[0].astype(str).str.startswith(("CURSOS", "DESCRIÇÃO"), na=False)].index.tolist()
        titles.append(len(self.offers))
        self.tables = {}

        name_titles = [self.offers.iloc[i,0] for i in titles[:-1]]

        for i in range(len(titles) - 1):
            start = titles[i]
            end = titles[i + 1] - 2
            init_title = self.offers.iloc[start, 0]

            if "CURSOS DE GRADUAÇÃO" in init_title:
                self.discount_df = init_title

            header = self.offers.iloc[start + 1].tolist()
            data = self.offers.iloc[start + 2:end + 1]

            if "CURSOS GRUPO V" in init_title:
                end = ((data.isna().idxmax())[1]) -1
                data = self.offers.iloc[start + 2:end + 1]

            data.columns = header
            data = data.dropna(how='all').dropna(axis=1, how='all')
            self.tables[init_title] = data.reset_index(drop=True)

    def _separate_warnings(self):
        self.warning_for_disc = {}
        self.reajust = " "

        warnings_df = (self.tables['DESCRIÇÃO DA PROMOÇÃO:'].iloc[:, 0].tolist() +
        self.tables['DESCRIÇÃO DA PROMOÇÃO:'].columns.tolist())
        for warning in warnings_df:
            warning_txt = str(warning).replace("*", "").strip()
            if "OBS:" in warning_txt:
                warning_txt = warning_txt.replace("OBS:","").strip()
                self.reajust = str(warning_txt)
            match_grp = re.search(r'GRUPOS?\s+(.+?)(?:\.|$)', warning_txt, re.IGNORECASE)
            if match_grp:
                trunc_txt = re.search(r'(.*graduação)',warning_txt)
                trunc_txt = trunc_txt.group(1)
                groups = re.split(r'\s*(?:e|,)\s*', match_grp.group(1))
                for group in groups:
                    group =group.strip()
                    group = group.replace(".","")
                    self.warning_for_disc[f'CURSOS GRUPO {group}'] = trunc_txt

    def _set_warnings(self):
        for group, warning in self.warning_for_disc.items():
            if "COM REAJUSTE ANUAL" in warning:
                warning = warning + ". " + self.reajust
            group_course = self.tables[group]
            group_course['Avisos'] = warning
 
    def _set_percentage_discount(self):
        discounts = self.tables[self.discount_df]
        for header in discounts.columns:
            if pd.isna(header) or header == "%":
                continue
            disc_str = str(discounts[header].iloc[-1])
            if header =="CURSOS BASE":
                header = "CURSOS GRUPO BASE"
            df_offer = self.tables[header]
            if "-" in disc_str:
                disc_value = f"{discounts.iloc[-2,-1]:.2f}"
                df_offer.loc[:,'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'] = disc_value
            else:
                disc_value = f"{discounts.iloc[-1,-1]:.2f}"
                df_offer.loc[:,'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'] = disc_value

    def _concat_offers_df(self):
        tables_offers = ['CURSOS GRUPO BASE','CURSOS GRUPO I','CURSOS GRUPO II','CURSOS GRUPO III','CURSOS GRUPO IV','CURSOS GRUPO V']
        for key,df in self.tables.items():
            df.columns = df.columns.str.lower().str.strip()
            self.tables[key] = df
        for title in tables_offers:
            self.tables[title] = self.tables[title].loc[:,['curso','modalidade','valor bruto','plano de pagamento','avisos','benefício 1 (chave osc)',
                                                           'data de fim da oferta','porcentagem de desconto da bolsa (fixo/1 º semestre)']]
        self.offers_concatened = dfu.concat_multiples_dataframes([self.tables['CURSOS GRUPO BASE'],self.tables['CURSOS GRUPO I'],
                                                                  self.tables['CURSOS GRUPO II'],self.tables['CURSOS GRUPO III'],
                                                                  self.tables['CURSOS GRUPO IV'],self.tables['CURSOS GRUPO V']])
    
    def _treatment_columns(self):
        self.offers_concatened = dfu.replace_series(self.offers_concatened,'plano de pagamento',' Mensalidades','')
        kinds = {'Tecnólogo': 'Tecnólogo (graduação)',
                  'Bacharelado': 'Bacharelado (graduação)',
                  'Licenciatura': 'Licenciatura (graduação)'}
        self.offers_concatened = self._multiple_replaces(self.offers_concatened,'modalidade',kinds)
        
    def _adjust_course_duration(self):
        self.offers_concatened['plano de pagamento'] = self.offers_concatened['plano de pagamento'].astype(int)
        self.offers_concatened['plano de pagamento'] = self.offers_concatened['plano de pagamento'] // 6
    
    def _add_extra_columns(self):
        self.offers_concatened['Nome da IES'] = 'UniFatecie'
        self.offers_concatened['ID da IES'] = 231
        self.offers_concatened['Nome do Campus'] = 'todos'
        self.offers_concatened['ID do Campus'] = 'todos'
        self.offers_concatened['modalidade'] = 'EaD'
        self.offers_concatened['Turno'] = 'Virtual'
        self.offers_concatened['Tipo de duração do curso'] = 'Semestre'
        self.offers_concatened['Qual valor usar?\n% ou R$'] = 'porcentagem'
        self.offers_concatened['Porcentagem de desconto IES'] = '0.70'
        self.offers_concatened['LIMITADA?'] = 'FALSE'
        self.offers_concatened['Semestre de Ingresso'] = 'Início Imediato'
        self.offers_concatened.loc[:, 'Data de Início da Oferta'] = self.get_date_actually()
    
    def _rename_columns(self):
        self.offers_concatened = self.offers_concatened.rename(columns={
            'curso': 'Nome do Curso',
            'modalidade': 'Grau',
            'plano de pagamento': 'Duração do Curso',
            'valor bruto': 'Mensalidade sem desconto',
            'benefício 1 (chave osc)': 'Benefício 1 (Chave OSC)',
            'data de fim da oferta': 'Data de Fim da Oferta',
            'avisos': 'Avisos',
            'porcentagem de desconto da bolsa (fixo/1 º semestre)': 'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'

        })  

    def get_date_actually(self):
        today = date.today()
        return today.strftime("%d/%m/%Y")

    def set_values(self,end_date,osc):
        for group,df in self.tables.items():
            if 'Curso' in df.columns:
                df['Benefício 1 (Chave OSC)'] = osc
                df.loc[:,'Data de Fim da Oferta'] = end_date
    
    def _substitute_kind_by_course(self):
        mask = self.offers_concatened[ 'Nome do Curso'].str.contains('^\\d', case=False, na=False)
        self.offers_concatened.loc[mask, 'Grau'] = 'Segunda Graduação'
        mask = self.offers_concatened[ 'Nome do Curso'].str.contains('Formação Pedagógica ', case=False, na=False)
        self.offers_concatened.loc[mask, 'Grau'] = 'Segunda Graduação'
        mask = self.offers_concatened[ 'Nome do Curso'].str.contains('(Semi-presencial)', case=False, na=False)
        self.offers_concatened.loc[mask, 'modalidade'] = 'Semipresencial'

    def load(self,path):
        self._separate_warnings()
        self._set_warnings()
        self._set_percentage_discount()
        self._concat_offers_df()
        self._treatment_columns()
        self._adjust_course_duration()
        self._rename_columns()
        self._add_extra_columns()
        self._substitute_kind_by_course()
        print(self.offers_concatened)
        try:
            dfu.save_dataframe(self.offers_concatened,path,"MSP Ofertas")
        except Exception as e:
            print (f"Erro durante o salvamento dos arquivos: {e}")

    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe