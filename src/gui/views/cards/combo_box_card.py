from qt_core import *
from .base_card import *
class ComboBoxCard(BaseCard):
    def __init__(self, title,items: list, description=""):
        self.items = items
        self.title = title
        self.description = description
        super().__init__(title,description)

        self.combo_box = QComboBox()
        self.combo_box.addItems(items)
        self.front.add_content(self.combo_box)
        self.front.redefine_component_order([self.combo_box, self.select_btn])

    def get_selected_value(self):
        return self.combo_box.currentText()