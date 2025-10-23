from ..views.main_window import *
from .menu_bar_controller import *
from .project_controller import *
from ..views.menu_item import *
from ...resources.styles.theme_manager import *
from src.config.configurations import PROJECT_CONFIGS, PROJECT_STYLES
class MainWindowController():
    def __init__(self,main_window: MainWindow):
        self.projects = PROJECT_CONFIGS.keys()
        self.projects_configs = PROJECT_CONFIGS
        self.project_styles = PROJECT_STYLES
        self.main_window = main_window
        self.project_components = {}
        self.project_controllers ={}
        self.card_area_index = {}

        self.menu_bar_controller = MenuBarController(self.main_window.menu_bar, self.projects)

        self.theme_manager = ThemeManager()
        current_theme = self.theme_manager.current_theme
        initial_style = self.project_styles['SiteOps'][current_theme]

        self.main_window.menu_bar.toggle_mode.toggled.connect(self.on_theme_toggled)

        self.main_window.menu_bar.set_default_area_style(initial_style.default_menu_area())
        
        self.main_window.menu_bar.cbox_projects.currentIndexChanged.connect(self.update_project_style)
        self.main_window.menu_bar.cbox_projects.currentIndexChanged.connect(
            lambda _: self.main_window.content_layout.setCurrentIndex(self.main_window.get_home_index())
        )

        self.create_projects()
        self.create_menu_items()
        self.build_card_areas()
        self.connect_home_button()
        self.connect_menu_items()
        self.apply_object_name_and_styles()

        # -- CREATION ON BASE COMPONENTS AND WINDOWS IN THE PROJECTS --

    def create_projects(self):
        for project in self.projects:
            controller = ProjectController(project, self.projects_configs[project])
            self.project_components[project] = {
                "project_contents": controller.project_contents,
                "card_controllers": controller.card_controllers,
                "menu_items" : None
            }
            self.project_controllers[project] = controller

    def create_menu_items(self):
        for project_name,menu_items in self.projects_configs.items():
            menus_to_add = []
            for section_name in menu_items:
                menu_create = MenuItem(section_name)
                menu_create.setProperty("project", project_name)
                menus_to_add.append(menu_create)                

            self.project_components[project_name]["menu_items"] = menus_to_add
            self.menu_bar_controller.add_menu_items(menus_to_add,project_name)

    def build_card_areas(self):
        for project,controller in self.project_controllers.items():
            for menu_item,card_area in controller.get_card_areas().items():
                index = self.main_window.content_layout.addWidget(card_area)
                key = f"{project}_{menu_item}"
                self.card_area_index[key] = index

        # -- CONNECT ACTIONS IN MENU BAR COMPONENTS --

    def connect_home_button(self):
        home_btn = self.main_window.menu_bar.get_home_button()
        home_index = self.main_window.get_home_index()

        home_btn.clicked.connect(
        lambda: self.select_menu_item(None, [])  
        )
        home_btn.clicked.connect(
            lambda: self.main_window.content_layout.setCurrentIndex(home_index)
        )

    def connect_menu_items(self):
        for project_name, menu_items in self.project_components.items():
            for menu_item in menu_items["menu_items"]:
                section_name = menu_item.lbl_text.text() 
                key = f"{project_name}_{section_name}"
                index = self.card_area_index.get(key)
                if index is not None:
                    menu_item.clicked.connect(
                        lambda i=index: self.main_window.content_layout.setCurrentIndex(i)
                    )

        # -- APPLY/RE-APPLY STILIZATION AND THEME --

    def apply_object_name_and_styles(self):
        current_theme = self.theme_manager.current_theme
        for project,components in self.project_components.items():
            style_class = self.project_styles[project][current_theme]

            card_areas = self.project_controllers[project].get_card_areas()
            menu_items = components["menu_items"]

            self.main_window.menu_bar.set_style_project_area(project,style_class.project_menu_area())
            for section_name,card_area in card_areas.items():
                card_area.set_style(style_class.card_area()) 
                cards = self.project_controllers[project].get_cards(section_name)   
                for card in cards: 
                    card.set_style_front_card(style_class.card()) 
                    card.set_style_back_card(style_class.card()) 
            for menu in menu_items:
                menu.set_styles(style_class.menu_item())
                menu.clicked.connect(lambda checked=False, m=menu: self.on_menu_clicked(m))
                
    def on_theme_toggled(self, checked):
        self.theme_manager.toggle_theme()
        self.reapply_all_styles()

    def reapply_all_styles(self):
        self.apply_object_name_and_styles()  
        self.update_project_style() 
        
    def update_project_style(self):
        self.deselect_current_project_menus()
        project = self.main_window.menu_bar.cbox_projects.currentText()
        current_theme = self.theme_manager.current_theme

        style_class = self.project_styles[project][current_theme]
        self.main_window.menu_bar.set_default_area_style(style_class.default_menu_area())

    def deselect_current_project_menus(self):
        current_project = self.main_window.menu_bar.cbox_projects.currentText()
        if current_project in self.project_components:
            menu_items = self.project_components[current_project]["menu_items"]
            for menu in menu_items:
                menu.set_selected(False)
    
    def on_menu_clicked(self, clicked_menu):
        project = clicked_menu.property("project")
        menu_items = self.project_components[project]["menu_items"]
        
        self.select_menu_item(clicked_menu, menu_items) 

    def select_menu_item(self, clicked_menu, menu_items):
        if clicked_menu is None:
            for project, components in self.project_components.items():
                for menu in components["menu_items"]:
                    menu.set_selected(False)
            return
        for menu in menu_items:
            if menu == clicked_menu:
                menu.set_selected(True)
            else:
                menu.set_selected(False)