import sys
from GUI.qt_core import *
from GUI.content_area import *
from GUI.menu_bar import *
from GUI.view.home import *
from GUI.view.cruzeiro import *
from GUI.view.utilities import *
from GUI.menu_bar import *

class MainWindow(QMainWindow):
    def __init__(self):      
        super().__init__()
        #seta um frame principal
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet("background-color: #FFFFFF")
        self.setCentralWidget(self.main_frame)
        #seta gerenciador de layout horizontal no frame principal
        self.main_layout = QHBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.home = Home()
        self.cruzeiro = CruzeiroDoSul()
        self.utilites = Utilities()

        self.setWindowIcon(QIcon(resource_path("ASSETS/ICONS/app_icon.ico")))


        #cria e seta o menu_bar
        self.menu_bar = MenuBar("#FF7E29",100,self.main_layout,"#F5F5F5","#FF7E29",33,"#FA9653","#F5F5F5")
        self.menu_bar.create_menu_button("#FF7E29","#FA9653","ASSETS/ICONS/menu_icon.png")
        self.home_btn = self.menu_bar.add_sub_menu_button("        Home","ASSETS/ICONS/home_icon.png")
        self.config = self.menu_bar.add_sub_menu_button("        Cruzeiro","ASSETS/ICONS/cruzeiro_icon.png")
        self.utilites_btn = self.menu_bar.add_sub_menu_button("        Utilities","ASSETS/ICONS/utilities_icon.png")
        self.menu_bar.start_selected_button(self.home_btn)
        self.buttons = self.menu_bar.get_sub_menu_buttons()

        #cria e seta o frame central
        self.central_frame = QWidget()
        self.stacks = QStackedLayout(self.central_frame)

        self.stacks.addWidget(self.home)
        self.stacks.addWidget(self.cruzeiro)
        self.stacks.addWidget(self.utilites)

        self.main_layout.addWidget(self.central_frame)

        self.menu_bar.set_action(self.home_btn,lambda: self.stacks.setCurrentIndex(0))
        self.menu_bar.set_action(self.config,lambda: self.stacks.setCurrentIndex(1))
        self.menu_bar.set_action(self.utilites_btn,lambda: self.stacks.setCurrentIndex(2))

        self.show()

    def setup_config(self,width,height,min_res_width,min_res_heigth,name = "Default Window"):
        self.setObjectName(name)
        self.resize(width, height)
        self.setMinimumSize(min_res_width, min_res_heigth)




    


