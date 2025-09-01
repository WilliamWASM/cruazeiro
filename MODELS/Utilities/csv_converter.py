import os
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from GUI.widgets.notifications import Notification 

class CSVConverter:
    def __init__(self, csv_file: str):
        self.df_csv = sma(csv_file).load()
        base_name = os.path.basename(csv_file)
        dir_name = os.path.dirname(csv_file) 
        new_name = "xlsx_" + base_name.replace(".csv", ".xlsx")
        self.excel_file = os.path.join(dir_name, new_name)
    
    def converter_para_excel(self):
        self.df_csv.to_excel(self.excel_file, index=False)
        Notification.info("Arquivo Salvo",f"📁 Arquivo Excel salvo: {self.excel_file}")
