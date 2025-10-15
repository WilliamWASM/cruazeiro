import os
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from GUI.widgets.notifications import Notification

class TableDivisor:
    def __init__(self,excel_file,quantity_divisions):
        self.excel_file = excel_file
        self.sheet = sma(self.excel_file)
        self.table = self.sheet.load()
        self.quantity_divisions = int(quantity_divisions)
        self.calc_quantity_rows()

    def calc_quantity_rows(self):
        total_rows = self.table.iloc[:, 1].last_valid_index() + 1
        self.rows_for_division = total_rows // self.quantity_divisions

    def create_files(self,path):
        name_file = os.path.splitext(os.path.basename(self.excel_file))[0]
        for i in range(1,self.quantity_divisions):
            df_temp = dfu.get_rows_by_index(self.table,range(0,self.rows_for_division))
            dfu.save_dataframe(df_temp, os.path.join(path, f"{name_file}{i}.xlsx"), "Sheet 1") #save_dataframe
            self.table = dfu.drop_rows(self.table,range(0,self.rows_for_division)) #drop_rows
        dfu.save_dataframe(self.table, os.path.join(path, f"{name_file}{self.quantity_divisions}.xlsx"), "Sheet 1")
        Notification.info("Arquivo Salvo",f"Arquivo salva na pasta {path}")
