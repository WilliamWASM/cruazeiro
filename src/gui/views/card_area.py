from qt_core import *
class CardArea(QWidget):
    def __init__(self):
        super().__init__()
        self.added_cards = 0
        self.cards = {}
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setSpacing(0)
        self.card_layout.setContentsMargins(0,0,0,0)

        self.top_area = QWidget()
        self.top_layout = QHBoxLayout(self.top_area)
        self.top_layout.setSpacing(50)
        self.top_layout.setContentsMargins(30,10,30,0)
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.bottom_area = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom_area)
        self.bottom_layout.setSpacing(20)

        self.card_layout.addWidget(self.top_area,1)
        self.card_layout.addWidget(self.bottom_area,1)

    def add_card(self, card):
        if self.added_cards < 3:
            self.top_layout.addWidget(card)
        else:
            self.bottom_layout.addWidget(card)
        self.cards[card] = card
        self.added_cards += 1
    
    def get_cards(self):
        return self.cards
    
    def set_style(self,style):
        self.setStyleSheet(style)