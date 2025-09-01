import pandas as pd
import openpyxl
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu

class tecnicoCruzeiro:
    def __init__(self,file_offers,file_campus):
        self.file_msp = file_offers
        self.file_campus = file_campus
        self.nursing_pending,self.pendings_courses,self.pending_msp = None,None,None

    def _load_dataframes(self):
        self.msp_offers = sma(self.file_msp,"Modelo Sem Parar").load()
        self.port_tec = sma(self.file_msp,"Polo X Portfólio Técnico").load()
        self.tec_nursing = sma(self.file_msp,"Polo X Portfólio Tec Enfermagem").load()
        self.exp_campus = sma(self.file_campus).load()

    def _adjusts_in_tecnico_sheet(self):
        self._treatment_name_ies_in_msp()
        self._create_search_columns()
        self._fill_in_campus_id_and_remove_nas()
        self._names_treatment()
        self._create_concat_in_tec_courses()
        self._concat_ids()
        self.concat_and_join_nursing_courses()
        self._create_list_of_ids_by_course()

    def _separate_campus(self):
        self.campus_brazcubas = dfu.filter_content_by_column(self.exp_campus,"Brazcubas","university_name")

    def _treatment_name_ies_in_msp(self):
        self.port_tec = self._multiples_replaces_in_dataframe(self.port_tec,'NOM_FILI',{"BRAZ CUBAS - TECNICO EAD":"BRAZ CUBAS","CRUZEIRO DO SUL - TECNICO EAD":"CRUZEIRO"})

    def _create_search_columns(self):
        self.port_tec = dfu.xlookup(self.port_tec,self.msp_offers,'NOM_FILI','Nome da IES','ID da IES','university_id')
        self.port_tec = self._multiples_concats_in_dataframe(self.port_tec,{'concat': ['university_id','ID_POLO'],'concat2': ['university_id','NOME_POL']})
        self.exp_campus = self._multiples_concats_in_dataframe(self.exp_campus,{'concat': ['university_id','metadata_code'],'concat2': ['university_id','name_from_university']})
        
    def _fill_in_campus_id_and_remove_nas(self):
        self.port_tec = dfu.xlookup(self.port_tec,self.exp_campus,'concat','concat','id','campus_id')
        campus_id = None
        if dfu.verify_if_have_nulls(self.port_tec['campus_id']):
            campus_id_na = dfu.get_rows_have_nulls(self.port_tec,'campus_id')
            self.port_tec = dfu.dropna_rows_by_column(self.port_tec,'campus_id')
            campus_id = dfu.xlookup(campus_id_na,self.exp_campus,'concat2','concat2','id','campus_id')
            if dfu.verify_if_have_nulls(campus_id['campus_id']):
                self.pendings_courses = dfu.get_rows_have_nulls(campus_id,'campus_id')
                campus_id = dfu.dropna_rows_by_column(campus_id,'campus_id')
        self.port_tec = dfu.concat_dataframes(self.port_tec,campus_id)

    def _names_treatment(self):
        self.port_tec = self._multiples_replaces_in_dataframe(self.port_tec,'DES_CURS',{" ":"",".":""})
        self.msp_offers['cursos'] = self.msp_offers['Nome do Curso']
        self.msp_offers = dfu.replace_series(self.msp_offers,'cursos'," ","")
        self.msp_offers = dfu.replace_series(self.msp_offers,'Semestre de Ingresso',",",".")

    def _create_concat_in_tec_courses(self):
        self.port_tec['concat_cursos'] = dfu.concat_series_with_separator([self.port_tec['campus_id'],self.port_tec['DES_CURS']], "-")
        self.port_tec = dfu.remove_duplicates_by_columns(self.port_tec,'concat_cursos')

    def _concat_ids(self):
        self.port_tec['ids_concatenados'] = dfu.concat_series_with_separator([self.port_tec['campus_id'],self.port_tec['ID_POLO']], ";campus_code:")

    def _create_list_of_ids_by_course(self):
        self.msp_offers['ID do Campus'] = [
            self.join_nursing if curso == 'TÉCNICOEMENFERMAGEM'
            else (
                result if (result := dfu.textjoin_unique(
                    self.port_tec.loc[(self.port_tec['university_id'] == uni_id) & (self.port_tec['DES_CURS'] == curso), 'ids_concatenados'
                    ]   
                )) else None
            )
            for uni_id, curso in zip(self.msp_offers['ID da IES'], self.msp_offers['cursos'])
        ]
        if self.msp_offers['ID do Campus'].isna().any():
            self.pending_msp = dfu.get_rows_have_nulls(self.msp_offers,'ID do Campus')
            self.msp_offers = dfu.dropna_rows_by_column(self.msp_offers,'ID do Campus')

    def _nursing_treatment(self):
        self._separate_campus()
        self.check_nas_in_nursing_courses()

    def check_nas_in_nursing_courses(self):
        self.tec_nursing['ID_POLO'] = self.tec_nursing['ID_POLO'].astype(str)
        self.tec_nursing = dfu.xlookup(self.tec_nursing,self.campus_brazcubas,'ID_POLO','metadata_code','id','campus_id')
        if dfu.verify_if_have_nulls(self.tec_nursing['campus_id']):
            self.nursing_pending = dfu.get_rows_have_nulls(self.tec_nursing,'campus_id')
            self.tec_nursing = dfu.dropna_rows_by_column(self.tec_nursing,'campus_id')

    def concat_and_join_nursing_courses(self):
        self.tec_nursing['concat'] = dfu.concat_series_with_separator([self.tec_nursing['campus_id'],self.tec_nursing['ID_POLO']],";campus_code:")
        self.join_nursing = dfu.textjoin_unique(self.tec_nursing['concat'])

    def load(self,path):
        try:
            self._load_dataframes()
            self._nursing_treatment()
            self._adjusts_in_tecnico_sheet()
            self._saving_and_separing_pendings(path)
        except Exception as e:
            print (f"Erro durante o processamento: {e}")

    def _saving_and_separing_pendings(self,path):
        dfu.save_multiple_dataframes([self.msp_offers,self.pendings_courses,self.nursing_pending,self.pending_msp],path,['Modelo Sem Parar','Pendencias portfolio','Pendencias enfermagem','Pendencias MSP'])

    def _multiples_concats_in_dataframe(self,dataframe,columns_to_concat : dict,separator = ","):
        for key, column in columns_to_concat.items():
            dataframe[key] = dfu.concat_series_with_separator([dataframe[item] for 
                                                               item in column],separator)
        return dataframe   
        
    def _multiples_replaces_in_dataframe(self,dataframe,column_replace,values_and_substitute : dict):
        for origin_value,new_value in values_and_substitute.items():
            dataframe = dfu.replace_series(dataframe,column_replace,origin_value,new_value)
        return dataframe
    
