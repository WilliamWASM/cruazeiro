from qt_core import *
from pathlib import Path
class MenuItem(QFrame):
    clicked = Signal()
    def __init__(self,text_item):
        super().__init__()
        self.selected = False
        self.styles = None
        self.text = text_item
        self.item_layout = QHBoxLayout(self)
        self.item_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setAttribute(Qt.WA_Hover)

        self.icon = QLabel()
        self.icon.setFixedSize(57,35)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_text = QLabel(self.text)
        self.lbl_text.setFixedHeight(35)
        self.lbl_text.setFixedWidth(100)

        self.item_layout.addWidget(self.icon)
        self.item_layout.addWidget(self.lbl_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit() 
        super().mousePressEvent(event)

    def get_text_item(self):
        return self.text
    
    def enterEvent(self, event):
        if not self.selected and self.styles:
            self.setStyleSheet(self.styles['hover'])
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.selected and self.styles:
            self.setStyleSheet(self.styles['default'])
        super().leaveEvent(event)

    def set_selected(self,value):
        self.selected = value
        if self.selected:
            self.setStyleSheet(self.styles['selected'])
        else:
            self.setStyleSheet(self.styles['default'])

    def set_styles(self,menu_item: dict):
        self.styles = menu_item

        if not self.selected:
            self.setStyleSheet(self.styles['default'])

    def set_icon(self,name_icon):
        icon_path = Path(__file__).resolve().parent.parent.parent / "resources" / "icons" / f"{name_icon}.png"
        pixmap = QPixmap(str(icon_path))
        self.icon.setPixmap(pixmap.scaled(self.icon.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))