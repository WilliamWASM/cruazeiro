from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from MODELS.campus.CampusMatchService import CampusMatchService as cms
from MODELS.campus.CampusUpdate import CampusUpdate as cupdate
import pandas as pd
class CampusVerifications:
    def __init__(self,exp_campus,msp_campus):
        self.exp = exp_campus
        self.msp = msp_campus
    
    def _load_dataframes(self):
        self.exp_verify = sma(self.exp).load()
        self.msp_campus = sma(self.msp).load()
        self.campus_update = pd.DataFrame()
        self.campus_create = pd.DataFrame()

    def _execute_all_verifications(self):
        match_service = cms(self.exp_verify,self.msp_campus,self.campus_update)
        self.campus_update,self.msp_campus = match_service.execute_verifications()
        if not self.campus_update.empty:
            updt_service = cupdate(self.campus_update,self.exp_verify)
            self.campus_update = updt_service.default_update_columns()
    
    def load(self,fullpath):
        self._load_dataframes()
        self._execute_all_verifications()
        if not self.msp_campus.empty:
            self.campus_create = self.msp_campus
        if not self.campus_update.empty and not self.campus_create.empty:
            dfu.save_multiple_dataframes([self.campus_create,self.campus_update],fullpath,['Campus para Criar','Campus para Atualizar'])
        elif not self.campus_update.empty and self.campus_create.empty:
            dfu.save_dataframe(self.campus_update,fullpath,'Campus para Atualizar')
        elif self.campus_update.empty and not self.campus_create.empty:
            dfu.save_dataframe(self.campus_create,fullpath,'Campus para Criar')
        elif self.campus_update.empty and self.campus_create.empty:
            raise ValueError('Não há campus para atualizar ou criar')
        