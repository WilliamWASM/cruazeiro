from qt_core import *
class BackCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.top_content = QWidget()
        self.top_content_layout = QHBoxLayout(self.top_content)
        self.top_content_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.title_card = QLabel(title)
        self.title_card.setProperty("label","title_card")
        self.title_card.setWordWrap(True)
        self.title_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.title_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_btn = QPushButton("X")
        self.info_btn.setFixedSize(25,25)
        self.top_content_layout.addWidget(self.title_card)
        self.top_content_layout.addWidget(self.info_btn)

        self.bottom_content = QWidget()
        self.bottom_content_layout = QVBoxLayout(self.bottom_content)
        self.bottom_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_descript = QScrollArea()
        self.scroll_descript.setWidgetResizable(True)   
        self.scroll_descript.setWidget(self.bottom_content)

        self.card_layout.addWidget(self.top_content,1)
        self.card_layout.addWidget(self.scroll_descript,3)
    
    def get_flip_button(self):
        return self.info_btn

    def set_description(self,description):
        self.description = description
        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet('font-size: 14px;')
        self.bottom_content_layout.addWidget(self.desc_label)
        
