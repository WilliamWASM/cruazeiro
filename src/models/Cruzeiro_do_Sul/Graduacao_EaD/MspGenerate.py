from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
from ..Graduacao_EaD.ExtraWarningGenerate import ExtraWarningGenerate as ewa
import pandas as pd


class MspGenerate:

    FINAL_COLUMNS = [
        'commercial_discount', 'university_regressive_discount', 'discount_percentage',
        'real_discount', 'desconto_balcao_final', 'regressive_discount', 'regressive_commercial_discount',
        'first_regressive_discount', 'second_regressive_discount', 'last_regressive_discount',
        'offered_price', 'name_from_university', 'university_name', 'university_id',
        'campus_name', 'campus_id', 'name', 'level', 'kind', 'shift', 'period_kind',
        'max_periods', 'COD SIAA', 'full_price', 'start', 'end', 'limited', 'total_seats',
        'offer_special_conditions', 'offer_extra_warning', 'enrollment_semester',
        'max_payments', 'metadata', 'course_metadata', 'offer_extra_benefit',
        'ID_POLO', 'POLO_SEDE', 'COD_EMPR', 'COD_INST', 'COD_CURS'
    ]

    def __init__(self, campus_offers, campus_group, campus_virtual):
        self.campus_offers = campus_offers.copy()
        self.campus_group = campus_group.copy()
        self.campus_virtual = campus_virtual.copy()
        self.offers_virtual = pd.DataFrame()
        self.offers_negative_discount = pd.DataFrame()

    def _empty_final(self):
        return pd.DataFrame(columns=self.FINAL_COLUMNS)

    def _text_column(self, dataframe, column):
        if column not in dataframe.columns:
            return pd.Series('', index=dataframe.index)
        return dataframe[column].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)

    def _to_number(self, series):
        return pd.to_numeric(
            series.astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        ).fillna(0)

    def _set_campus_ids(self):
        if self.campus_offers.empty:
            return
        self.campus_offers['campus_id'] = self.campus_offers['lookup_group']
        self.campus_offers = dfu.normalize_lookup_columns(self.campus_offers, ['campus_id', 'lookup_group', 'lookup_3719'])

    def _get_enrollment_period(self):
        if 'Semestre de Ingresso' not in self.campus_offers.columns:
            raise ValueError(
                "Coluna 'Semestre de Ingresso' ausente ao calcular descontos regressivos."
            )
        semester = str(self.campus_offers.iloc[0]['Semestre de Ingresso']).strip()
        parts = semester.split('.')
        if len(parts) != 2 or parts[1] not in ('1', '2'):
            raise ValueError(
                f"Semestre de Ingresso inválido: '{semester}'. "
                "Esperado o formato 'AAAA.1' ou 'AAAA.2'."
            )
        return int(parts[1])

    def _process_discounts(self):
        if self.campus_offers.empty:
            return

        self.campus_offers.rename(columns={
            'NOME_POL': 'campus_name_from_university',
            'CURSO': 'name',
            'GRAU': 'level',
            'METODOLOGIA': 'kind',
            'DURAÇÃO': 'max_periods',
            'PREÇO PARCELAS': 'full_price',
        }, inplace=True)

        self.campus_offers['name_from_university'] = self.campus_offers['name']
        self.campus_offers['max_periods'] = self._text_column(self.campus_offers, 'max_periods')
        period = self._get_enrollment_period()

        first_disc = self._to_number(self.campus_offers['PORCENTAGEM DE DESCONTO'])
        guaranteed_disc = self._to_number(self.campus_offers['DESCONTO GARANTIDO'])

        if period == 1:
            second_disc = first_disc
            last_disc = guaranteed_disc
        else:
            second_disc = guaranteed_disc
            last_disc = guaranteed_disc

        def _pct(series):
            return (series * 100).round().astype(int)

        def _triple(first, second, last):
            return (
                _pct(first).astype(str) + ' '
                + _pct(second).astype(str) + ' '
                + _pct(last).astype(str)
            )

        self.campus_offers['discount_percentage']          = _pct(first_disc)
        self.campus_offers['commercial_discount']          = _pct(first_disc - 0.05)
        self.campus_offers['real_discount']                = _pct(last_disc)
        self.campus_offers['desconto_balcao_final']        = _pct(last_disc - 0.05)
        self.campus_offers['regressive_commercial_discount'] = _pct(first_disc - last_disc)
        self.campus_offers['regressive_discount']          = _triple(first_disc, second_disc, last_disc)
        self.campus_offers['university_regressive_discount'] = _triple(first_disc - 0.05, second_disc - 0.05, last_disc - 0.05)

        self.campus_offers['PORCENTAGEM DE DESCONTO'] = _pct(first_disc)
        self.campus_offers['_second_disc']            = _pct(second_disc)
        self.campus_offers['_last_disc']              = _pct(last_disc)

    def _compute_derived_values(self):
        if self.campus_offers.empty:
            return

        self.campus_offers['COD SIAA'] = self.campus_offers.get('CÓDIGO SIAA')
        # self.campus_offers['metadata'] = (
        #     'code:' + self._text_column(self.campus_offers, 'COD_CURS') +
        #     ';campus_code:' + self._text_column(self.campus_offers, 'ID_POLO') +
        #     ';ies_code:' + self._text_column(self.campus_offers, 'CÓDIGO DA IES')
        # )

        self.campus_offers['total_seats'] = None
        self.campus_offers['max_payments'] = None
        self.campus_offers['course_metadata'] = None

    def _lookup_campus_fields(self, dataframe, campus_dataframe):
        if dataframe.empty:
            return dataframe

        dataframe = dataframe.copy()
        campus_dataframe = dfu.normalize_lookup_columns(campus_dataframe.copy(), ['id', 'university_id'])
        dataframe = dfu.normalize_lookup_columns(dataframe, ['campus_id'])

        lookup_map = {
            'name': 'campus_name',
            'university_name': 'university_name',
            'university_id': 'university_id'
        }
        for source_column, target_column in lookup_map.items():
            if source_column in campus_dataframe.columns:
                dataframe = dfu.xlookup(
                    dataframe, campus_dataframe, 'campus_id', 'id',
                    source_column, target_column
                )
        return dataframe

    def _fill_in_remaining_values(self):
        if self.campus_offers.empty:
            return
        self.campus_offers = self._lookup_campus_fields(self.campus_offers, self.campus_group)
        self.campus_offers = ewa(self.campus_offers).load()

    def _append_certification_warning(self, dataframe):
        base_warning = self._text_column(dataframe, 'Avisos')
        certification = self._text_column(dataframe, 'certification_name')

        extra_warning = certification.map(
            lambda value: f"Certificado pela {value}" if value else ''
        )
        dataframe['Avisos'] = [
            ' | '.join(part for part in [base, extra] if part)
            for base, extra in zip(base_warning, extra_warning)
        ]
        return dataframe

    def _generate_virtual_offers(self):
        if self.campus_offers.empty:
            self.offers_virtual = self.campus_offers.copy()
            return

        virtual_mask = self.campus_offers['lookup_3719'].notna()
        self.offers_virtual = self.campus_offers[virtual_mask].copy()

        if not self.offers_virtual.empty:
            self.offers_virtual['campus_id'] = self.offers_virtual['lookup_3719']
            self.offers_virtual = self._lookup_campus_fields(self.offers_virtual, self.campus_virtual)
            self.offers_virtual['university_id'] = '3719'
            self.offers_virtual = self._append_certification_warning(self.offers_virtual)

        self.campus_offers = self.campus_offers[
            self.campus_offers['lookup_group'].notna()
        ].reset_index(drop=True)

    def _finalize_dataframe(self, dataframe):
        if dataframe.empty:
            return self._empty_final()

        final_rename = {
            'PORCENTAGEM DE DESCONTO': 'first_regressive_discount',
            '_second_disc': 'second_regressive_discount',
            '_last_disc': 'last_regressive_discount',
            'Turno': 'shift',
            'Tipo de duração do curso': 'period_kind',
            'LIMITADA?': 'limited',
            'Data de Início da Oferta': 'start',
            'Data de Fim da Oferta': 'end',
            'Benefício 1 (Chave OSC)': 'offer_special_conditions',
            #'Benefício 2 (Chave OSC)': 'offer_extra_benefit',
            'Semestre de Ingresso': 'enrollment_semester',
            'Avisos': 'offer_extra_warning',
        }

        dataframe = dataframe.rename(columns=final_rename).copy()
        for column in self.FINAL_COLUMNS:
            if column not in dataframe.columns:
                dataframe[column] = None
        return dataframe[self.FINAL_COLUMNS].reset_index(drop=True)

    def _separate_negative_discounts(self):
        if self.campus_offers.empty:
            return
        negative_mask = self.campus_offers['desconto_balcao_final'] < 0
        self.offers_negative_discount = self.campus_offers[negative_mask].copy()
        self.campus_offers = self.campus_offers[~negative_mask].reset_index(drop=True)

    def _deduplicate_by_sku(self, dataframe):
        if dataframe.empty:
            return dataframe
        sku_columns = [
            'university_id',
            'campus_id',
            'name',
            'level',
            'kind',
            'Turno',
            'Semestre de Ingresso',
            'max_payments',
            'full_price',
            'COD SIAA',
        ]
        subset = [col for col in sku_columns if col in dataframe.columns]
        return dataframe.drop_duplicates(subset=subset).reset_index(drop=True)

    def load(self):
        self._set_campus_ids()
        self._process_discounts()
        self._separate_negative_discounts()
        self._compute_derived_values()
        self._fill_in_remaining_values()
        self._generate_virtual_offers()
        self.campus_offers = self._deduplicate_by_sku(self.campus_offers)
        self.offers_virtual = self._deduplicate_by_sku(self.offers_virtual)
        offers_group = self._finalize_dataframe(self.campus_offers)
        offers_virtual = self._finalize_dataframe(self.offers_virtual)
        return offers_group, offers_virtual, self.offers_negative_discount
