from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
class CampusMatchService:
    def __init__(self,exp_verify,msp_campus,df_update):
        self.msp_campus = msp_campus
        self.exp_verify = exp_verify
        self.campus_update = df_update

    def execute_verifications(self):
        self._init_treatments()
        if self._verify_metadata_exists():
            self._metadata_verifications()
        elif not self.msp_campus.empty and self._verify_name_ies_exists():
            self._name_verifications()
        elif not self.msp_campus.empty and self._sku_exists():
            self._sku_verifications()
        return self.campus_update,self.msp_campus
    
    def _metadata_verifications(self):
        self._verify_from_('metadata_code')
        self._return_metadata_unique()
        if not self.msp_campus.empty and self._verify_name_ies_exists():
            self._name_verifications()
            if not self.msp_campus.empty and self._sku_exists():
                self._sku_verifications()

    def _name_verifications(self):
        if 'name' in self.msp_campus.columns:
                self._verify_from_('name')
        elif 'name_from_university' in self.msp_campus.columns:
            self._verify_from_('name_from_university')
        if not self.msp_campus.empty and self._sku_exists():
            self._sku_verifications()

    def _sku_verifications(self):
        self.msp_campus = self._sku_generate(self.msp_campus)
        self.exp_verify = self._sku_generate(self.exp_verify)
        self._verify_from_('concat1')


    def _sku_exists(self):
        required = {'address_number', 'zipcode', 'virtual', 'university_id'}
        return required.issubset(self.msp_campus.columns)
    
    def _separate_have_id(self):
        if 'id' in self.msp_campus.columns:
            if not self.msp_campus['id'].isnull().any():
                self.campus_update = dfu.concat_dataframes(self.campus_update,self.msp_campus)
                self.msp_campus = pd.DataFrame()
            elif not self.msp_campus['id'].isnull().all():
                id_nulls = dfu.get_rows_have_nulls(self.msp_campus,'id')
                ids_have_value = dfu.drop_rows_have_nulls(self.msp_campus, 'id')
                self.campus_update = dfu.concat_dataframes(self.campus_update,ids_have_value)
                self.msp_campus = dfu.filter_content_by_column(id_nulls,id_nulls,'id')
            
    
    def _init_treatments(self):
        self._separate_have_id()
        self._lower_all_columns_have_string()
        self._slug_treatment()
        if self._verify_metadata_exists():
            self._metadata_treatment()

    def _slug_treatment(self):
        self.exp_verify['name'] = self.exp_verify['name'].str.replace(r'[^\w\s]|_', '', regex=True)
        if not self.msp_campus.empty and 'name' in self.msp_campus.columns:
            self.msp_campus['name'] = self.msp_campus['name'].str.replace(r'[^\w\s]|_', '', regex=True)

    def _lower_all_columns_have_string(self):
            cols = ['name','name_from_university','address','address_adjunct','neighborhood','city']
            cols_in_msp = [col for col in cols if col in self.msp_campus.columns]
            cols_in_exp = [col for col in cols if col in self.exp_verify.columns]
            for col in cols_in_exp:
                self.exp_verify[col] = self.exp_verify[col].fillna('').astype(str).str.lower().str.replace(r'\s+', ' ', regex=True).str.strip()
            for col in cols_in_msp:
                self.msp_campus[col] = self.msp_campus[col].fillna('').astype(str).str.lower().str.replace(r'\s+', ' ', regex=True).str.strip()
    
    def _verify_metadata_exists(self):
        if 'metadata_code' in self.msp_campus.columns:
            if not self.msp_campus['metadata_code'].isnull().all():
                return True
            else:
                return False
    def _verify_name_ies_exists(self):
        if 'name' or 'name_from_university' in self.msp_campus.columns:
            return True
        else:
            return False
        
    def _metadata_treatment(self):
            self.exp_verify['metadata_code'] = self.exp_verify['metadata_code'].astype(str).str.split("#")
            self.exp_verify = self.exp_verify.explode("metadata_code",ignore_index= True)
            self.exp_verify['metadata_code'] = self.exp_verify['metadata_code'].replace('nan', '').fillna('')

    def _verify_from_(self,column_search):
        campus_verif = dfu.xlookup(self.msp_campus,self.exp_verify,column_search,column_search,'id','id')
        if dfu.verify_if_have_nulls(campus_verif['id']):
            create_by = dfu.get_rows_have_nulls(campus_verif,'id')
            campus_verif = dfu.drop_rows_have_nulls(campus_verif,'id')
            self.campus_update = dfu.concat_dataframes(self.campus_update,campus_verif )
            self.msp_campus = create_by
        else:
            self.campus_update = dfu.concat_dataframes(self.campus_update,campus_verif)
            self.msp_campus = pd.DataFrame()

    def _return_metadata_unique(self):
        dup_ids_exp = self.exp_verify[self.exp_verify.duplicated(subset=['id'], keep=False)]
        if not dup_ids_exp.empty:
            mask_in_update = self.exp_verify['metadata_code'].isin(self.campus_update['metadata_code'])
            if mask_in_update.any():
                self.exp_verify = self.exp_verify[~mask_in_update].reset_index(drop=True)
        self.exp_verify = dfu.remove_duplicates_by_columns(self.exp_verify, 'id')

    def _sku_generate(self,dataframe):
        dataframe = dataframe.assign(
                concat1 = dfu.concat_series_with_separator(
                    [
                        dataframe['university_id'],
                        dataframe['address_number'],
                        dataframe['zipcode'],
                        dataframe['virtual']
                    ], 
                    ","
                )
            )
        return dataframe