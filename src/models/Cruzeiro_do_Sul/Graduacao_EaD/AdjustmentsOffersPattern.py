from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
from datetime import date
import numpy as np


class AdjustmentsOffersPattern:
    def __init__(self,offers,offers_to_campus,enrollment_semester,end_date,special_condition):

        self.kinds_map = {
            'BACHARELADO': 'Bacharelado (graduação)',
            'TECNÓLOGO': 'Tecnólogo (graduação)',
            'LICENCIATURA': 'Licenciatura (graduação)',
            'BACH / LICENC': 'Bacharelado + Licenciatura (graduação)',
            'GRADUAÇÃO 2.0': 'Segunda graduação',
            'ABI': 'Bacharelado + Licenciatura (graduação)'
        }
        self.shift_map = {
            '100% EAD':	'EaD',
            'DIGITAL': 'EaD',
            'SEMIPRESENCIAL': 'Semipresencial',
            'AO VIVO': 'Ao vivo'
        }
        self.enrollment_semester = enrollment_semester
        self.end_date = end_date
        self.special_condition = special_condition
        self.offers = offers
        self.offers_to_campus = offers_to_campus

    def _adjusts_offers(self):
        self.offers_to_campus = self._multiples_xlookup(self.offers_to_campus, self.offers)
        self.offers_to_campus = self._columns_treatment(self.offers_to_campus)
        self.offers_to_campus['Semestre de Ingresso'] = self.enrollment_semester
        self.offers_to_campus['Turno'] = 'Virtual'
        self.offers_to_campus['Tipo de duração do curso'] = 'semestre'
        self.offers_to_campus['Qual valor usar?\n% ou R$'] = 'porcentagem'
        self.offers_to_campus['LIMITADA?'] = 'FALSE'
        self.offers_to_campus['Data de Fim da Oferta'] = self.end_date
        self.offers_to_campus['Benefício 1 (Chave OSC)'] = self.special_condition
        self.offers_to_campus.loc[:, 'Data de Início da Oferta'] = self.get_date_actually()

    def _remove_nan_offers(self):
        self.offers_to_campus['GRAU'] = (self.offers_to_campus['GRAU'].replace(['nan', 'NaN', 'None', 'NULL', 'null', ''], np.nan))
        self.offers_to_campus = dfu.drop_rows_have_nulls(self.offers_to_campus, 'GRAU')

    def _multiple_replaces(self, dataframe, header, values_dict: dict):
        normalized_map = {
            str(original_value).strip().upper(): new_value
            for original_value, new_value in values_dict.items()
        }
        dataframe[header] = dataframe[header].map(
            lambda value: normalized_map.get(str(value).strip().upper(), value)
        )
        return dataframe

    def _multiples_xlookup(self, dataframe_base, dataframe_search):
        dataframe = dataframe_base.copy()
        dataframe = dfu.normalize_lookup_columns(dataframe, ['COD_CURS', 'MATCH_KEY'])
        dataframe_search = dfu.normalize_lookup_columns(dataframe_search.copy(), ['Cód. Curso', 'MATCH_KEY'])

        lookup_columns = {
            'GRAU': 'GRAU',
            'Modalidade': 'METODOLOGIA',
            'Duração': 'DURAÇÃO',
            'Preço SIAA': 'PREÇO PARCELAS',
            'Porcentagem com Desconto 1° ano': 'PORCENTAGEM DE DESCONTO',
            'Desconto Garantido Demais Semestres': 'DESCONTO GARANTIDO',
            'Cód. IES': 'CÓDIGO DA IES',
            'Curso': 'CURSO',
            'Código SIAA': 'CÓDIGO SIAA',
            'Certificadora': 'CERTIFICADORA'
        }

        for source_column, target_column in lookup_columns.items():
            if source_column in dataframe_search.columns:
                dataframe = dfu.xlookup(
                    dataframe, dataframe_search, 'MATCH_KEY', 'MATCH_KEY',
                    source_column, target_column
                )
        return dataframe

    def get_date_actually(self):
        today = date.today()
        return today.strftime("%d/%m/%Y")

    def _columns_treatment(self, dataframe):
        dataframe = self._multiple_replaces(dataframe, 'GRAU', self.kinds_map)
        dataframe = self._multiple_replaces(dataframe, 'METODOLOGIA', self.shift_map)
        dataframe = dfu.replace_series(dataframe, 'DURAÇÃO', ' semestres', '')
        return dataframe

    def load(self):
        self._adjusts_offers()
        self._remove_nan_offers()
        return self.offers_to_campus
