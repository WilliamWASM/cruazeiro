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
        self.campus_offers_undefined,self.not_totally_group,self.not_totally_virtual = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()

    def _load_dataframes(self):
        self.offers = sma(self.offers).load()
        self.offers_to_campus = sma(self.campus_relation).load()
        self.campus = sma(self.campus).load()
        self.offers_mapping = sma(self.campus_relation,'de-para').load()

    def _drop_excessive_columns(self):
        self.offers_to_campus = self.offers_to_campus.drop(columns=['CIDADE','ESTADO','TIPO_POLO','SIT_POLO','METODOLOGIA','SITUACAO_CURSO','COD_EMEC','COD_SENSO_POLO','ID_POLO NOVO',
                                                                    'COD_EMPR','NM_FANTA'])
    
    def _separate_group(self):
        self.campus_virtual = dfu.filter_content_by_column(self.campus,"3719","university_id")
        self.campus_group = self.campus.copy()
        self.campus_group = dfu.remove_values_from_column(self.campus_group,"university_id",self.campus_virtual['university_id'])

    def _adjust_in_campus_offers(self):
        self.offers_to_campus = self._multiple_replaces(self.offers_to_campus,'NOM_FILI',self.name_ies_map)
        value_in_campus = list(self.offers_mapping['CAMPUS'])
        value_in_offers = list(self.offers_mapping['OFFERS'])
        offers_map = { 
            campi:offer for (campi,offer) in zip(value_in_campus,value_in_offers)
        } 
        self.offers_to_campus = self._multiple_replaces(self.offers_to_campus,'DES_CURS',offers_map)
    
    def _verify_offers_to_campus_not_match(self):
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus,self.campus_group,'ID_POLO','metadata_code','id','matches_concat')
        if dfu.verify_if_have_nulls(self.offers_to_campus['matches_concat']):
            self.campus_offers_undefined = dfu.get_rows_have_nulls(self.offers_to_campus,'matches_concat')
            self.offers_to_campus = dfu.drop_rows_have_nulls(self.offers_to_campus,'matches_concat')
            self.campus_offers_undefined = dfu.xlookup(self.campus_offers_undefined,self.campus_group,'ID_POLO_HUB','metadata_code','id','matches_concat')
            if dfu.verify_if_have_nulls(self.campus_offers_undefined['matches_concat']):
                not_sec_match = dfu.get_rows_have_nulls(self.campus_offers_undefined,'matches_concat')
                self.campus_offers_undefined = dfu.drop_rows_have_nulls(self.campus_offers_undefined,'matches_concat')
                self.offers_to_campus = dfu.concat_dataframes(self.offers_to_campus,self.campus_offers_undefined)
                self.campus_offers_undefined = not_sec_match
            
    def _verify_campus_totally_existence(self):
        self.offers_to_campus =  dfu.xlookup(self.offers_to_campus,self.campus_group,'ID_POLO','metadata_code','id','lookup_group')
        self.offers_to_campus =  dfu.xlookup(self.offers_to_campus,self.campus_virtual,'ID_POLO','metadata_code','id','lookup_3719')
        if dfu.verify_if_have_nulls(self.offers_to_campus['lookup_group']):
            self.not_totally_group = dfu.get_rows_have_nulls(self.offers_to_campus,'lookup_group')
            self.offers_to_campus = dfu.drop_rows_have_nulls(self.offers_to_campus,'lookup_group')
        if dfu.verify_if_have_nulls(self.offers_to_campus['lookup_3719']):
            self.not_totally_virtual = dfu.get_rows_have_nulls(self.offers_to_campus,'lookup_group')
            self.offers_to_campus = dfu.drop_rows_have_nulls(self.offers_to_campus,'lookup_group')

    def load(self):
        self._load_dataframes()
        self._drop_excessive_columns()
        self._separate_group()
        self._adjust_in_campus_offers()
        self._verify_offers_to_campus_not_match()
        self._verify_campus_totally_existence()
        return [self.offers,self.offers_to_campus,self.campus_group,self.campus_virtual,self.campus_offers_undefined,self.not_totally_group,self.not_totally_virtual]
        
    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe
    