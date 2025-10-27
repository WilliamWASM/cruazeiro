from ..views.cards.base_card import *
from ..managers.file_manager import FileManager
import os 
from functools import partial
class CardController():
    def __init__(self,card : BaseCard):
        self.card = card
        self.components = self.card.get_front_components()
        self.default_values_buttons = {}

        self.flip_btn_front = self.card.get_front_button_flip()
        self.flip_btn_back = self.card.get_back_button_flip()
        
        self.flip_btn_front.clicked.connect(self.card.flip)
        self.flip_btn_back.clicked.connect(self.card.flip)

        self.selector_buttons = self.card.front.get_selector_buttons()
        for button in self.selector_buttons:
            button.clicked.connect(partial(self.get_selection, button))

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

