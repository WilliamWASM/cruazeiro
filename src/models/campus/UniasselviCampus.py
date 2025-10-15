from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from MODELS.campus.CampusMatchService import CampusMatchService as cms
from MODELS.campus.CampusUpdate import CampusUpdate as cupdate
from MODELS.campus.CampusVerifications import CampusVerifications as cvs
import pandas as pd
class UniasselviCampus:
    def __init__(self,exp_campus,campus,type_verification = 'EAD'):

        self.EAD_HEADERS_MAP = {
        'Código_Polo':'metadata_code',
        'Polo':'name_from_university',
        'Rua':'address',
        'Número':'address_number',
        'Complemento':'address_adjunct',
        'Bairro':'neighborhood',
        'CEP':'zipcode',
        'Cidade':'city',
        'Estado':'state'
        }  
        self.PRESENCIAL_HEADERS_MAP = {
        'CODIGO SEDE GIOCONDA':'metadata_code',
        'FONE':'phone',
        'ENDEREÇO':'address',
        'NUMERO':'address_number',
        'COMPLEMENTO':'address_adjunct',
        'BAIRRO':'neighborhood',
        'CEP':'zipcode',
        'CIDADE':'city',
        'UF':'state'
        }
        self.exp_verify = exp_campus
        self.campus_verify = campus
        self.type_verification = type_verification
        
    def _load_df(self):
        if self.type_verification == 'PRESENCIAL':
            self.campus_verify = sma(self.campus_verify,"ENDEREÇO_PRESENCIAL").load()
        elif self.type_verification == 'EAD':
            self.campus_verify = sma(self.campus_verify,"ENDEREÇO_EAD").load()
        else:
            raise ValueError("Tipo de verificação inválido. Use 'EAD' ou 'PRESENCIAL'.")
        
    def rename_headers_and_set_dtype(self):
        if self.type_verification == 'PRESENCIAL':
            self.campus_verify.rename(columns=self.PRESENCIAL_HEADERS_MAP,inplace=True)
        elif self.type_verification == 'EAD':
            self.campus_verify.rename(columns=self.EAD_HEADERS_MAP,inplace=True)
        else:
            raise ValueError("Tipo de verificação inválido. Use 'EAD' ou 'PRESENCIAL'.")
        
    def load(self,fullpath):
        self._load_df()
        self.rename_headers_and_set_dtype()
        cvs(self.exp_verify,self.campus_verify).load_have_campus_df(fullpath)
        

    




    


    

