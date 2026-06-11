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
        self.offer_conflicts = self.list_treated[7]
        self.offers_without_relation = self.list_treated[8]
        self.offers_negative_discount = pd.DataFrame()

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
        offers_msp = mgen(self.offers_to_campus, self.campus_group, self.campus_virtual)
        self.offers_group, self.offers_virtual, self.offers_negative_discount = offers_msp.load()

    def load(self,fullpath):
        self._generate_msp()
        # Abas principais separadas por IES
        sheets = [self.offers_group, self.offers_virtual]
        names = ['Ofertas Grupo', 'Ofertas 3719']
        # Abas auxiliares (somente se não vazias)
        if not self._verify_if_empty(self.campus_offers_undefined):
            sheets.append(self.campus_offers_undefined)
            names.append('campi_not_found')
        if not self._verify_if_empty(self.not_totally_group):
            sheets.append(self.not_totally_group)
            names.append('apenas_no_virtual')
        if not self._verify_if_empty(self.not_totally_virtual):
            sheets.append(self.not_totally_virtual)
            names.append('criar_no_3719')
        if not self._verify_if_empty(self.offer_conflicts):
            sheets.append(self.offer_conflicts)
            names.append('ofertas_codigo_conflitos')
        if not self._verify_if_empty(self.offers_without_relation):
            sheets.append(self.offers_without_relation)
            names.append('ofertas_sem_relacao')
        if not self._verify_if_empty(self.offers_negative_discount):
            sheets.append(self.offers_negative_discount)
            names.append('Ofertas com Desconto Negativo')
        dfu.save_multiple_dataframes(sheets, fullpath, names)

    def _verify_if_empty(self,dataframe):
        return dataframe.empty
