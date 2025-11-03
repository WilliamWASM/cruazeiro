from ..views.cards.base_card import *
from ..managers.file_manager import FileManager
import os 
from functools import partial
from ..views.notifications import *
from ...workers.card_action_worker import *
class CardController():
    def __init__(self,card : BaseCard,action_config: dict):
        self.card = card
        self.components = self.card.get_front_components()
        self.default_values_buttons = {}
        self.action_config = action_config


        self.selector_buttons = self.card.front.get_selector_buttons()
        for button in self.selector_buttons:
            button.clicked.connect(partial(self.get_selection, button))

        self.flip_btn_front = self.card.get_front_button_flip()
        self.flip_btn_back = self.card.get_back_button_flip()
        
        self.flip_btn_front.clicked.connect(self.card.flip)
        self.flip_btn_back.clicked.connect(self.card.flip)

        self.card.front.generate_btn.clicked.connect(self.on_clicked_generate)

    def get_selection(self,button):
        file_path = FileManager.select_file(self.card)

        if file_path:
            self.card.front.set_path_for_button(button,file_path)
            button.setText(os.path.basename(file_path))
        else:
            self.card.front.set_path_for_button(button,None)
            button.setText(self.default_values_buttons.get(button,"Selecionar arquivo"))
    
    def set_default_values(self,values: list):
        for button,value in zip(self.selector_buttons,values):
            self.default_values_buttons[button] = value
            button.setText(value)

    def on_clicked_generate(self):
        if not self.card.front.verify_all_paths_selected():
            Notification.error("Erro", "Selecione todos os arquivos antes de gerar.")
            return
        
        paths = self.card.front.get_paths()
        data = {"paths": paths}
        
        require_input = self.action_config.get("requires_input", False)
        if require_input:
            inputs = self.action_config.get("user_inputs", [])
            user_inputs = self.get_user_inputs(inputs, "Entradas Necessárias")
            if not user_inputs:
                Notification.error("Cancelado", "Processo cancelado pelo usuário.")
                return
            data["user_inputs"] = user_inputs
            
        save_type = self.action_config.get("save_type","save_file")
        if save_type == "directory":
            save_path = FileManager.select_directory(self.card)
        elif save_type == "save_file":
            save_path = FileManager.save_file(self.card)
        else:
            Notification.error("Erro ao processar solicitação", f"Tipo de salvamento desconhecido: {save_type}")
            return
        
        if not save_path:
            Notification.error("Cancelado", "Processo cancelado pelo usuário.")
            return
            
        data["save_path"] = save_path
        
        generate_action = self.action_config.get("generate_action")

        worker = CardActionWorker(func=generate_action, data=data, parent=self.card)

        def after_finished():
            self.set_default_values(list(self.default_values_buttons.values()))
            worker.show_result_notification()

        worker.dialog.finished.connect(after_finished)
        worker.run()

    def get_user_inputs(self,fields: list, title="Entradas do Usuário"):
        return Notification.get_inputs(fields,title,self.card)
