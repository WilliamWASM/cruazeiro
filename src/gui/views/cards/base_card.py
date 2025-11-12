from qt_core import *
from .front_card import *
from .back_card import *
class BaseCard(QFrame):
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        super().__init__()
        self.card_layout = QStackedLayout(self)
        self.cards_to_flip = {}
        self.create_card()

    def create_card(self):
        self.front = FrontCard(self.title)
        self.back = BackCard(self.title)
        self.back.set_description(self.description)

        self.select_btn = QPushButton("Selecionar arquivo")
        self.front.add_content(self.select_btn)

        self.cards_to_flip["front"] = self.card_layout.addWidget(self.front)
        self.cards_to_flip["back"] = self.card_layout.addWidget(self.back)
    
    def get_front_components(self):
        return self.front.get_components()

    def get_back_button_flip(self):
        return self.back.get_flip_button()
    
    def get_front_button_flip(self):
        return self.front.get_flip_button()
    
    def flip(self):
        current_index = self.card_layout.currentIndex()
        new_index = self.cards_to_flip["back"] if current_index == self.cards_to_flip["front"] else self.cards_to_flip["front"]
        self.card_layout.setCurrentIndex(new_index)

    def get_title(self):
        return self.title
    
    def set_style_front_card(self,card_style : dict):
        self.front.setStyleSheet(card_style['card'])
        default_front_btns = self.front.get_default_buttons()
        default_front_btns[0].setStyleSheet(card_style['generate_btn']) #btn generate
        default_front_btns[1].setStyleSheet(card_style['ask_button']) #btn "i"
        components = self.front.get_components()
        for component in components:
            if isinstance(component, QComboBox):
                component.setStyleSheet(card_style['combo_box'])
            else:
                component.setStyleSheet(card_style['button'])

    def set_style_back_card(self,card_style: dict):
        self.back.setStyleSheet(card_style['card'])
        self.back.get_flip_button().setStyleSheet(card_style['ask_button'])

    def set_style_titles(self,style):
        self.back.title_card.setStyleSheet(style)
        self.front.title_card.setStyleSheet(style)
