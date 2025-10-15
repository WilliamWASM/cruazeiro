from qt_core import *

class FrontCard(QFrame):
    def __init__(self,title):
        super().__init__()
        self.title = title
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(0,0,0,0)
        self.card_layout.setSpacing(0) 
        self.components = {}
        self.default_buttons = []

        self.top_content = QWidget()
        self.top_content_layout = QHBoxLayout(self.top_content)
        self.top_content_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.top_content_layout.setSpacing(20)
        self.top_content_layout.setContentsMargins(0, 0, 20, 0)
        self.title_card = QLabel(title)
        self.info_btn = QPushButton("i")
        self.info_btn.setFixedSize(25,25)
        self.top_content_layout.addWidget(self.title_card)
        self.top_content_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.top_content_layout.addWidget(self.info_btn)
        

        self.contents_area = QWidget()
        self.contents_layout = QVBoxLayout(self.contents_area)
        self.contents_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        self.contents_layout.setSpacing(15)

        self.generate_btn_area = QWidget()
        self.generate_btn_layout = QHBoxLayout(self.generate_btn_area)
        self.generate_btn_area.setFixedHeight(50)
        self.generate_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter )
        self.generate_btn_layout.setContentsMargins(0,0,0,10)
        self.generate_btn = QPushButton("Gerar")
        self.generate_btn_layout.addWidget(self.generate_btn)
        self.generate_btn.setFixedSize(220,35)
        self.card_layout.addWidget(self.top_content,1)
        self.card_layout.addWidget(self.contents_area,3)
        self.card_layout.addWidget(self.generate_btn_area,2)

        self.default_buttons.append(self.generate_btn)
        self.default_buttons.append(self.info_btn)
    
    def add_content(self, widget):
        widget.setFixedSize(220,35)
        self.contents_layout.addWidget(widget)
        self.components[widget] = None

    def redefine_component_order(self,new_order: list):
        for component in new_order:
            if component in self.components:
                self.contents_layout.removeWidget(component)
                self.contents_layout.addWidget(component)
    
    def get_components(self):
        return self.components
    
    def get_flip_button(self):
        return self.info_btn
    
    def get_default_buttons(self):
        return self.default_buttons