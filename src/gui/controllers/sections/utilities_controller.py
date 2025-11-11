from ....models.Utilities.exp_msp import *
from ....models.Utilities.duplicates import *
from ....models.Utilities.csv_converter import *
from ....models.Utilities.divisor import *
from ....models.Utilities.university_offer import *

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

        number_of_divisions = process_data["selected_value"]
        number_of_divisions = int(number_of_divisions)
        div = TableDivisor(path,number_of_divisions)
        div.create_files(save_path)

    def process_dup_univ_offer(self,process_data:dict):
        paths = list(process_data["paths"].values())
        
        path = paths[0]
        dup = RemoverUniversityOfferDuplicates(path)
        dup.execute()
        
