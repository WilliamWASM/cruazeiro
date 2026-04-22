from ...excel_file.SheetManipulation import SheetManipulation as sma
from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
from ..Graduacao_EaD.AdjustmentsOffersPattern import AdjustmentsOffersPattern as aop
from ..Graduacao_EaD.ExtraWarningGenerate import ExtraWarningGenerate as ewa
import pandas as pd
class MspGenerate:
    def __init__(self,campus_offers,campus_group):
        self.campus_offers = campus_offers
        self.campus_group = campus_group
        self.columns_map = {
            'CERTIFICADORA':'Nome da IES',
            'NOME_POL':'Nome do Campus',
            'CURSO':'Nome do Curso',
            'GRAU':'Grau',
            'MODALIDADE':'Modalidade',
            'DURACAO':'Duração do Curso',
            'PRECO_PARCELAS':'Mensalidade sem desconto',
            'PORCENTAGEM_DESCONTO':'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)',
            'COD_CURSO':'COD CURSO',
            'ID_POLO':'COD CAMPUS',
            'COD_IES': 'COD IES'
        }

    def _verify_regression(self):
        if self.campus_offers.empty:
            raise ValueError("ERRO! Nenhuma oferta encontrada. Verifique se os códigos de curso da planilha de relação correspondem aos da planilha de ofertas.")
        try:
            semester = str(self.campus_offers['Semestre de Ingresso'].iloc[0])
            if "." in semester:
                enrollment = semester.split(".")[1]
                return int(enrollment)
        except Exception as e:
            raise ValueError(f"ERRO! Semestre de ingresso inválido: {e}")

    def _set_regression(self):
        regression = self._verify_regression()
        if regression == 1:
            self.campus_offers['Porcentagem total de desconto da bolsa\n(2º Semestre)'] = self.campus_offers['PORCENTAGEM_DESCONTO']

    def _adjusts_discounts(self):
        self._set_regression()
        self.campus_offers.rename(columns=self.columns_map,inplace=True)
        if 'Porcentagem total de desconto da bolsa\n(2º Semestre)' in self.campus_offers.columns:
            self.campus_offers.rename(columns={'DESCONTO_GARANTIDO':'Porcentagem total de desconto da bolsa\n(3º Semestre)'}, inplace=True)
            self.campus_offers['Porcentagem de desconto IES (1º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem de desconto da bolsa (Fixo/1 º Semestre)'])
            self.campus_offers['Porcentagem de desconto IES (2º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem total de desconto da bolsa\n(2º Semestre)'])
            self.campus_offers['Porcentagem de desconto IES (3º semestre)'] = self._generate_formatted_percentage_column(self.campus_offers['Porcentagem total de desconto da bolsa\n(3º Semestre)'])
        else:
            self.campus_offers.rename(columns={'DESCONTO_GARANTIDO':'Porcentagem total de desconto da bolsa\n(2º Semestre)'}, inplace=True)
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

    def _split_group_and_virtual(self):
        has_group = self.campus_offers['lookup_group'].notna()
        has_3719 = self.campus_offers['lookup_3719'].notna()
        self.offers_grupo = self.campus_offers[has_group].copy().reset_index(drop=True)
        self.offers_3719 = self.campus_offers[has_3719].copy().reset_index(drop=True)
        self.offers_grupo['COD CAMPUS'] = self.offers_grupo['lookup_group']
        self.offers_grupo['Nome do Campus'] = self.offers_grupo['campus_name_group']
        self.offers_3719['Avisos'] = self.offers_3719['Avisos'] + " | Certificado pela " + self.offers_3719['Nome da IES']
        self.offers_3719['ID da IES'] = '3719'
        self.offers_3719['Nome da IES'] = 'Cruzeiro Virtual'
        self.offers_3719['COD CAMPUS'] = self.offers_3719['lookup_3719']
        self.offers_3719['Nome do Campus'] = self.offers_3719['campus_name_3719']

    def _drop_extra_columns(self):
        cols_to_drop = ['COD_INST','NOM_FILI','CIDADE','ESTADO','lookup_group','lookup_3719','campus_name_group','campus_name_3719']
        existing_grupo = [c for c in cols_to_drop if c in self.offers_grupo.columns]
        existing_3719 = [c for c in cols_to_drop if c in self.offers_3719.columns]
        self.offers_grupo = self.offers_grupo.drop(columns=existing_grupo)
        self.offers_3719 = self.offers_3719.drop(columns=existing_3719)

    def _drop_unused_columns(self):
        empty_grupo = [col for col in self.offers_grupo.columns if self.offers_grupo[col].isna().all()]
        empty_3719 = [col for col in self.offers_3719.columns if self.offers_3719[col].isna().all()]
        self.offers_grupo = self.offers_grupo.drop(columns=empty_grupo)
        self.offers_3719 = self.offers_3719.drop(columns=empty_3719)

    def load(self):
        self._adjusts_discounts()
        self._fill_in_remaining_values()
        self._remaining_columns()
        self._split_group_and_virtual()
        self._drop_extra_columns()
        self._drop_unused_columns()
        return self.offers_grupo,self.offers_3719
