from ..Graduacao_EaD.AdjustmentsOffersPattern import AdjustmentsOffersPattern
from ..Graduacao_EaD.InitialTreatments import InitialTreatments as it
from ..Graduacao_EaD.MspGenerate import MspGenerate as mgen
from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd
class ModifyHandler:
    def __init__(self,offers,campus_relation,exp_campus):
        self.offers = offers
        self.campus_relation = campus_relation
        self.campus = exp_campus
        self._initial_treatments()
        self._set_new_variables()

    def _initial_treatments(self):
        treatments = it(self.offers,self.campus_relation,self.campus)
        self.list_treated = treatments.load()

    def _set_new_variables(self):
        self.offers = self.list_treated[0]
        self.offers_to_campus = self.list_treated[1]
        self.campus_group = self.list_treated[2]
        self.campus_virtual = self.list_treated[3]
        self.campus_offers_undefined = self.list_treated[4]

    def set_values(self,enrollment_semester,end_date,special_condition):
        adj_offers = AdjustmentsOffersPattern(self.offers,self.offers_to_campus,enrollment_semester,end_date,special_condition)
        self.offers_to_campus = adj_offers.load()

    def _generate_msp(self):
        offers_msp = mgen(self.offers_to_campus,self.campus_group)
        self.offers_grupo,self.offers_3719 = offers_msp.load()

    def load(self,fullpath):
        self._generate_msp()
        dataframes = [self.offers_grupo,self.offers_3719]
        sheet_names = ['Ofertas Grupo','Ofertas 3719']
        if not self._verify_if_empty(self.campus_offers_undefined):
            dataframes.append(self.campus_offers_undefined)
            sheet_names.append('campi_not_found')
        dfu.save_multiple_dataframes(dataframes,fullpath,sheet_names)

    def _verify_if_empty(self,dataframe):
        return dataframe.empty
        