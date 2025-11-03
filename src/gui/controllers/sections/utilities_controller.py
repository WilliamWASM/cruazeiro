from ....models.Utilities.exp_msp import *
from ....models.Utilities.duplicates import *
from ....models.Utilities.csv_converter import *
from ....models.Utilities.divisor import *

class UtilitiesController:
    def process_exp_msp(self,process_data:dict):
        paths = list(process_data["paths"].values())
        
        path = paths[0]

        exp_converter = MSPConverter(path)
        exp_converter.convert()

    def process_dup(self,process_data:dict):
        paths = list(process_data["paths"].values())
        
        path = paths[0]
        dup = RemoverDuplicadas(path)
        dup.execute()

    def process_csv_converter(self,process_data:dict):
        paths = list(process_data["paths"].values())
        
        path = paths[0]
        csv_converter = CSVConverter(path)
        csv_converter.converter_para_excel()
    
    def create_division(self,process_data:dict):
        paths = list(process_data["paths"].values())
        
        path = paths[0]
        save_path = process_data["save_path"]

        selected = process_data["selected_text"]
        div = TableDivisor(path,selected)
        div.create_files(save_path)
        
