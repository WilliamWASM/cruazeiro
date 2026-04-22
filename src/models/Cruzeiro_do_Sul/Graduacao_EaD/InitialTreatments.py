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

    def _load_dataframes(self):
        self.offers = sma(self.offers).load()
        self.offers_to_campus = sma(self.campus_relation).load()
        self.campus = sma(self.campus).load()

    def _unpivot_campus_relation(self):
        curso_cols = [col for col in self.offers_to_campus.columns if str(col).strip().upper().startswith('CURSO_')]
        id_cols = [col for col in self.offers_to_campus.columns if not str(col).strip().upper().startswith('CURSO_')]
        self.offers_to_campus = self.offers_to_campus.melt(
            id_vars=id_cols,
            value_vars=curso_cols,
            var_name='CURSO_COL',
            value_name='OFERECE'
        )
        self.offers_to_campus = self.offers_to_campus[
            self.offers_to_campus['OFERECE'].astype(str).str.strip().str.upper() == 'X'
        ]
        self.offers_to_campus['COD_CURSO'] = self.offers_to_campus['CURSO_COL'].astype(str).str.strip().str.upper().str.replace('CURSO_', '', regex=False)
        self.offers_to_campus = self.offers_to_campus.drop(columns=['CURSO_COL', 'OFERECE'])
        self.offers_to_campus['COD_CURSO'] = self.offers_to_campus['COD_CURSO'].astype(str)
        self.offers_to_campus = self.offers_to_campus.reset_index(drop=True)

    def _separate_group(self):
        self.campus_virtual = dfu.filter_content_by_column(self.campus,"3719","university_id")
        self.campus_group = self.campus.copy()
        self.campus_group = dfu.remove_values_from_column(self.campus_group,"university_id",self.campus_virtual['university_id'])

    def _adjust_in_campus_offers(self):
        self.offers_to_campus = self._multiple_replaces(self.offers_to_campus,'NOM_FILI',self.name_ies_map)

    def _verify_campus_existence(self):
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus,self.campus_group,'ID_POLO','metadata_code','id','lookup_group')
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus,self.campus_group,'ID_POLO','metadata_code','name','campus_name_group')
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus,self.campus_virtual,'ID_POLO','metadata_code','id','lookup_3719')
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus,self.campus_virtual,'ID_POLO','metadata_code','name','campus_name_3719')
        has_group = self.offers_to_campus['lookup_group'].notna()
        has_3719 = self.offers_to_campus['lookup_3719'].notna()
        has_any = has_group | has_3719
        has_both = has_group & has_3719
        undefined = self.offers_to_campus[~has_both].copy().reset_index(drop=True)
        undefined_has_group = undefined['lookup_group'].notna()
        undefined_has_3719 = undefined['lookup_3719'].notna()
        undefined['Faltando Em'] = ''
        undefined.loc[~undefined_has_group & undefined_has_3719, 'Faltando Em'] = 'Grupo'
        undefined.loc[undefined_has_group & ~undefined_has_3719, 'Faltando Em'] = '3719'
        undefined.loc[~undefined_has_group & ~undefined_has_3719, 'Faltando Em'] = 'Grupo e 3719'
        self.campus_offers_undefined = undefined
        self.offers_to_campus = self.offers_to_campus[has_any].reset_index(drop=True)

    def load(self):
        self._load_dataframes()
        self._unpivot_campus_relation()
        self._separate_group()
        self._adjust_in_campus_offers()
        self._verify_campus_existence()
        return [self.offers,self.offers_to_campus,self.campus_group,self.campus_virtual,self.campus_offers_undefined]

    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe
