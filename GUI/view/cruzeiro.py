from GUI.content_area import *
from GUI.widgets.cards import *
from MODELS.Cruzeiro_do_Sul.PosGradEad import PosGradEadCruzeiro
from MODELS.Cruzeiro_do_Sul.tecnico import tecnicoCruzeiro
from GUI.widgets.notifications import *


class CruzeiroDoSul(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)
        
        self.card_tecnico = Card("tecnico","#FF7E29")
        self.card_tecnico.create_front_card("Cruzeiro Técnico","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione o EXP")
        btn2_tec = self.card_tecnico.create_btn("Selecione a MSP","#F5F5F5","#000000","5px","#D4D4D4",170,30)
        self.card_tecnico.add_component_card(btn2_tec)
        self.card_tecnico.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha MSP. \n2. Selecione o EXP de campus.\n3.Clique em 'Gerar'\n\n*IMPORTANTE: Certifique-se de selecionar na ordem correta, conforme instruções*")
        self.card_tecnico.set_action_btn("btn_generate",self.process_tec)

        self.card_pos = Card("pos-grad","#FF7E29")
        self.card_pos.create_front_card("Cruzeiro Pós-Grad","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione Relação Polos")
        self.card_pos.create_back_card("#FF7E29","Para a verificação e preenchimento correto siga as instruções: \n1. Selecione a planilha de Ofertas. \n2. Selecione o EXP de campus.\n3.Selecione a relação de Polos. \n4.Clique em 'Gerar'\n5.Selecione diretório que deseja salvar \n6.Preencha todos os campos solicitados e clique em 'OK'\n*IMPORTANTE: Certifique-se de selecionar na ordem correta*")
        btn2_pos = self.card_pos.create_btn("Selecione o EXP","#F5F5F5","#000000","5px","#D4D4D4",170,30)
        self.card_pos.add_component_card(btn2_pos)
        btn3_pos = self.card_pos.create_btn("Selecione Planilha ofertas","#F5F5F5","#000000","5px","#D4D4D4",170,30)
        self.card_pos.add_component_card(btn3_pos)
        self.card_pos.set_action_btn("btn_generate",self.process_pos)


        self.add_card(self.card_tecnico,"TOP")
        self.add_card(self.card_pos,"TOP")

    def process_tec(self):
            if self.card_tecnico.paths["btn_option1"] and self.card_tecnico.paths["btn_option2"]:
                try:
                    msp = self.card_tecnico.paths["btn_option2"]
                    exp = self.card_tecnico.paths["btn_option1"]
                    tecnico = tecnicoCruzeiro(msp,exp)
                    self.card_tecnico.set_save_manager("btn_generate")
                    path_save = self.card_tecnico.paths["save"]
                    if not path_save:
                     Notification.error("DIretório inválido","Erro ao tentar gerar planilha final. Diretório não selecionado ou inválido. Execute a operação novamente, selecionando um diretório válido.")
                    else:
                        tecnico.load(path_save)
                        Notification.info("Operação finalizada","Planilha gerada com sucesso.")
                    self.card_tecnico.set_text_btns(["btn_option1","btn_option2"])
                except Exception as e:
                     Notification.error("Arquivos incorretos",f"Erro ao tentar gerar planilha final. Verificar arquivos selecionados e ordem de seleção \n {e}")    
            else:
                 Notification.error("Arquivos não selecionados","Necessário selecionar os arquivos para execução da operação. Tente novamente após selecioná-los")

    def process_pos(self):
            if self.card_pos.paths["btn_option1"] and self.card_pos.paths["btn_option2"] and self.card_pos.paths["btn_option3"]:
                try:
                    msp = self.card_pos.paths["btn_option3"]
                    exp = self.card_pos.paths["btn_option2"]
                    relation = self.card_pos.paths["btn_option1"]
                    pos = PosGradEadCruzeiro(msp,exp,relation)
                    self.card_pos.set_directory("btn_generate")
                    path_save = self.card_pos.paths["save"]
                    pos.load()
                    values = Notification.get_user_input()
                    if values:
                        end,osc,semester = values
                        pos.set_values_missing_in_msp(end,osc,semester)
                        pos.save(path_save)
                    else:
                         Notification.error("Erro ao carregar planilha, verifique as informações passsadas e tente novamente.")

                    Notification.info("Operação finalizada","Planilha gerada com sucesso.")
                    self.card_pos.set_text_btns(["btn_option1","btn_option2","btn_option3"])
                except Exception as e:
                    Notification.error("Erro interno", f"Erro ao tentar gerar planilha final.\nDetalhes: {e}")
                    
            else:
                 Notification.error("Arquivos não selecionados","Necessário selecionar os arquivos para execução da operação. Tente novamente após selecioná-los")