from GUI.content_area import *
from GUI.widgets.cards import *
from GUI.widgets.notifications import *
from MODELS.unifatecie import *


class Universities(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)
        
        self.unifatecie = Card("unifatecie","#FF7E29")
        self.unifatecie.create_front_card("Unifatecie","#FF7E29","#F5F5F5","#000000","#D4D4D4","#8148C9","#F5F5F5","#7D3FC9","Selecione a planilha")
        self.unifatecie.set_action_btn("btn_generate", self.process_unifatecie)    

        self.add_card(self.unifatecie,"TOP")

    def process_unifatecie(self):
        if self.unifatecie.paths["btn_option1"]:
            try:
                offers = self.unifatecie.paths["btn_option1"]
                self.unifatecie.set_save_manager("btn_generate")
                path_save = self.unifatecie.paths["save"]
                unifatecie = Unifatecie(offers)
                values = Notification.get_date_and_osc()
                if values:
                    end,osc = values
                    unifatecie.set_values(end,osc)
                    unifatecie.load(path_save)
                else:
                        Notification.error("Erro ao carregar planilha, verifique as informações passsadas e tente novamente.")

                Notification.info("Operação finalizada","Planilha gerada com sucesso.")
                self.unifatecie.set_text_btns(["btn_option1"])
            except Exception as e:
                Notification.error("Erro interno", f"Erro ao tentar gerar planilha final.\nDetalhes: {e}")     
        else:
                Notification.error("Arquivos não selecionados","Necessário selecionar os arquivos para execução da operação. Tente novamente após selecioná-los")