from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
import openpyxl
import os
from datetime import date
class NormalizationGradEaD:
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
        self.campus_not_match,self.offers_not_match = pd.DataFrame(),pd.DataFrame()

    def _load_dataframes(self):
        self.offers = sma(self.offers).load()
        self.campus_offers = sma(self.campus_relation).load()
        self.campus = sma(self.campus).load()
        self.offers_mapping = sma(self.campus_relation,'de-para')
    
    def _separate_group(self):
        self.campus_virtual = dfu.filter_content_by_column(self.campus,"3719","university_id")
        self.campus_group = self.campus.copy()
        self.campus_group = dfu.remove_values_from_column(self.campus_group,"university_id",self.campus_virtual['university_id'])

    def _adjust_in_campus_offers(self):
        self.campus_offers = self._multiple_replaces(self.campus_offers,'NOM_FILI',self.name_ies_map)
        value_in_campus = list(self.offers_mapping['CAMPUS'])
        value_in_offers = list(self.offers_mapping['OFFERS'])
        offers_map = { 
            campi:offer for (campi,offer) in zip(value_in_campus,value_in_offers)
        } 
        self.campus_offers = self._multiple_replaces(self.campus_offers,'DES_CURS',offers_map)

    def _separate_campus_not_match(self):
        self.campus_offers['concat'] = dfu.concat_series_with_separator([self.campus_offers['ID_POLO'],self.campus_offers['NOME_POL'],self.campus_offers['NOM_FILI']],"-")
        self.campus_group['concat'] = dfu.concat_series_with_separator([self.campus_group['metadata_code'],self.campus_group['name_from_university'],self.campus_group['university_name']],"-")
        self.campus_offers = dfu.xlookup(self.campus_offers,self.campus_group,'concat','concat','id','matches_concat')
        if dfu.verify_if_have_nulls(self.campus_offers['matches_concat']):
            self.offers_not_match = dfu.get_rows_have_nulls(self.campus_offers,'matches_concat')
            self.campus_offers = dfu.drop_rows_have_nulls(self.campus_offers,'matches_concat')
            self.campus_not_match = self.offers_not_match.loc[:, ['ID_POLO', 'NOME_POL', 'NOM_FILI','concat']]
            self.campus_not_match = dfu.remove_duplicates_by_columns(self.campus_not_match,'concat')
            self.campus_not_match = self.campus_not_match.drop(columns= 'concat')

    def normalize_and_return(self):
        self._load_dataframes()
        self._separate_group()
        self._adjust_in_campus_offers()
        self._separate_campus_not_match()
        return self.campus_group,self.campus_virtual,self.campus_offers,self.offers_not_match,self.campus_not_match
    
    def _multiple_replaces(self,dataframe,header,values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe,header,original_value,new_value)
        return dataframe