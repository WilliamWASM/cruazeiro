from ...excel_file.SheetManipulation import SheetManipulation as sma
from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
import pandas as pd


class InitialTreatments:
    def __init__(self,offers,campus_relation,exp_campus):
        self.offers = offers
        self.campus_relation = campus_relation
        self.campus = exp_campus
        self.name_ies_map = {
            'UNICID - GRADUAÇÃO EAD' : 'UNICID',
            'CRUZEIRO DO SUL - GRADUAÇÃO EAD' : 'UNICSUL - Cruzeiro do Sul',
            'UNIFRAN - GRADUAÇÃO EAD' : 'UNIFRAN',
            'FSG - GRADUAÇÃO EAD' : 'FSG',
            'UNIPÊ - GRADUAÇÃO EAD' : 'UNIPÊ',
            'BRAZ CUBAS - GRAD EAD' : 'Brazcubas',
            'POSITIVO - GRAD. EAD' : 'Universidade Positivo'
        }
        self.campus_offers_undefined = pd.DataFrame()
        self.not_totally_group = pd.DataFrame()
        self.not_totally_virtual = pd.DataFrame()
        self.offer_conflicts = pd.DataFrame()
        self.offers_without_relation = pd.DataFrame()

    def _load_dataframes(self):
        self.offers = sma(self.offers).load()
        self.offers_to_campus = sma(self.campus_relation).load()
        self.campus = sma(self.campus).load()

    def _normalize_offer_headers(self):
        header_aliases = {
            'Grau': 'GRAU',
        }
        for source_header, target_header in header_aliases.items():
            if source_header in self.offers.columns and target_header not in self.offers.columns:
                self.offers.rename(columns={source_header: target_header}, inplace=True)

    def _normalize_loaded_keys(self):
        self.offers = dfu.normalize_lookup_columns(self.offers, ['Cód. Curso', 'Cód. Campus', 'Código SIAA'])
        self.campus = dfu.normalize_lookup_columns(self.campus, ['id', 'metadata_code', 'university_id'])
        self.offers_to_campus = dfu.normalize_lookup_columns(
            self.offers_to_campus,
            ['ID_POLO', 'COD_INST', 'COD_CURS', 'COD SIAA', 'POLO_SEDE', 'COD_EMPR']
        )

    def _build_offers_match_key(self):
        if 'Código SIAA' not in self.offers.columns:
            return
        self.offers['MATCH_KEY'] = dfu.normalize_lookup_key(self.offers['Código SIAA'])

    def _detect_offer_conflicts(self):
        if 'MATCH_KEY' not in self.offers.columns:
            return
        valid = self.offers['MATCH_KEY'].notna()
        duplicated = valid & self.offers.duplicated(subset='MATCH_KEY', keep=False)
        if duplicated.any():
            self.offer_conflicts = self.offers[duplicated].copy()

    def _build_validation_frames(self):
        if 'MATCH_KEY' not in self.offers.columns or 'MATCH_KEY' not in self.offers_to_campus.columns:
            return

        relation_key_values = self.offers_to_campus['MATCH_KEY'].dropna().unique()
        self.offers_without_relation = self.offers[
            self.offers['MATCH_KEY'].notna() & ~self.offers['MATCH_KEY'].isin(relation_key_values)
        ].copy()

    def _prepare_campus_relation(self):
        if 'COD SIAA' not in self.offers_to_campus.columns:
            return
        self.offers_to_campus['MATCH_KEY'] = self.offers_to_campus['COD SIAA']
        subset = [col for col in ['ID_POLO', 'COD SIAA'] if col in self.offers_to_campus.columns]
        self.offers_to_campus = (
            self.offers_to_campus
            .drop_duplicates(subset=subset)
            .reset_index(drop=True)
        )

    def _separate_group(self):
        self.campus_virtual = dfu.filter_content_by_column(self.campus, "3719", "university_id")
        self.campus_group = self.campus[self.campus['university_id'] != "3719"].copy()

    def _normalize_ies_names(self):
        self.offers_to_campus = self._multiple_replaces(self.offers_to_campus, 'NOM_FILI', self.name_ies_map)
        self.offers_to_campus['certification_name'] = self.offers_to_campus['NOM_FILI']

    def _verify_offers_to_campus_not_match(self):
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus, self.campus_group, 'ID_POLO', 'metadata_code', 'id', 'lookup_group')
        self.offers_to_campus = dfu.xlookup(self.offers_to_campus, self.campus_virtual, 'ID_POLO', 'metadata_code', 'id', 'lookup_3719')

        found_mask = self.offers_to_campus['lookup_group'].notna() | self.offers_to_campus['lookup_3719'].notna()
        self.campus_offers_undefined = self.offers_to_campus[~found_mask].copy()
        self.offers_to_campus = self.offers_to_campus[found_mask].reset_index(drop=True)

    def _verify_campus_totally_existence(self):
        self.not_totally_group = self.offers_to_campus[self.offers_to_campus['lookup_group'].isna()].copy()
        self.not_totally_virtual = self.offers_to_campus[self.offers_to_campus['lookup_3719'].isna()].copy()

    def load(self):
        self._load_dataframes()
        self._normalize_offer_headers()
        self._normalize_loaded_keys()
        self._build_offers_match_key()
        self._detect_offer_conflicts()
        self._prepare_campus_relation()
        self._build_validation_frames()
        self._separate_group()
        self._normalize_ies_names()
        self._verify_offers_to_campus_not_match()
        self._verify_campus_totally_existence()
        return [self.offers, self.offers_to_campus, self.campus_group, self.campus_virtual,
                self.campus_offers_undefined, self.not_totally_group, self.not_totally_virtual,
                self.offer_conflicts, self.offers_without_relation]

    def _multiple_replaces(self, dataframe, header, values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe, header, original_value, new_value)
        return dataframe
