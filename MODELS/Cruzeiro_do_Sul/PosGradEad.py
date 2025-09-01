from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
import openpyxl
import os
from datetime import date
class PosGradEadCruzeiro:
    def __init__(self,offer_file,file_campus,file_ratio_campus):
        self.headers_transform = {
            "Nome da IES" : "CERTIFICADORA",  
            "Nome do Curso" : "CURSO",
            "Modalidade" : "METODOLOGIA",
            "Duração do Curso" : "DURAÇÃO (MESES)",
            "Quantidade de Parcelas" : "QUANTD PARCELAS",
            "Mensalidade sem desconto" : "PREÇO PARCELAS",
            "Porcentagem de desconto da bolsa (Fixo/1 º Semestre)" : "PORCENTAGEM DE DESCONTO"
        }   
        self.offers = offer_file
        self.campus = file_campus
        self.campus_ratio = file_ratio_campus

    def _load_dataframes(self):
        self.offers = sma(self.offers).convert_to_msp_offers_and_load(self.headers_transform)
        self.campus = sma(self.campus).load()
        self.pole_ratio_unp = sma(self.campus_ratio,"UNIPÊ").load()
        self.pole_ratio_pos = sma(self.campus_ratio,"POSITIVO").load()
        self.pole_ratio_unp['COD_POLO'] = self.pole_ratio_unp['COD_POLO'].astype(str)
        self.pole_ratio_pos['COD_POLO'] = self.pole_ratio_pos['COD_POLO'].astype(str)
        
    def _adjusts_in_msp(self):
        self.msp_columns_adjusts()
        self.separe_universities_courses()

    def _adjusts_in_campus(self):
        self.remove_campus_have_nulls()
        self.separate_campus()
        self.lookup_campus_ids()
        self.remove_campus_that_repeat()

    def _fill_campus_id_in_msps(self):
        self.concat_values_in_ratio_and_join()
        self.create_concat_campus()
        self.fill_in_campus_id_msp()
        self.concat_ies_offers()

    def msp_columns_adjusts(self):
        self.offers['Turno'] = "Virtual"
        self.offers['Tipo de duração do curso'] = "mes"
        self.offers['Grau'] = "Especialização (pós-graduação)"
        self.offers['Qual valor usar?\n% ou R$'] = "porcentagem"
        self.offers['LIMITADA?'] = "FALSE"
        self.offers.loc[:, 'Data de Início da Oferta'] = self.get_date_actually()
        self.offers['Porcentagem de desconto IES'] = self.transform_and_subtract_value(self.offers,'Porcentagem de desconto da bolsa (Fixo/1 º Semestre)')
        self.offers = dfu.find_and_replace(self.offers,'Nome da IES','CRUZEIRO DO SUL - PÓS EAD','ID da IES',3719)
        self.offers = dfu.find_and_replace(self.offers,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID da IES',1639)
        self.offers = dfu.find_and_replace(self.offers,'Nome da IES','UNIPÊ - PÓS-GRADUAÇÃO EAD','ID da IES',1593)

    def get_date_actually(self):
        today = date.today()
        return today.strftime("%d/%m/%Y")
    
    def transform_and_subtract_value(self, dataframe, column_name):
        new_column = dataframe[column_name].astype(float) - 0.05
        return new_column.round(2).astype(str)

    def separe_universities_courses(self):
        self.unipe = dfu.filter_content_by_column(self.offers,'UNIPÊ - PÓS-GRADUAÇÃO EAD','Nome da IES')
        self.positivo = dfu.filter_content_by_column(self.offers,'POSITIVO - PÓS-GRADUAÇÃO EAD','Nome da IES')
        self.cruzeiro = dfu.filter_content_by_column(self.offers,'CRUZEIRO DO SUL - PÓS EAD','Nome da IES')

    def remove_campus_have_nulls(self):
        if dfu.verify_if_have_nulls(self.campus['metadata_code']):
            self.pending_campus = dfu.get_rows_have_nulls(self.campus,'metadata_code')
            self.campus = dfu.dropna_rows_by_column(self.campus,'metadata_code')
        
    def separate_campus(self):
        self.exp_unp = dfu.filter_content_by_column(self.campus,"1593","university_id")
        self.exp_pos = dfu.filter_content_by_column(self.campus,"1639","university_id")
        self.exp_cruzeiro = dfu.filter_content_by_column(self.campus,"3719","university_id")
    
    def lookup_campus_ids(self):
        self.pole_ratio_unp = dfu.xlookup(self.pole_ratio_unp,self.exp_unp,'COD_POLO','metadata_code','id','campus_id')
        self.pole_ratio_pos = dfu.xlookup(self.pole_ratio_pos,self.exp_pos,'COD_POLO','metadata_code','id','campus_id')
        if dfu.verify_if_have_nulls(self.pole_ratio_unp['campus_id']):
            self.pending_unp = dfu.get_rows_have_nulls(self.pole_ratio_unp,'campus_id')
            self.pole_ratio_unp = dfu.dropna_rows_by_column(self.pole_ratio_unp,'campus_id')
        if dfu.verify_if_have_nulls(self.pole_ratio_pos['campus_id']):
            self.pending_pos = dfu.get_rows_have_nulls(self.pole_ratio_pos,'campus_id')
            self.pole_ratio_pos = dfu.dropna_rows_by_column(self.pole_ratio_pos,'campus_id')
            self.campus_ratio_pending = dfu.concat_dataframes(self.pending_pos,self.pending_unp)

    def remove_campus_that_repeat(self):
        self.exp_cruzeiro = dfu.remove_values_from_column(self.exp_cruzeiro,'metadata_code',self.pole_ratio_pos['COD_POLO'])
        self.exp_cruzeiro = dfu.remove_values_from_column(self.exp_cruzeiro,'metadata_code',self.pole_ratio_unp['COD_POLO'])

    def concat_values_in_ratio_and_join(self):
        self.pole_ratio_unp['concat'] = dfu.concat_series_with_separator([self.pole_ratio_unp['campus_id'],self.pole_ratio_unp['COD_POLO']],';campus_code:')
        self.pole_ratio_pos['concat'] = dfu.concat_series_with_separator([self.pole_ratio_pos['campus_id'],self.pole_ratio_pos['COD_POLO']],';campus_code:')
        self.join_unp = dfu.textjoin_unique(self.pole_ratio_unp['concat'])
        self.join_pos = dfu.textjoin_unique(self.pole_ratio_pos['concat'])

    def create_concat_campus(self):
        keys = dfu.concat_series_with_separator([self.exp_cruzeiro['id'],self.exp_cruzeiro['metadata_code']],';campus_code:')
        keys_count = keys.str.len()
        limit_cells = 32767
        sum_cells = 0
        self.groups = []
        init = 0
        for row in range(len(keys)):
            current_length = keys_count.iloc[row] + 1
            sum_cells += current_length
            if limit_cells < sum_cells:
                result = dfu.textjoin_unique(keys.iloc[init:row])
                self.groups.append(result)
                init = row
                sum_cells = keys_count.iloc[row] 
        if init < len(keys):
            result = dfu.textjoin_unique(keys.iloc[init:])
            self.groups.append(result)

    def fill_in_campus_id_msp(self):
        self.unipe = dfu.find_and_replace(self.unipe,'Nome da IES','UNIPÊ - PÓS-GRADUAÇÃO EAD','ID do Campus',self.join_unp)
        if len(self.pole_ratio_pos) == 1:
            self.campus_pos = self.pole_ratio_pos['campus_id'][0]   
            self.positivo = dfu.find_and_replace(self.positivo,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','COD CAMPUS',self.join_pos)
            self.positivo = dfu.find_and_replace(self.positivo,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID do Campus',self.campus_pos)
        else:
            self.positivo = dfu.find_and_replace(self.positivo,'Nome da IES','POSITIVO - PÓS-GRADUAÇÃO EAD','ID do Campus',self.join_pos)
    
    def concat_ies_offers(self):
        self.msp = dfu.concat_dataframes(self.positivo,self.unipe)

    def create_files_and_save(self,file_save):
        range_for = len(self.groups)
        for i in range(range_for):
            self.df_temp = dfu.find_and_replace(self.cruzeiro,'Nome da IES','CRUZEIRO DO SUL - PÓS EAD',"ID do Campus",self.groups[i])
            dfu.save_dataframe(self.df_temp,os.path.join(file_save,f"CRUZEIRO_POS_GRAD{i}.xlsx"),'Modelo Sem Parar')
        dfu.save_dataframe(self.msp,os.path.join(file_save, "UNIPE_E_POSITIVO.xlsx"),'Modelo Sem Parar')

    def load(self):  
        try:
            self._load_dataframes()
            self._adjusts_in_msp()
            self._adjusts_in_campus()
            self._fill_campus_id_in_msps()     
        except Exception as e:
            print (f"Erro durante o processamento: {e}")

    def set_values_missing_in_msp(self,end_date,osc,admission_semester):
        self.cruzeiro['Data de Fim da Oferta'] = end_date
        self.msp['Data de Fim da Oferta'] = end_date
        self.cruzeiro['Benefício 1 (Chave OSC)'] = osc
        self.msp['Benefício 1 (Chave OSC)'] = osc
        self.cruzeiro['Semestre de Ingresso'] = admission_semester
        self.msp['Semestre de Ingresso'] = admission_semester

    def save(self,path_save):
        try:
            self.create_files_and_save(path_save)
        except Exception as e:
            print (f"Erro durante o salvamento dos arquivos: {e}")