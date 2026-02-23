import pandas as pd
import os
from ...models.excel_file.SheetManipulation import SheetManipulation as sma
from ...models.excel_file.DataFrameUtils import DataFrameUtils as dfu
from ...gui.views.notifications import Notification

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

    def _compare_prices_by_discount(self):
        if (self.type_table == "msp_offers"):
            discount_type = "Porcentagem de desconto da bolsa (Fixo/1 º Semestre)"
        elif  (self.type_table == "exp_offers"):
            discount_type = "discount_percentage"
        else:
            raise ValueError("Tipo de tabela não reconhecido")
        lower_index = self.df.groupby('sku')[discount_type].idxmin()
        
        df_min_price = self.df.groupby('sku')[discount_type].transform('max')
        mask_equal = self.df[discount_type] == df_min_price
        self.df_low_discount_percentage = self.df[mask_equal]
        self.df_high_discount_percentage = self.df.drop(self.df_low_discount_percentage.index)

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
    
    def get_offer_duplicates(self):
        self._get_sku_by_type()
    
        if self.type_table == "msp_offers":
            price_column = "Mensalidade sem desconto"
            discount_column = "Porcentagem de desconto da bolsa (Fixo/1 º Semestre)"
        elif self.type_table == "exp_offers":
            price_column = "full_price"
            discount_column = "discount_percentage"
        else:
            raise ValueError("Tipo de tabela não reconhecido")
        
        has_price_difference = (self.df.groupby('sku')[price_column].nunique() > 1).any()
        
        if has_price_difference:
            self._compare_prices_by_sku()
        else:
            self._compare_prices_by_discount()

    def get_path(self):
        base_name = os.path.splitext(os.path.basename(self.excel_file))[0]
        self.output_file = os.path.join(os.path.dirname(self.excel_file), f"Offers_by_sku_{base_name}.xlsx")

    def execute(self):
        self.get_path()
        self.get_offer_duplicates()
        dfu.save_multiple_dataframes([self.df_low_full_price, self.df_high_full_price], self.output_file, ["Menor Preço", "Maior Preço"])
