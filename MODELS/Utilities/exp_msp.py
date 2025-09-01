import pandas as pd
import os
from GUI.widgets.notifications import Notification
from MODELS.excel_file.SheetManipulation import SheetManipulation as sma
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu

class MSPConverter:
    def __init__(self,exp_file):
        self.exp_file = exp_file
        self.sheet = sma(self.exp_file)
        self.df = self.sheet.load()
        
        self.offers_msp_dict = {
            'university_name': 'Nome da IES',
            'university_id': 'ID da IES',
            'campus_name_from_university': 'Nome do Campus',
            'campus_id': 'ID do Campus',
            'name_from_university': 'Nome do Curso',
            'level': 'Grau',
            'kind': 'Modalidade',
            'shift': 'Turno',
            'period_kind': 'Tipo de duração do curso',
            'max_periods': 'Duração do Curso',
            'max_payments': 'Quantidade de Parcelas',
            'full_price': 'Mensalidade sem desconto',
            'offered_price': 'Mensalidade com desconto',
            'discount_percentage': 'Porcentagem de desconto da bolsa (Fixo/1º Semestre)',
            'commercial_discount': 'Mensalidade balcão',
            'university_regressive_discount': 'Porcentagem de desconto IES',
            'start': 'Data de Início da Oferta',
            'end': 'Data de Fim da Oferta',
            'limited': 'LIMITADA?',
            'total_seats': 'Quantidade de Vagas',
            'enrollment_semester': 'Semestre de Ingresso',
            'offer_special_conditions': 'Benefício 1 (Chave OSC)',
            'offer_extra_warning': 'Avisos',
            'offer_extra_benefit': 'Benefícios Extras',
            'campaign': 'Campanha',
            'restricted': 'Restrita?',
            'systems': 'Tipo de restrição (systems:)',
            'ecode_pool_name': 'ecode_pool_name'
        }
        self.remove_columns = [
            'offer_id', 'campus_name', 'name', 'regressive_discount',
            'real_discount', 'created_at', 'paid_seats', 'reserved_seats',
            'saleable_seats', 'position', 'campus_state', 'univ_offer_enabled',
            'course_enabled', 'offer_enabled', 'open_channel_type', 'status',
            'university_offer_id', 'course_id', 'forced_disabled',
            'passing_grade', 'external_id', 'uuid', 'show_on_main_search',
            'stock_type'
        ]
        self.extra_columns = [
            ('Qual valor usar? % ou R$', 'Quantidade de Parcelas', ''),
            ('Porcentagem total de desconto da bolsa (2º Semestre)', 'Porcentagem de desconto da bolsa (Fixo/1º Semestre)', ''),
            ('Mensalidade com desconto (2º Semestre)', 'Porcentagem total de desconto da bolsa (2º Semestre)', ''),
            ('Frequência das aulas', 'Campanha', ''),
            ('Taxa de matrícula', 'Frequência das aulas', ''),
            ('Data de início das aulas', 'Taxa de matrícula', ''),
            ('Carga horária do Curso (em horas)', 'Data de início das aulas', ''),
            ('TCC Obrigatório?', 'Carga horária do Curso (em horas)', ''),
            ('Benefício 2 (Chave OSC)', 'Benefício 1 (Chave OSC)', ''),
            ('COD CURSO', 'Tipo de restrição (systems:)', ''),
            ('COD IES', 'COD CURSO', ''),
            ('COD CAMPUS', 'COD IES', ''),
            ('COD TIPO GRAD', 'COD CAMPUS', ''),
            ('COD TURNO', 'COD TIPO GRAD', ''),
            ('COD CURSO PAI', 'COD TURNO', ''),
            ('COD CAMPUS PAI', 'COD CURSO PAI', ''),
            ('CONCURSO', 'COD CAMPUS PAI', ''),
            ('CodCursoVest', 'CONCURSO', ''),
            ('CodCursoIES', 'CodCursoVest', ''),
            ('NomeCurso', 'CodCursoIES', ''),
            ('TurnoMetadata', 'NomeCurso', ''),
            ('CURRICULO', 'TurnoMetadata', ''),
            ('CodCampus', 'CURRICULO', ''),
            ('CodCampanha', 'CodCampus', ''),
            ('affiliate_link', 'CodCampanha', ''),
            ('tags', 'affiliate_link', '')
        ]
        self.metadata_mapping = {
            'code': 'COD CURSO',
            'campus_code': 'COD CAMPUS',
            'ies_code': 'COD IES',
            'level_code': 'COD TIPO GRAD',
            'shift_code': 'COD TURNO',
            'cod_curso_pai': 'COD CURSO PAI',
            'cod_campus_pai': 'COD CAMPUS PAI',
            'CONCURSO': 'CONCURSO',
            'CURSO_VEST': 'CodCursoVest',
            'CURSO': 'CodCursoIES',
            'DESCRICAO': 'NomeCurso',
            'TURNO': 'TurnoMetadata',
            'CURRICULO': 'CURRICULO',
            'UNIDADE_FISICA': 'CodCampus',
            'COD_CAMPANHA': 'CodCampanha',
            'affiliate_link': 'affiliate_link',
            'tags': 'tags'
        }
        self.course_metadata_mapping = {
            'total_hours': 'Carga horária do Curso (em horas)',
            'obligatory_monograph': 'TCC Obrigatório?'
        }
        self.clean_columns = [
            'Qual valor usar? % ou R$', 'Mensalidade com desconto',
            'Porcentagem de desconto da bolsa (Fixo/1º Semestre)', 'regressive_discount',
            'Mensalidade balcão', 'Porcentagem de desconto IES', 'Data de Início da Oferta',
            'Data de Fim da Oferta', 'LIMITADA?', 'Quantidade de Vagas', 'Semestre de Ingresso',
            'Benefício 1 (Chave OSC)', 'Benefício 2 (Chave OSC)', 'Benefícios Extras',
            'Campanha', 'Frequência das aulas', 'Taxa de matrícula', 'Data de início das aulas',
            'course_metadata', 'Restrita?', 'ecode_pool_name', 'Tipo de restrição (systems:)'
        ]

    def convert(self):
        self._remove_unwanted_columns()
        self._rename_columns()
        self._insert_empty_column_after('Nome da IES', 'v5.0 10/01')
        self._insert_extra_columns()
        self._metadata_dist('metadata', self.metadata_mapping)
        self._metadata_dist('course_metadata', self.course_metadata_mapping)
        self._clean_df(self.clean_columns)
        self._save()

    def _remove_unwanted_columns(self):
        cols_to_remove = [col for col in self.remove_columns if col in self.df.columns]
        self.df.drop(columns=cols_to_remove, inplace=True)

    def _rename_columns(self):
        self.df.rename(columns=self.offers_msp_dict, inplace=True)

    def _insert_empty_column_after(self, reference_col, new_col_name): 
        loc = self.df.columns.get_loc(reference_col)
        self.df.insert(loc=loc, column=new_col_name, value='')

    def _insert_extra_columns(self):
        for new_col, ref_col, default_val in self.extra_columns:
            if ref_col in self.df.columns:
                pos = self.df.columns.get_loc(ref_col) + 1
                self.df.insert(loc=pos, column=new_col, value=default_val)

    def _metadata_dist(self, column, mapping):
        if column in self.df.columns:
            metadata_parsed = self.df[column].apply(self._parse_metadata)
            for key, col_dest in mapping.items():
                self.df[col_dest] = metadata_parsed.apply(lambda d: d.get(key, ''))
            self.df = self.df.drop(columns=[column])

    def _parse_metadata(self, value):
        try:
            if pd.isna(value) or str(value).strip() == '':
                return {}
            result = {}
            for pair in str(value).split(';'):
                if ':' in pair:
                    key, val = pair.split(':', 1)
                    result[key.strip()] = val.strip()
            return result
        except Exception:
            print(f"⚠️ Ignorado metadata inválido: {value}")
            return {}
        
    def _clean_df(self, mapping):
        for col in mapping:
            if col in self.df.columns:
                self.df[col] = ''

    def _save(self):
        base_nome = os.path.splitext(os.path.basename(self.exp_file))[0]
        msp_file = os.path.join(os.path.dirname(self.exp_file), f"MSP_{base_nome}.xlsx")
 
        try:
            dfu.save_dataframe(self.df, msp_file,"MSP")
            Notification.info("Arquivo Salvo",f"\n✅ Arquivo {msp_file} criado com sucesso com a estrutura MSP!")
        except Exception as e:
            Notification.error("Error ao Salvar",f"Erro ao salvar o arquivo Excel: {e}")
