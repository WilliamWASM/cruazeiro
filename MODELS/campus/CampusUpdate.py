from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd

class CampusUpdate:
    def __init__(self,campus_update,exp):
        self.campus_update = campus_update
        self.exp_verify = exp

    def _remove_extra_columns(self):
    # verificar a lista de colunas excedentes e remover
        if not self.campus_update.empty:
            columns_to_remove = []
            if 'concat1' in self.campus_update.columns:
                columns_to_remove.append('concat1')
            columns_difference = self.campus_update.columns.difference(self.exp_verify.columns)
            columns_to_remove.extend(columns_difference.tolist())
            self.campus_update = self.campus_update.loc[:, ~self.campus_update.columns.isin(columns_to_remove)]
            self.exp_verify = self.exp_verify.loc[:, ~self.exp_verify.columns.isin(columns_to_remove)]

    def _remove_extra_rows(self):
        self.exp_verify = self.exp_verify[self.exp_verify['id'].isin(self.campus_update['id'])]

    def _drop_rows_duplicated(self):
        self.campus_update = dfu.remove_duplicates_by_columns(self.campus_update,'id')
        self.exp_verify = dfu.remove_duplicates_by_columns(self.exp_verify,'id')
    
    def _rows_verifies(self):
        self._remove_extra_rows()
        self._drop_rows_duplicated()
        self.campus_update = self.campus_update.sort_values(by="id").reset_index(drop=True)
        self.exp_verify = self.exp_verify.sort_values(by="id").reset_index(drop=True)

    def _separate_infos_in_columns(self):
        columns_update = list(self.campus_update.columns)
        if 'virtual' in columns_update:
            columns_update.remove('virtual')
        for column in columns_update:
            if column in ['id','university_id']:
                continue
            mask = self.campus_update[column].eq(self.exp_verify[column])
            self.campus_update.loc[mask, column] = True

    def _drop_columns_all_ignore(self):
        for col in self.campus_update.columns:
            if col == 'virtual' and self.campus_update[col].eq(False).all():
                self.campus_update.drop(columns= col, inplace=True)
            else:
                if self.campus_update[col].eq(True).all():
                    self.campus_update.drop(columns= col, inplace=True)

    def _fill_in_true_where_ignore(self):
        cols = self.campus_update.columns.difference(['id','university_id'])
        self.campus_update = self.campus_update.reset_index(drop=True)
        self.exp_verify = self.exp_verify.reset_index(drop=True)
        for col in cols:
            mask = self.campus_update[col].eq(True)
            self.campus_update.loc[mask, col] = 'ignore'

    def default_update_columns(self):
        self.campus_update['id'] = self.campus_update['id'].astype(int)
        self._remove_extra_columns()
        self._rows_verifies()
        self._separate_infos_in_columns()
        self._drop_columns_all_ignore()
        self._fill_in_true_where_ignore()
        return self.campus_update