from qt_core import *
from .base_card import *
class TripleButtonCard(BaseCard):
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        super().__init__(title, description)

        self.second_btn = QPushButton("Selecionar arquivo")
        self.third_btn = QPushButton("Selecionar arquivo")
        self.front.add_content(self.second_btn)
        self.front.add_content(self.third_btn)