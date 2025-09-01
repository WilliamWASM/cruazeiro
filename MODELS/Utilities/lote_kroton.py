import pandas as pd
import os
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from GUI.widgets.notifications import Notification 

class KrotonLote:
    def __init__(self, exp_file, path_save):
        self.tec_courses = None
        self.save_path = path_save
        self.exp_file = exp_file
        self.sheet = sma(self.exp_file)
        self.dataframe = self.sheet.load()
        
        # self.file = path
        # self.sheet = sma(self.file)          # Crie o objeto SheetManipulation
        # self.dataframe = self.sheet.load()   # Carregue o dataframe

# Criar a coluna SKU na posição C (índice 2) - 
    def concat_sku_and_drop_duplicates(self):
        self.dataframe['sku'] = dfu.concat_series_with_separator([
            self.dataframe['IES'],
            self.dataframe['COD_UNIDADE'],
            self.dataframe['CURSO'],
            self.dataframe['MODALIDADE'],
            self.dataframe['TURNO'],
            self.dataframe['GRAU'],
            self.dataframe['QTDE PERIODOS'],
            self.dataframe['PRECO BRUTO']
           ], "-"
        )
        self.dataframe = dfu.remove_duplicates_by_columns(self.dataframe, 'sku')
   
# Excluir e add colunas SOURCE e METADATA
    def drop_column_and_create_corrects(self):
        self.dataframe = dfu.delete_series(self.dataframe,'SOURCE ')
        self.dataframe ['SOURCE'] = 'table'
        self.dataframe ['METADATA'] = 'external_id:0'
    
    def separate_courses(self):
        self.tec_courses = dfu.filter_content_by_column(self.dataframe,'TÉCNICO', 'GRAU')
        self.dataframe = dfu.remove_values_from_column(self.dataframe, 'GRAU', self.tec_courses['GRAU'])
    
    def load(self):
        self.concat_sku_and_drop_duplicates()
        self.drop_column_and_create_corrects()
        self.separate_courses()
        
        try:
            dfu.save_multiple_dataframes([self.dataframe, self.tec_courses], self.save_path, ['graduação', 'técnico'])
        except Exception as e:
            Notification.error("Error ao Salvar",f"Erro ao salvar o arquivo Excel: {e}")
    



 