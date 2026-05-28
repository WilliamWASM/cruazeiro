from ...excel_file.DataFrameUtils import DataFrameUtils as dfu
from ..Graduacao_EaD.ExtraWarningGenerate import ExtraWarningGenerate as ewa
import pandas as pd

class MspGenerate:

    FINAL_COLUMNS = [
        'commercial_discount', 'university_regressive_discount', 'discount_percentage',
        'real_discount', 'regressive_discount', 'regressive_commercial_discount',
        'first_regressive_discount', 'second_regressive_discount', 'last_regressive_discount',
        'offered_price', 'name_from_university', 'university_name', 'university_id',
        'campus_name', 'campus_id', 'name', 'level', 'kind', 'shift', 'period_kind',
        'max_periods', 'COD SIAA', 'full_price', 'start', 'end', 'limited', 'total_seats',
        'offer_special_conditions', 'offer_extra_warning', 'enrollment_semester',
        'max_payments', 'metadata', 'course_metadata', 'offer_extra_benefit'
    ]

    def __init__(self, campus_offers, campus_group, campus_virtual):
        self.campus_offers = campus_offers
        self.campus_group = campus_group
        self.campus_virtual = campus_virtual

    def _set_campus_ids(self):
        # campus_id recebe o id do marketplace (lookup_group), não o ID_POLO da IES
        self.campus_offers['campus_id'] = self.campus_offers['lookup_group']

    def _get_enrollment_period(self):
        try:
            semester = str(self.campus_offers.iloc[0]['Semestre de Ingresso'])
            return int(semester.split('.')[1]) if '.' in semester else 2
        except Exception:
            return 2

    def _to_ies_discount(self, series):
        s = pd.to_numeric(
            series.astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        ).fillna(0) - 0.05
        return s.map(lambda x: f"{x:.2f}")

    def _process_discounts(self):
        period = self._get_enrollment_period()

        # Renomeia colunas principais para os nomes finais
        self.campus_offers.rename(columns={
            'NOM_FILI': 'name_from_university',
            'NOME_POL': 'campus_name',
            'CURSO': 'name',
            'GRAU': 'level',
            'METODOLOGIA': 'kind',
            'DURAÇÃO': 'max_periods',
            'PREÇO PARCELAS': 'full_price',
        }, inplace=True)

        if period == 1:
            # Semestre .1: desconto do 2º = mesmo do 1º; regressão só no 3º (próximo janeiro)
            self.campus_offers['_second_disc'] = self.campus_offers['PORCENTAGEM DE DESCONTO']
            self.campus_offers['_last_disc'] = self.campus_offers['DESCONTO GARANTIDO']
        else:
            # Semestre .2: já regride no 2º semestre (próximo janeiro)
            self.campus_offers['_second_disc'] = self.campus_offers['DESCONTO GARANTIDO']
            self.campus_offers['_last_disc'] = self.campus_offers['DESCONTO GARANTIDO']

        # Descontos comerciais (IES) = desconto do aluno - 5%
        self.campus_offers['commercial_discount'] = self._to_ies_discount(
            self.campus_offers['PORCENTAGEM DE DESCONTO'])
        self.campus_offers['regressive_commercial_discount'] = self._to_ies_discount(
            self.campus_offers['_second_disc'])
        self.campus_offers['university_regressive_discount'] = self._to_ies_discount(
            self.campus_offers['_last_disc'])

        # Aliases de desconto do aluno
        self.campus_offers['discount_percentage'] = self.campus_offers['PORCENTAGEM DE DESCONTO']
        self.campus_offers['regressive_discount'] = self.campus_offers['_second_disc']

    def _compute_derived_values(self):
        fp = pd.to_numeric(
            self.campus_offers['full_price'].astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        ).fillna(0)
        dp = pd.to_numeric(
            self.campus_offers['PORCENTAGEM DE DESCONTO'].astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        ).fillna(0)

        self.campus_offers['offered_price'] = (fp * (1 - dp)).round(2)
        self.campus_offers['real_discount'] = (fp * dp).round(2)

        self.campus_offers['COD SIAA'] = self.campus_offers['CÓDIGO SIAA']
        self.campus_offers['metadata'] = (
            'code:' + self.campus_offers['COD_CURS'].astype(str) +
            ';campus_code:' + self.campus_offers['ID_POLO'].astype(str) +
            ';cod_ies:' + self.campus_offers['CÓDIGO DA IES'].astype(str)
        )

        self.campus_offers['total_seats'] = None
        self.campus_offers['max_payments'] = None
        self.campus_offers['offer_extra_benefit'] = None

    def _fill_in_remaining_values(self):
        # university_id via nome normalizado da IES → university_name no campus_group
        self.campus_offers = dfu.xlookup(
            self.campus_offers, self.campus_group,
            'name_from_university', 'university_name', 'university_id', 'university_id'
        )
        # university_name completo via campus_id → id no campus_group
        self.campus_offers = dfu.xlookup(
            self.campus_offers, self.campus_group,
            'campus_id', 'id', 'university_name', 'university_name'
        )
        # Gera o aviso conforme modalidade
        self.campus_offers = ewa(self.campus_offers).load()

    def _generate_virtual_offers(self):
        # Somente polos presentes no campus_virtual recebem oferta virtual
        virtual_mask = self.campus_offers['lookup_3719'].notna()
        self.offers_virtual = self.campus_offers[virtual_mask].copy()

        self.offers_virtual['campus_id'] = self.offers_virtual['lookup_3719']
        # Re-resolve university_name pelo campus do 3719
        self.offers_virtual = dfu.xlookup(
            self.offers_virtual, self.campus_virtual,
            'campus_id', 'id', 'university_name', 'university_name'
        )
        self.offers_virtual['Avisos'] = (
            self.offers_virtual['Avisos'] + " | Certificado pela " +
            self.offers_virtual['name_from_university']
        )
        self.offers_virtual['university_id'] = '3719'
        self.offers_virtual['name_from_university'] = 'Cruzeiro Virtual'

        # campus_offers fica apenas com as linhas que têm campus no grupo
        self.campus_offers = self.campus_offers[
            self.campus_offers['lookup_group'].notna()
        ].reset_index(drop=True)

    def _finalize_dataframe(self, df):
        # Renomeia os últimos nomes intermediários para o formato final
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
            'Semestre de Ingresso': 'enrollment_semester',
            'Avisos': 'offer_extra_warning',
        }
        df = df.rename(columns=final_rename)
        # Garante que todas as colunas finais existam (vazio se ausente)
        for col in self.FINAL_COLUMNS:
            if col not in df.columns:
                df[col] = None
        return df[self.FINAL_COLUMNS].reset_index(drop=True)

    def load(self):
        self._set_campus_ids()
        self._process_discounts()
        self._compute_derived_values()
        self._fill_in_remaining_values()
        self._generate_virtual_offers()
        offers_group = self._finalize_dataframe(self.campus_offers)
        offers_virtual = self._finalize_dataframe(self.offers_virtual)
        return offers_group, offers_virtual
