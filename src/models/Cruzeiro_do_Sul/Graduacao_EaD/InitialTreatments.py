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
        self.offers_to_campus = dfu.normalize_lookup_columns(self.offers_to_campus, ['ID_POLO', 'COD_INST'])

    def _consolidate_offers_by_course(self):
        if 'Cód. Curso' not in self.offers.columns:
            return

        watched_columns = [
            'Cód. IES', 'Cód. Campus', 'Código SIAA', 'Certificadora', 'Curso',
            'GRAU', 'Modalidade', 'Duração', 'Preço SIAA',
            'Porcentagem com Desconto 1° ano',
            'Desconto Garantido Demais Semestres'
        ]
        watched_columns = [col for col in watched_columns if col in self.offers.columns]
        conflict_frames = []

        for course_code, group in self.offers.groupby('Cód. Curso', dropna=False, sort=False):
            if pd.isna(course_code) or len(group) <= 1:
                continue

            conflict_columns = [
                col for col in watched_columns
                if dfu.normalize_lookup_key(group[col].fillna('')).nunique(dropna=False) > 1
            ]
            if conflict_columns:
                conflict = group.copy()
                conflict['conflict_columns'] = ' | '.join(conflict_columns)
                conflict_frames.append(conflict)

        if conflict_frames:
            self.offer_conflicts = pd.concat(conflict_frames, ignore_index=True)

        self.offers = self.offers.drop_duplicates(subset='Cód. Curso', keep='first').reset_index(drop=True)

    def _unpivot_campus_relation(self):
        curso_cols = [col for col in self.offers_to_campus.columns if col.startswith('CURSO_')]
        id_vars = [
            col for col in ['ID_POLO', 'NOME_POL', 'CIDADE', 'ESTADO', 'NOM_FILI', 'COD_INST']
            if col in self.offers_to_campus.columns
        ]

        self.offers_to_campus = self.offers_to_campus.melt(
            id_vars=id_vars,
            value_vars=curso_cols,
            var_name='CURSO_COL',
            value_name='PRESENTE'
        )

        presente = self.offers_to_campus['PRESENTE'].astype('string').str.strip().str.upper()
        self.offers_to_campus = self.offers_to_campus[presente == 'X'].copy()
        self.offers_to_campus['COD_CURS'] = self.offers_to_campus['CURSO_COL'].str.replace('CURSO_', '', regex=False)
        self.offers_to_campus = dfu.normalize_lookup_columns(self.offers_to_campus, ['ID_POLO', 'COD_CURS', 'COD_INST'])
        self.offers_to_campus = (
            self.offers_to_campus
            .drop(columns=['CURSO_COL', 'PRESENTE'])
            .drop_duplicates(subset=['ID_POLO', 'COD_CURS'])
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
        self._consolidate_offers_by_course()
        self._unpivot_campus_relation()
        self._separate_group()
        self._normalize_ies_names()
        self._verify_offers_to_campus_not_match()
        self._verify_campus_totally_existence()
        return [self.offers, self.offers_to_campus, self.campus_group, self.campus_virtual,
                self.campus_offers_undefined, self.not_totally_group, self.not_totally_virtual,
                self.offer_conflicts]

    def _multiple_replaces(self, dataframe, header, values_dict: dict):
        for original_value, new_value in values_dict.items():
            dataframe = dfu.replace_series(dataframe, header, original_value, new_value)
        return dataframe
