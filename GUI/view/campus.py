from GUI.content_area import *
from GUI.widgets.cards import *
from GUI.widgets.notifications import *
from MODELS.campus.CampusVerifications import *
from MODELS.campus.UniasselviCampus import *


class Campus(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)
        
        self.campus = Card("campus","#FF7E29")
        self.campus.create_front_card("Campus","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione MSP Polos")
        self.campus.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione Exp de Campus e MSP Polos. \n2.Clique em 'Gerar'\n\n3. Selecione o diretório e nome do arquivo que será gerado")
        btn2_exp = self.campus.create_btn("Selecione exp campus","#F5F5F5","#000000","5px","#D4D4D4",170,30)
        self.campus.add_component_card(btn2_exp)
        self.campus.set_action_btn("btn_generate", self.process_campus)

        self.campus_uni_ead = Card("Uniasselvi EaD","#FF7E29")
        self.campus_uni_ead.create_front_card("Uniasselvi EaD","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione Planilha Campus")
        self.campus_uni_ead.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione Exp de Campus e MSP Polos. \n2.Clique em 'Gerar'\n\n3. Selecione o diretório e nome do arquivo que será gerado")
        btn2_exp_uni_ead = self.campus_uni_ead.create_btn("Selecione exp campus","#F5F5F5","#000000","5px","#D4D4D4",170,30)
        self.campus_uni_ead.add_component_card(btn2_exp_uni_ead)
        self.campus_uni_ead.set_action_btn("btn_generate", self.process_uni_ead)

        self.campus_uni_pres = Card("Uniasselvi Presencial","#FF7E29")
        self.campus_uni_pres.create_front_card("Uniasselvi Presencial","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione Planilha Campus")
        self.campus_uni_pres.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione Exp de Campus e MSP Polos. \n2.Clique em 'Gerar'\n\n3. Selecione o diretório e nome do arquivo que será gerado")
        btn2_exp_uni_pres = self.campus_uni_pres.create_btn("Selecione exp campus","#F5F5F5","#000000","5px","#D4D4D4",170,30)
        self.campus_uni_pres.add_component_card(btn2_exp_uni_pres)
        self.campus_uni_pres.set_action_btn("btn_generate", self.process_uni_pres)

        self.add_card(self.campus,"TOP")
        self.add_card(self.campus_uni_ead,"TOP")
        self.add_card(self.campus_uni_pres,"TOP")


    def process_campus(self):
        msp = self.campus.paths["btn_option1"]
        exp = self.campus.paths["btn_option2"]
        if msp and exp:
            try:
                self.campus.set_save_manager("btn_generate")
                path_save = self.campus.paths["save"]
                campus = CampusVerifications(exp,msp)
                if not path_save:
                        Notification.error("Diretório inválido","Erro ao tentar gerar planilha final. Diretório não selecionado ou inválido. Execute a operação novamente, selecionando um diretório válido.")
                else:
                    campus.load(path_save)
                    Notification.info("Operação finalizada","Planilha gerada com sucesso.")
                self.campus.set_text_btns(["btn_option1","btn_option2"])
            except Exception as e:
                Notification.error("Erro ao gerar Planilha", f"Erro ao tentar gerar planilha final.\nDetalhes: {e}")
    
    def process_uni_ead(self):
        msp = self.campus_uni_ead.paths["btn_option1"]
        exp = self.campus_uni_ead.paths["btn_option2"]
        if msp and exp:
            try:
                self.campus_uni_ead.set_save_manager("btn_generate")
                path_save = self.campus_uni_ead.paths["save"]
                campus = UniasselviCampus(exp,msp,'EAD')
                if not path_save:
                        Notification.error("Diretório inválido","Erro ao tentar gerar planilha final. Diretório não selecionado ou inválido. Execute a operação novamente, selecionando um diretório válido.")
                else:
                    campus.load(path_save)
                    Notification.info("Operação finalizada","Planilha gerada com sucesso.")
                self.campus_uni_ead.set_text_btns(["btn_option1","btn_option2"])
            except Exception as e:
                Notification.error("Erro ao gerar Planilha", f"Erro ao tentar gerar planilha final.\nDetalhes: {e}")

    def process_uni_pres(self):
        msp = self.campus_uni_pres.paths["btn_option1"]
        exp = self.campus_uni_pres.paths["btn_option2"]
        if msp and exp:
            try:
                self.campus_uni_pres.set_save_manager("btn_generate")
                path_save = self.campus_uni_pres.paths["save"]
                campus = UniasselviCampus(exp,msp,'PRESENCIAL')
                if not path_save:
                        Notification.error("Diretório inválido","Erro ao tentar gerar planilha final. Diretório não selecionado ou inválido. Execute a operação novamente, selecionando um diretório válido.")
                else:
                    campus.load(path_save)
                    Notification.info("Operação finalizada","Planilha gerada com sucesso.")
                self.campus_uni_pres.set_text_btns(["btn_option1","btn_option2"])
            except Exception as e:
                Notification.error("Erro ao gerar Planilha", f"Erro ao tentar gerar planilha final.\nDetalhes: {e}")