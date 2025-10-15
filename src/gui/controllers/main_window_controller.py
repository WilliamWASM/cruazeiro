from views.main_window import *
from .menu_bar_controller import *
from .project_controller import *
from views.menu_item import *
from config.configurations import PROJECT_CONFIGS, PROJECT_STYLES
class MainWindowController():
    def __init__(self,main_window: MainWindow):
        self.projects = PROJECT_CONFIGS.keys()
        self.main_window = main_window
        self.project_components = {}
        self.project_controllers ={}
        self.card_area_index = {}
        self.project_styles = PROJECT_STYLES

        self.menu_bar_controller = MenuBarController(self.main_window.menu_bar, self.projects)

        self.main_window.menu_bar.cbox_projects.currentIndexChanged.connect(
            lambda _: self.main_window.content_layout.setCurrentIndex(self.main_window.get_home_index())
        )

        self.main_window.menu_bar.set_default_area_style(self.project_styles['Siteops'].default_menu_area())

        self.main_window.menu_bar.cbox_projects.currentIndexChanged.connect(self.update_project_style)
        
        self.create_projects()
        self.create_menu_items()
        self.connect_home_button()
        self.build_card_areas()
        self.connect_menu_items()
        self.apply_object_name_and_styles()

    
    def update_project_style(self):
        project = self.main_window.menu_bar.cbox_projects.currentText()

        self.main_window.menu_bar.set_default_area_style(self.project_styles[project].default_menu_area())

    def apply_object_name_and_styles(self):
        for project,components in self.project_components.items():
            card_areas = self.project_controllers[project].get_card_areas()
            menu_items = components["menu_items"]
            self.main_window.menu_bar.set_style_project_area(project,self.project_styles[project].project_menu_area())
            for section_name,card_area in card_areas.items():
                card_area.setStyleSheet(self.project_styles[project].card_area()) 
                cards = self.project_controllers[project].get_cards(section_name)   
                for card in cards: 
                    card.set_style_front_card(self.project_styles[project].card()) 
                    card.set_style_back_card(self.project_styles[project].card()) 
            for menu in menu_items:
                menu.set_styles(self.project_styles[project].menu_item())
                menu.clicked.connect(lambda m=menu: self.select_menu_item(m, menu_items)) 

    def select_menu_item(self, clicked_menu, menu_items):
        for menu in menu_items:
            if menu == clicked_menu:
                menu.set_selected(True)
            else:
                menu.set_selected(False)

    def create_projects(self):
        for project in self.PROJECT_CONFIGS.keys():
            controller = ProjectController(project, self.PROJECT_CONFIGS[project])
            self.project_components[project] = {
                "project_contents": controller.project_contents,
                "card_controllers": controller.card_controllers,
                "menu_items" : None
            }
            self.project_controllers[project] = controller

    def create_menu_items(self):
        for project_name,menu_items in self.PROJECT_CONFIGS.items():
            menus_to_add = []
            for section_name in menu_items:
                menu_create = MenuItem(section_name)
                menus_to_add.append(menu_create)

            self.project_components[project_name]["menu_items"] = menus_to_add
            self.menu_bar_controller.add_menu_items(menus_to_add,project_name)

    def build_card_areas(self):
        for controller in self.project_controllers.values():
            for menu_item,card_area in controller.get_card_areas().items():
                index = self.main_window.content_layout.addWidget(card_area)
                self.card_area_index[menu_item] = index

    def connect_home_button(self):
        home_btn = self.main_window.menu_bar.get_home_button()
        home_index = self.main_window.get_home_index()
        home_btn.clicked.connect(
            lambda: self.main_window.content_layout.setCurrentIndex(home_index)
        )

    def connect_menu_items(self):
        for project_name, menu_items in self.project_components.items():
            for menu_item in menu_items["menu_items"]:
                section_name = menu_item.lbl_text.text() 
                index = self.card_area_index.get(section_name)
                if index is not None:
                    menu_item.clicked.connect(
                        lambda i=index: self.main_window.content_layout.setCurrentIndex(i)
                    )
