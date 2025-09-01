from GUI.qt_core import *
import os
import sys
class MenuBar(QFrame):
    def __init__(self,color,width,layout_to_set,btn_text_color,bg_color,txt_pad,bg_hover,border_color):
        super().__init__()
        self.setStyleSheet(f"background-color: {color};")
        self.setMaximumWidth(width)
        self.content = QVBoxLayout(self)
        self.content.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_to_set.addWidget(self)
        self.content.setContentsMargins(0,20,0,0)
        self.content.setSpacing(0)
        self.group = QButtonGroup()
        self.group.setExclusive(True)
        self.buttons = {}

        self.style_btn = f"""
                QPushButton {{
                    color: {btn_text_color};
                    background-color: {bg_color};
                    padding-left: {txt_pad};
                    text-align: left;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {bg_hover};
                }}
                QPushButton:pressed {{
                    background-color: {bg_hover};
                }}
            """
        self.pressed = f"""
                QPushButton {{
                    background-color: {bg_hover};
                    border-right: 5px solid {border_color};
                }}
            """
    
    def add_sub_menu_button(self,text,icon_path):

        btn_frame = QFrame()
        btn_frame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        btn_frame.setFixedHeight(40)
        layout_frame = QVBoxLayout(btn_frame)
        layout_frame.setContentsMargins(0,0,0,0)
        layout_frame.setSpacing(0)
        button = QPushButton(text)
        font = QFont("Arial", 11)  
        button.setFont(font)
        icon = QIcon(resource_path(icon_path))
    
        button.setIcon((icon))
        button.setIconSize(QSize(30,30))
        button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        button.setCheckable(True)
        layout_frame.addWidget(button)
        self.group.addButton(button)
        self.content.addWidget(btn_frame)
        button.clicked.connect(self.switch_style_btns)
        self.buttons[text] = button
        return button

    def create_menu_button(self,bg_color,bg_hover,icon_path):
        
        btn_frame = QFrame()
        btn_frame.setStyleSheet(f"background-color: {bg_color}")
        btn_frame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        btn_frame.setFixedHeight(40)

        layout_frame = QVBoxLayout(btn_frame)
        layout_frame.setContentsMargins(0,0,0,0)
        layout_frame.setSpacing(0)
        button = QPushButton()
        icon = QIcon(resource_path(icon_path))
        button.setIconSize(QSize(40,40))
        button.setIcon(icon)
        button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        button.setStyleSheet(f"""
                QPushButton{{
                           background-color:{bg_color};
                           border: none;
                }} 
                QPushButton:hover{{
                    background-color:{bg_hover};
                    border: none;
                }}
        """)
        layout_frame.addWidget(button)
        button.clicked.connect(self.toggle_button)
        self.content.addWidget(btn_frame)

    def toggle_button(self):
        self.menu_width = self.width()
        width = 100

        if self.menu_width == 100:
            width = 200

        self.animation = QPropertyAnimation(self,b"minimumWidth")
        self.animation.setStartValue(self.menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def switch_style_btns(self):
        for button in self.group.buttons():
            if button.isChecked():
                button.setStyleSheet(self.style_btn + self.pressed)
                button.setEnabled(False)
            else:
                button.setStyleSheet(self.style_btn)
                button.setEnabled(True)

    def start_selected_button(self,button):
        button.setChecked(True)
        self.switch_style_btns()

    
    def get_sub_menu_buttons(self):
        return self.buttons
    
    def set_action(self,button,action):
        button.clicked.connect(action)

def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS 
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)