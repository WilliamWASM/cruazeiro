from ...excel_file.SheetManipulation import SheetManipulation as sma
from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
class InitialTreatments:
    def __init__(self,offers,campus_relation,exp_campus):
        self.offers = offers
        self.campus_relation = campus_relation
        self.campus = exp_campus
        self.name_ies_map = {
            'UNICID - GRADUAÇÃO EAD' : 'UNICID',
            'CRUZEIRO DO SUL - GRADUAÇÃO EAD' : 'UNICSUL - Cruzeiro do Sul',
            'UNIFRAN - GRADUAÇÃO EAD' : 'UNIFRAN',
            'FSG - GRADUAÇÃO EAD' : 'FSG',
            'UNIPÊ - GRADUAÇÃO EAD' : 'UNIPÊ',
            'BRAZ CUBAS - GRAD EAD' : 'Brazcubas',
            'POSITIVO - GRAD. EAD' : 'Universidade Positivo'
        }
        self.campus_offers_undefined = pd.DataFrame()
        self.not_totally_group = pd.DataFrame()
        self.not_totally_virtual = pd.DataFrame()

    def _load_dataframes(self):
        self.offers = sma(self.offers).load()
        self.offers_to_campus = sma(self.campus_relation).load()
        self.campus = sma(self.campus).load()

    def _unpivot_campus_relation(self):
        # Detecta dinamicamente as colunas CURSO_* da matriz pivotada
        curso_cols = [col for col in self.offers_to_campus.columns if col.startswith('CURSO_')]
        id_vars = ['ID_POLO', 'NOME_POL', 'NOM_FILI', 'COD_INST']
        self.offers_to_campus = self.offers_to_campus.melt(
            id_vars=id_vars,
            value_vars=curso_cols,
            var_name='CURSO_COL',
            value_name='PRESENTE'
        )
        # Mantém apenas linhas onde o polo tem o curso (marcado com X)
        self.offers_to_campus = self.offers_to_campus[self.offers_to_campus['PRESENTE'] == 'X'].copy()
        # Extrai o código numérico de CURSO_<COD> → COD_CURS como string
        self.offers_to_campus['COD_CURS'] = self.offers_to_campus['CURSO_COL'].str.replace('CURSO_', '', regex=False)
        self.offers_to_campus = self.offers_to_campus.drop(columns=['CURSO_COL', 'PRESENTE']).reset_index(drop=True)

    def _separate_group(self):
        self.campus_virtual = dfu.filter_content_by_column(self.campus, "3719", "university_id")
        self.campus_group = self.campus.copy()
        self.campus_group = dfu.remove_values_from_column(self.campus_group, "university_id", self.campus_virtual['university_id'])

    def _normalize_ies_names(self):
        # Normaliza NOM_FILI para bater com university_name no exp-campus
        self.offers_to_campus = self._multiple_replaces(self.offers_to_campus, 'NOM_FILI', self.name_ies_map)

    def _verify_offers_to_campus_not_match(self):
        # Verifica em campus_group E campus_virtual separadamente
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus, self.campus_group, 'ID_POLO', 'metadata_code', 'id', 'lookup_group')
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus, self.campus_virtual, 'ID_POLO', 'metadata_code', 'id', 'lookup_3719')
        # Mantém polo se encontrado em pelo menos um dos dois
        found_mask = self.offers_to_campus['lookup_group'].notna() | self.offers_to_campus['lookup_3719'].notna()
        self.campus_offers_undefined = self.offers_to_campus[~found_mask].copy()
        self.offers_to_campus = self.offers_to_campus[found_mask].reset_index(drop=True)

    def _verify_campus_totally_existence(self):
        # Polos apenas no virtual (sem campus no grupo) — sem ofertas de grupo
        self.not_totally_group = self.offers_to_campus[self.offers_to_campus['lookup_group'].isna()].copy()
        # Polos apenas no grupo (sem campus no 3719) — precisam ser criados no 3719
        self.not_totally_virtual = self.offers_to_campus[self.offers_to_campus['lookup_3719'].isna()].copy()

    def load(self):
        self._load_dataframes()
        self._unpivot_campus_relation()
        self._separate_group()
        self._normalize_ies_names()
        self._verify_offers_to_campus_not_match()
        self._verify_campus_totally_existence()
        return [self.offers, self.offers_to_campus, self.campus_group, self.campus_virtual,
                self.campus_offers_undefined, self.not_totally_group, self.not_totally_virtual]

    def _multiple_replaces(self, dataframe, header, values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe, header, original_value, new_value)
        return dataframe
