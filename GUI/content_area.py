from GUI.qt_core import *

class ContentArea(QFrame):
    def __init__(self,color,type = "HBox"):
        super().__init__()
        self.setStyleSheet(f"background-color: {color};")
        if type == "HBox":
            self.content = QHBoxLayout()
        else:
            self.content = QVBoxLayout()

        self.setLayout(self.content)
        
    def set_cards_area(self,color,layout_to_add):
        top = ContentArea(color,"HBox")
        top.setMinimumHeight(325)
        self.top_layout = top.layout()
        self.top_layout.setContentsMargins(80,0,0,0)
        self.top_layout.setSpacing(80)
        self.top_layout.setAlignment(Qt.AlignLeft)

        bottom =ContentArea(color,"HBox")
        bottom.setMinimumHeight(325)
        self.bottom_layout = bottom.layout()
        self.bottom_layout.setContentsMargins(80,0,0,0)
        self.bottom_layout.setSpacing(80)
        self.bottom_layout.setAlignment(Qt.AlignLeft)     
        layout_to_add.addWidget(top)
        layout_to_add.addWidget(bottom)

    def add_card(self,card,frame_to_add):
        if frame_to_add == "TOP":
            frame = self.top_layout
        elif frame_to_add == "BOTTOM":
            frame = self.bottom_layout
        else:
            frame = None
        
        if frame is not None:
            frame.addWidget(card)

    def get_content_areas(self):
        areas = [self.top_layout,self.bottom_layout]
        return areas