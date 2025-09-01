from GUI.qt_core import *
import os

class Card(QFrame):
    def __init__(self,name_card,bg_color):
        super().__init__()
        self.name_card = name_card
        self.layout_card = QStackedLayout(self)
        self.setStyleSheet(f"background-color: {bg_color}; border-radius: 30px;")
        self.setFixedSize(220,300)
        self.card_components = {
            self.name_card: {
                "front":{
                    "title": None,
                    "btn_info":None,
                    "btn_option1": None,
                    "btn_option2": None,
                    "btn_option3": None,
                    "combo_box": None,
                    "btn_generate": None
                },
                "back": {
                    "description": None,
                    "btn_close": None
                }
            }
        }
        self.paths = {
            "btn_option1": None,
            "btn_option2": None,
            "btn_option3": None,
            "save": None
        }
        self.text_buttons = {
            "btn_option1": None,
            "btn_option2": None,
            "btn_option3": None
        }

    def base_card(self,bg_color): 
        card_frame = QFrame()
        card_frame.setStyleSheet(f"background-color: {bg_color}; border-radius: 30px;")
        card_frame.setFixedSize(220,300)
        layout_gerenc = QVBoxLayout(card_frame)
        layout_gerenc.setSpacing(0)
        #frames superior e inferior
        top_frame = QFrame()
        bottom_frame = QFrame()
        #layout sup e inf
        top_layout = QVBoxLayout(top_frame)
        top_layout.setAlignment(Qt.AlignTop)
        top_layout.setSpacing(10)
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom )
        bottom_layout.setSpacing(12)
        layout_gerenc.addWidget(top_frame)
        layout_gerenc.addWidget(bottom_frame)
        return [top_layout, bottom_layout,top_frame,bottom_frame,card_frame]

    def create_front_card(self,title,bg_color_card,btn_opt_color,color_opt_name,color_hover_opt,btn_gnrt_color,color_gnrt_name,color_hover_gnrt,text_btn_select):
        base_card = self.base_card(bg_color_card)
        top_layout = base_card[0]
        self.bottom_layout_front = base_card[1]
        btn_info = self.create_btn("i","#FF7E29","#F5F5F5","10px","#CCCCCC",20,20,"circular","#F5F5F5")
        btn_opt1 = self.create_btn(text_btn_select,btn_opt_color,color_opt_name,"5px",color_hover_opt,170,30)
        self.text_buttons["btn_option1"] = text_btn_select
        btn_generate = self.create_btn("Gerar",btn_gnrt_color,color_gnrt_name,"5px",color_hover_gnrt,170,50)
        name_label = QLabel(title)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #F5F5F5")
        name_label.setFixedHeight(30)
        self.card_components[self.name_card]["front"].update({
            "title": name_label,
            "btn_option1": btn_opt1,
            "btn_generate": btn_generate,
            "btn_info": btn_info
        })
        self.set_action_btn("btn_option1",lambda: self.set_selector_manager("btn_option1"))
        self.set_action_btn("btn_option1",lambda: self.switch_text_btn("btn_option1"))
        self.layout_card.addWidget(base_card[4])
        self.set_action_btn("btn_info",lambda: self.set_card_visible("back"))
        top_layout.addWidget(btn_info)
        top_layout.addWidget(name_label)
        self.bottom_layout_front.addWidget(btn_opt1)
        self.bottom_layout_front.addWidget(btn_generate)

    def create_back_card(self,bg_color_card,description):
        base_card = self.base_card(bg_color_card)
        frame_top = base_card[2]
        frame_bottom = base_card[3]
        frame_top.setFixedSize(200,40)
        frame_bottom.setContentsMargins(0,10,0,0)
        top_layout = base_card[0]
        bottom_layout = base_card[1]
        top_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        bottom_layout.setAlignment( Qt.AlignmentFlag.AlignTop)
        btn_close = self.create_btn("X","#FF7E29","#F5F5F5","10px","#CCCCCC",20,20,"circular","#F5F5F5")
        descript_lbl = QLabel(description)
        descript_lbl.setWordWrap(True)
        descript_lbl.setAlignment(Qt.AlignmentFlag.AlignTop )
        descript_lbl.setFixedSize(193,240)
        descript_lbl.setStyleSheet(
            "font: 13px Calibri bold; color: #F5F5F5;"
        )
        self.card_components[self.name_card]["back"].update({
            "description": description,
            "btn_close": btn_close,
        })
        self.set_action_btn("btn_close",lambda: self.set_card_visible("front"),"back")
        bottom_layout.addWidget(descript_lbl)
        top_layout.addWidget(btn_close)
        self.layout_card.addWidget(base_card[4])

    def set_style_btn(self,component,bg_color,color,border,bg_hover_color,type = "selection",color_border = None):

        default = f"""
            QPushButton {{
                background-color: {bg_color};
                color: {color};
                border-radius: {border};
            }}
            QPushButton:hover {{
                background-color: {bg_hover_color};
            }}
            """
        circular = f"""
            QPushButton {{
                font-weight: 900;
                border: 2px solid {color_border};
            }}
            """
                                    
        if type == "circular":
            component.setStyleSheet(default + circular)
        else:
            component.setStyleSheet(default)
        
    def add_component_card(self,component,type= "button"):
        self.bottom_layout_front.insertWidget(0,component)
        if type == "button":
            if self.card_components[self.name_card]["front"]["btn_option2"]:
                self.card_components[self.name_card]["front"]["btn_option3"] = component
                self.set_action_btn("btn_option3",lambda: self.set_selector_manager("btn_option3"))
                self.text_buttons["btn_option3"] = component.text()
                self.set_action_btn("btn_option3",lambda: self.switch_text_btn("btn_option3"))
            else:
                self.card_components[self.name_card]["front"]["btn_option2"] = component
                self.set_action_btn("btn_option2",lambda: self.set_selector_manager("btn_option2"))
                self.text_buttons["btn_option2"] = component.text()
                self.set_action_btn("btn_option2",lambda: self.switch_text_btn("btn_option2"))
        elif type == "combobox":
            self.card_components[self.name_card]["front"]["combo_box"] = component
        else:
            print(" Erro! Type invalido")

    def create_btn(self,text,bg_color,color,border,bg_hover_color,width,height,type = "selection",color_border = None):
        button = QPushButton(text)
        self.set_style_btn(button,bg_color,color,border,bg_hover_color,type,color_border)
        button.setFixedSize(width,height)
        
        return button

    def create_combobox(self,list_itens):
        cb_box = QComboBox()
        cb_box.setFixedSize(170,22)
        cb_box.setStyleSheet("background-color: #F5F5F5")
        cb_box.addItems(list_itens)
        return cb_box

    def set_action_btn(self,btn_to_set,action,side = "front"):
        button = self.card_components[self.name_card][side][btn_to_set]
        button.clicked.connect(action)

    def set_card_visible(self,card_face):
        if card_face == "front":
            self.layout_card.setCurrentIndex(0)
        elif card_face =="back":
            self.layout_card.setCurrentIndex(1)

    def get_components(self):
        return self.card_components
    
    def get_name_card(self):
        return self.name_card
    
    def switch_text_btn(self,key_btn,side = "front"):
        button = self.card_components[self.name_card][side][key_btn]
        if self.paths[key_btn]:
            path = self.paths[key_btn]
            path = os.path.basename(path)
            button.setText(path)
        else:
            button.setText(self.text_buttons[key_btn])

    def set_save_manager(self,key_btn,side = "front"):
        button = self.card_components[self.name_card][side][key_btn]
        file_path,_ = QFileDialog.getSaveFileName(button,"Salvar arquivo ","","Arquivos Excel(*.xlsx *.csv)")
        if file_path:
            self.paths["save"] = file_path

    def set_selector_manager(self,key_btn,side = "front"):
        button = self.card_components[self.name_card][side][key_btn]
        file_path,_ = QFileDialog.getOpenFileName(button,"Selecione um arquivo ","","Arquivos Excel(*.xlsx *.csv *.xlsb)")
        if file_path:
            self.paths[key_btn] = file_path
        else:
            self.paths[key_btn] = None
    
    def set_directory(self,key_btn,side = "front"):
        button = self.card_components[self.name_card][side][key_btn]
        file_path = QFileDialog.getExistingDirectory(button, "Selecione o diretório", "", QFileDialog.ShowDirsOnly)
        if file_path:
            self.paths["save"] = file_path
        else:
            self.paths["save"] = None

    def set_text_btns(self,buttons):
        for button in buttons:
            self.card_components[self.name_card]["front"][button].setText(self.text_buttons[button])

    def get_selected_text(self):
        if self.card_components[self.name_card]["front"]["combo_box"]:
            cb_box = self.card_components[self.name_card]["front"]["combo_box"]
            return cb_box.currentText()

    