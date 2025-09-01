from GUI.content_area import *
from GUI.widgets.cards import *

class Home(ContentArea):
    def __init__(self):
        super().__init__("#F5F5F5","VBox")
        self.set_cards_area("#F5F5F5",self.content)
        areas = self.get_content_areas()
        top = areas[0]
        lbl_home = QLabel("Seja bem vindo!")
        lbl_home.setStyleSheet("font-size: 30px; font-weight: bold; color: #000000")
        top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top.addWidget(lbl_home)
        