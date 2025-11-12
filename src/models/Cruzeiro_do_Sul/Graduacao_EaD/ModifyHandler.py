from ..Graduacao_EaD.AdjustmentsOffersPattern import AdjustmentsOffersPattern
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
        self.not_totally_group = self.list_treated[5]
        self.not_totally_virtual = self.list_treated[6]

    def set_values(self,enrollment_semester,end_date,special_condition):
        adj_offers = AdjustmentsOffersPattern(self.offers,self.offers_to_campus,enrollment_semester,end_date,special_condition)
        self.offers_to_campus = adj_offers.load()
        if not self._verify_if_empty(self.not_totally_group):
            adj_not_tot_group = AdjustmentsOffersPattern(self.offers,self.not_totally_group,enrollment_semester,end_date,special_condition)
            self.not_totally_group = adj_not_tot_group.load()
        if not self._verify_if_empty(self.not_totally_virtual):
            adj_not_tot_virtual = AdjustmentsOffersPattern(self.offers,self.not_totally_virtual,enrollment_semester,end_date,special_condition)
            self.not_totally_virtual = adj_not_tot_virtual.load()

    def _generate_msp(self):
        offers_msp = mgen(self.offers_to_campus,self.campus_group)
        self.offers_generated,self.offers_virtual = offers_msp.load()
        self.offers_generated = dfu.concat_dataframes(self.offers_generated,self.offers_virtual)

    def load(self,fullpath):
        self._generate_msp()
        if not self._verify_if_empty(self.campus_offers_undefined):
            dfu.save_multiple_dataframes([self.offers_generated,self.campus_offers_undefined,self.not_totally_group,self.not_totally_virtual],fullpath,
                                         ['Ofertas para subir','campi_not_found','group_not_found','virtual_not_found'])
        else:
            dfu.save_multiple_dataframes([self.offers_generated,self.not_totally_group,self.not_totally_virtual],fullpath,
                                         ['Ofertas para subir','group_not_found','virtual_not_found'])

    def _verify_if_empty(self,dataframe):
        return dataframe.empty
        