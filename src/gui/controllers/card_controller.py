from ..views.cards.base_card import *
class CardController():
    def __init__(self,card : BaseCard):
        self.card = card
        self.components = self.card.get_front_components()

        self.flip_btn_front = self.card.get_front_button_flip()
        self.flip_btn_back = self.card.get_back_button_flip()
        
        self.flip_btn_front.clicked.connect(self.card.flip)
        self.flip_btn_back.clicked.connect(self.card.flip)