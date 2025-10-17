import pandas as pd
import os
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
from GUI.widgets.notifications import Notification

class RemoverUniversityOfferDuplicates:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.sheet = sma(self.excel_file)
        self.df = self.sheet.load()
        self.type_table = self.sheet.get_sheet_type()
        self.df_high_full_price = pd.DataFrame()
        self.df_low_full_price =  pd.DataFrame()
        self.output_file = pd.DataFrame()

    def _get_sku_by_type(self):
        if (self.type_table == "msp_offers"):
            self.df['sku'] = dfu.concat_series_with_separator([self.df["ID da IES"], self.df["ID do Campus"], self.df["Nome do Curso"], self.df["Grau"], self.df["Modalidade"], self.df["Turno"], self.df["Semestre de Ingresso"], self.df["Quantidade de Parcelas"]], separator = "_")
        elif  (self.type_table == "exp_offers"):
            self.df['sku'] = dfu.concat_series_with_separator([self.df["university_id"], self.df["campus_id"], self.df["name_from_university"], self.df["level"], self.df["kind"], self.df["shift"], self.df["enrollment_semester"], self.df["max_payments"]], separator = "_")
        else:
            raise ValueError("Tipo de tabela não reconhecido")

    def _compare_prices_by_sku(self):
        if (self.type_table == "msp_offers"):
            price_type = "Mensalidade sem desconto"
        elif  (self.type_table == "exp_offers"):
            price_type = "full_price"
        else:
            raise ValueError("Tipo de tabela não reconhecido")
        lower_index = self.df.groupby('sku')[price_type].idxmin()

        df_min_price = self.df.groupby('sku')[price_type].transform('min')
        mask_equal = self.df[price_type] == df_min_price
        self.df_low_full_price = self.df[mask_equal]
        self.df_high_full_price = self.df.drop(self.df_low_full_price.index)
    
    def execute(self):
        base_name = os.path.splitext(os.path.basename(self.excel_file))[0]
        self.output_file = os.path.join(os.path.dirname(self.excel_file), f"Offers_by_sku_{base_name}.xlsx")
        self._get_sku_by_type()
        self._compare_prices_by_sku()
        dfu.save_multiple_dataframes([self.df_low_full_price, self.df_high_full_price], self.output_file, ["Menor Preço", "Maior Preço"])
