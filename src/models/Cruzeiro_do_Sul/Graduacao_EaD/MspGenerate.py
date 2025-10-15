from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from MODELS.Cruzeiro_do_Sul.Graduacao_EaD import AdjustmentsOffersPattern as aop
from MODELS.Cruzeiro_do_Sul.Graduacao_EaD.ExtraWarningGenerate import ExtraWarningGenerate as ewa
import pandas as pd
class MspGenerate:
    def __init__(self,campus_offers,campus_group):
        self.campus_offers = campus_offers
        self.campus_group = campus_group
        self.columns_map = {
            'NOM_FILI':'Nome da IES',
            'NOME_POL':'Nome do Campus',
            'CURSO':'Nome do Curso',
            'GRAU':'Grau',
            'METODOLOGIA' :'Modalidade',
            'DURAÇÃO':'Duração do Curso',
            'PREÇO PARCELAS':'Mensalidade sem desconto',
            'PORCENTAGEM DE DESCONTO':'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)',
            'COD_CURS':'COD CURSO',
            'ID_POLO':'COD CAMPUS',
            'CÓDIGO DA IES': 'COD IES'
        }    

    def _verify_regression(self):
        try:
            semester = self.campus_offers.loc[3,'Semestre de Ingresso']
            if "." in semester:
                semester = semester.split(".")
                enrollment = semester[1]
                return int(enrollment)
        except Exception:
            raise "ERRO! Semestre de ingresso inválido"
    
    def _set_regression(self):
        regression = self._verify_regression()
        if regression ==  1:
            self.campus_offers['Porcentagem total de desconto da bolsa\n(2º Semestre)'] = self.campus_offers['PORCENTAGEM DE DESCONTO']
    
    def _adjusts_discounts(self):
        self._set_regression()
        self.campus_offers.rename(columns=self.columns_map,inplace= True)
        if 'Porcentagem total de desconto da bolsa\n(2º Semestre)' in self.campus_offers.columns:
            self.campus_offers.rename(columns={'PORCENTAGEM DE DESCONTO':'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'}, inplace=True)
            self.campus_offers.rename(columns={'DESCONTO GARANTIDO':'Porcentagem total de desconto da bolsa\n(3º Semestre)'}, inplace=True)
            self.campus_offers['Porcentagem de desconto IES (1º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'])
            self.campus_offers['Porcentagem de desconto IES (2º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem total de desconto da bolsa\n(2º Semestre)'])
            self.campus_offers['Porcentagem de desconto IES (3º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem total de desconto da bolsa\n(3º Semestre)'])
        else:
            self.campus_offers.rename(columns={'PORCENTAGEM DE DESCONTO':'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)',
                                                'DESCONTO GARANTIDO':'Porcentagem total de desconto da bolsa\n(2º Semestre)'}, inplace=True)
            self.campus_offers['Porcentagem de desconto IES (1º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'])
            self.campus_offers['Porcentagem de desconto IES (2º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem total de desconto da bolsa\n(2º Semestre)'])
            
    def _generate_formatted_percentage_column(self,series):
        series_float = series.astype(str).str.replace(',', '.', regex=False).astype(float) 
        series_float = series_float - 0.05
        return series_float.map(lambda x: f"{x:.2f}")
    
    def _fill_in_remaining_values(self):
        self.campus_offers = dfu.xlookup(self.campus_offers,self.campus_group,'Nome da IES','university_name','university_id','ID da IES')
        self.campus_offers = ewa(self.campus_offers).load()

    def _remaining_columns(self):
        cols_in_df = list(self.campus_offers.columns)
        cols_in_df.remove('Porcentagem total de desconto da bolsa\n(2º Semestre)') 
        idx_ref = cols_in_df.index('Porcentagem de desconto da bolsa (Fixo/1 º Semestre)') + 1
        cols_in_df.insert(idx_ref,'Porcentagem total de desconto da bolsa\n(2º Semestre)')
        self.campus_offers = self.campus_offers[cols_in_df]

    def _generate_virtual_offers(self):
        self.offers_virtual = self.campus_offers.copy()
        self.offers_virtual['Avisos'] = self.offers_virtual['Avisos'] + " | Certificado pela " + self.offers_virtual['Nome da IES']
        self.offers_virtual.loc[:,'ID da IES'] = '3719'
        self.offers_virtual.loc[:,'Nome da IES'] = 'Cruzeiro Virtual'

    def _drop_extra_columns(self):
        self.campus_offers = self.campus_offers.drop(columns=['COD_INST','ID_POLO_HUB','NOME_POLO_HUB','matches_concat','lookup_group','lookup_3719','DES_CURS'])
        self.offers_virtual = self.offers_virtual.drop(columns=['COD_INST','ID_POLO_HUB','NOME_POLO_HUB','matches_concat','lookup_group','lookup_3719','DES_CURS'])

    def load(self):
        self._adjusts_discounts()
        self._fill_in_remaining_values()
        self._remaining_columns()
        self._generate_virtual_offers()
        self._drop_extra_columns()
        return self.campus_offers,self.offers_virtual
