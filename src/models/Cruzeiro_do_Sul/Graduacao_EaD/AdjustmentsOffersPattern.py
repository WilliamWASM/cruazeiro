from ...excel_file.SheetManipulation import SheetManipulation as sma
from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
from datetime import date
import numpy as np
class AdjustmentsOffersPattern:
    def __init__(self,offers,offers_to_campus,enrollment_semester,end_date,special_condition):

        self.kinds_map = {
            'BACHARELADO': 'Bacharelado (graduação)',
            'TECNÓLOGO': 'Tecnólogo (graduação)',
            'LICENCIATURA': 'Licenciatura (graduação)',
            'BACH / LICENC': 'Bacharelado + Licenciatura (graduação)'
        }
        self.shift_map = {
            '100% EAD':	'EaD',
            'SEMIPRESENCIAL': 'Semipresencial',
            'AO VIVO': 'Ao vivo',
            'Digital': 'EaD'
        }
        self.name_ies_map = {
            'Unicid - Graduação Ead': 'UNICID',
            'Cruzeiro - Graduação Ead': 'UNICSUL - Cruzeiro do Sul',
            'Unifran - Graduação Ead': 'UNIFRAN',
            'Fsg - Graduação Ead': 'FSG',
            'Unipê - Graduação Ead': 'UNIPÊ',
            'Braz Cubas - Graduação Ead': 'Brazcubas',
            'Positivo - Graduação Ead': 'Universidade Positivo'
        }
        self.enrollment_semester = enrollment_semester
        self.end_date = end_date
        self.special_condition = special_condition
        self.offers = offers
        self.offers_to_campus = offers_to_campus

    def _adjusts_offers(self):
        self.offers_to_campus = self._multiples_xlookup(self.offers_to_campus,self.offers)
        self.offers_to_campus = self._columns_treatment(self.offers_to_campus)
        self.offers_to_campus['Semestre de Ingresso'] = self.enrollment_semester
        self.offers_to_campus['Turno'] = 'Virtual'
        self.offers_to_campus['Tipo de duração do curso'] = 'semestre'
        self.offers_to_campus['Qual valor usar?\n% ou R$'] = 'porcentagem'
        self.offers_to_campus['LIMITADA?'] = 'FALSE'
        self.offers_to_campus['Data de Fim da Oferta'] = self.end_date
        oscs = str(self.special_condition).split('|')
        self.offers_to_campus['Benefício 1 (Chave OSC)'] = oscs[0].strip()
        self.offers_to_campus['Benefício 2 (Chave OSC)'] = oscs[1].strip() if len(oscs) > 1 else None
        self.offers_to_campus['Data de Início da Oferta'] = self.get_date_actually()

    def _remove_nan_offers(self):
        self.offers_to_campus['GRAU'] = (self.offers_to_campus['GRAU'].replace(['nan', 'NaN', 'None', 'NULL', 'null', ''], np.nan))
        self.offers_to_campus = dfu.drop_rows_have_nulls(self.offers_to_campus,'GRAU')

    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe

    def _multiples_xlookup(self,dataframe_base,dataframe_search):
        dataframe_base['COD_CURSO'] = dataframe_base['COD_CURSO'].astype(str).str.upper().str.replace(r'\.0$', '', regex=True).str.strip().apply(lambda x: x.lstrip('0') if x != '0' else x)
        dataframe_search['Cód. Curso'] = dataframe_search['Cód. Curso'].astype(str).str.upper().str.replace(r'\.0$', '', regex=True).str.strip().apply(lambda x: x.lstrip('0') if x != '0' else x)
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','GRAU','GRAU')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Modalidade','MODALIDADE')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Duração','DURACAO')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Preço SIAA','PRECO_PARCELAS')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Porcentagem com Desconto 1° ano','PORCENTAGEM_DESCONTO')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Desconto Garantido Demais Semestres','DESCONTO_GARANTIDO')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Cód. IES','COD_IES')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Curso','CURSO')
        dataframe = dfu.xlookup(dataframe_base,dataframe_search,'COD_CURSO','Cód. Curso','Certificadora','CERTIFICADORA')
        return dataframe

    def get_date_actually(self):
        today = date.today()
        return today.strftime("%d/%m/%Y")

    def _columns_treatment(self,dataframe):
        dataframe = self._multiple_replaces(dataframe,'GRAU',self.kinds_map)
        dataframe = self._multiple_replaces(dataframe,'MODALIDADE',self.shift_map)
        dataframe = self._multiple_replaces(dataframe,'CERTIFICADORA',self.name_ies_map)
        dataframe = dfu.replace_series(dataframe,'DURACAO',' semestres','')
        return dataframe

    def load(self):
        self._adjusts_offers()
        self._remove_nan_offers()
        return self.offers_to_campus
