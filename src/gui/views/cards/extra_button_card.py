from qt_core import *
from .base_card import *
class ExtraButtonCard(BaseCard):
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        super().__init__()

        self.extra_btn = QPushButton("Selecionar arquivo")
        self.front.add_content(self.extra_btn)