import pandas as pd
from MODELS.excel_file.DataFrameUtils import DataFrameUtils as dfu
class ExtraWarningGenerate:
    def __init__(self,msp_offers):
        self.msp_offers = msp_offers
        self.warning_special = 'Este curso, é necessário ter a comprovação de no mínimo 160 horas.  Assim, é possível concluir o curso em até 4 semestres | EaD 100% Virtual, sendo necessário que o aluno se matricule para esta opção no site da instituição | Condições válidas para matrículas efetivadas até 7 dias corridos após o pagamento da pré-matrícula no site que garantiu a bolsa'

        self.relation_kind = pd.DataFrame({
            "Modalidade": ['EaD','Ao vivo', 'Semipresencial'],
            "extra_warning": ['EaD 100% Virtual, sendo necessário que o aluno se matricule para esta opção no site da instituição | Condições válidas para matrículas efetivadas até 7 dias corridos após o pagamento da pré-matrícula no site que garantiu a bolsa',
                              'EaD 100% Virtual  com Aulas ao vivo, sendo necessário que o aluno se matricule para esta opção no site da instituição | Condições válidas para matrículas efetivadas até 7 dias corridos após o pagamento da pré-matrícula no site que garantiu a bolsa',
                              'O EAD Semipresencial une o melhor do ensino a distância com o presencial, sendo necessário que o aluno se matricule para esta opção no site da instituição | Condições válidas para matrículas efetivadas até 7 dias corridos após o pagamento da pré-matrícula no site que garantiu a bolsa']
        })

    def load(self):
        self.msp_offers = dfu.xlookup(self.msp_offers,self.relation_kind,'Modalidade','Modalidade','extra_warning','Avisos')
        self.msp_offers.loc[self.msp_offers["Nome do Curso"].str.contains("2.0", na=False), "Avisos"] = self.warning_special
        return self.msp_offers 
    
             