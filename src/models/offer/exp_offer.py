import pandas as pd
import os
from ...models.Utilities.duplicates import RemoverDuplicadas as rd
from ...models.Utilities.university_offer import RemoverUniversityOfferDuplicates as ruod
from ...models.excel_file.SheetManipulation import SheetManipulation as sma
from ...models.excel_file.DataFrameUtils import DataFrameUtils as dfu
from ...gui.views.notifications import Notification

class CheckAnyErrorFromOfferSheet:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.sheet = sma(self.excel_file)
        self.df = self.sheet.load()
        self.type_table = self.sheet.get_sheet_type()
        self.no_dup_df = pd.DataFrame()
        self.no_dup_offer_df = pd.DataFrame()
        self.low_price_df = pd.DataFrame()
        self.high_price_df = pd.DataFrame()
        self.headers = self.sheet.get_headers()
        self.missing_column = 0
        self.missing_headers = []

    def _check_required_headers(self, header):
        if header not in self.headers:
            self.missing_headers.append(header)
            self.missing_column += 1

    def _check_missing_columns(self):
        if self.type_table == "exp_offers":
            for columns in self.sheet.required_headers['exp_offers_general']:
                    self._check_required_headers(columns)
            if not any(columns in self.headers for columns in self.sheet.required_headers['exp_offers_offered_price']):
                self._check_required_headers(columns)
        else:
           raise ValueError("A planilha não é do tipo EXP.") 

    def generate_error_missing_columns(self):
        self._check_missing_columns()
        if self.missing_column > 0:
            missing_cols = ", ".join(self.missing_headers)
            raise ValueError(f"As seguintes colunas estão faltando na planilha: {missing_cols}")
    
    def _check_lines(row):
        return row["full_price"] == row['offered_price'] * row["discount_percentage"]
    
    def check_discount_n_price(self):
            for columns in self.sheet.required_headers['exp_offers_offered_price']:
                if all(header in self.headers for header in columns) and "full_price" in self.headers:
                   self.df["Discount_check"] = self.df.apply(self._check_lines, axis=1)

    def remove_duplicates(self):
        remover_dup = rd(self.excel_file)
        remover_dup.get_duplicates()
        self.no_dup_df = remover_dup.df_no_dup
        return self.no_dup_df
    
    def remove_duplicates_offers(self):
        remover_dup_offer = ruod(self.excel_file)
        remover_dup_offer.df = self.no_dup_df
        remover_dup_offer.get_offer_duplicates()
        remover_dup_offer.get_path()
        if remover_dup_offer.df_high_full_price.empty:
            self.no_dup_offer_df = remover_dup_offer.df_low_full_price
            dfu.save_dataframe(self.no_dup_offer_df, remover_dup_offer.output_file, "Sem Duplicatas")
        else:
            dfu.save_multiple_dataframes([remover_dup_offer.df_low_full_price, remover_dup_offer.df_low_full_price], remover_dup_offer.output_file, ["Menor Preço", "Maior Preço"])


    def execute(self):
        self.generate_error_missing_columns()
        self.check_discount_n_price()
        self.remove_duplicates()
        self.remove_duplicates_offers()