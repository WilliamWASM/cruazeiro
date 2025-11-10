from qt_core import *
from .toggle_button import *
class MenuBar(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_bar = QVBoxLayout(self)
        self.layout_bar.setContentsMargins(0,0,0,0)
        self.layout_bar.setSpacing(0)
        self.setFixedWidth(200)

        self.project_items = {}

        # -- default area content --
        self.default_content = QWidget()
        self.default_layout = QVBoxLayout(self.default_content)
        self.default_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.default_layout.setSpacing(0)

        # -- default components --
        self.menu_widget = QWidget()
        self.menu_widget.setFixedHeight(50)
        self.menu_layout_top = QHBoxLayout(self.menu_widget)
        self.menu_layout_top.setContentsMargins(0,0,0,0)
        self.menu_layout_top.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.btn_menu = QPushButton()
        self.btn_menu.setIcon(QIcon("src/resources/icons/Menu_icon.png"))
        self.btn_menu.setIconSize(QSize(24, 24))
        self.btn_menu.setFixedHeight(46)
        self.btn_menu.setMaximumWidth(88)

        self.toggle_container = QWidget()
        self.toggle_container.setMaximumWidth(90)
        self.toggle_container.setFixedHeight(30)
        self.toggle_layout = QHBoxLayout(self.toggle_container) 
        self.toggle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toggle_layout.setContentsMargins(3,0,18,0)
        self.toggle_mode = ToggleButton(
        )
        self.toggle_mode.setMinimumWidth(60) 
        self.toggle_mode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.home_bar = QWidget()
        self.home_bar.setFixedHeight(50)
        self.home_layout = QHBoxLayout(self.home_bar)
        self.home_layout.setContentsMargins(0,0,0,0)
        self.btn_home = QPushButton()
        self.btn_home.setIcon(QIcon("src/resources/icons/Home_icon.png"))
        self.btn_home.setIconSize(QSize(24, 24)) 
        self.btn_home.setFixedHeight(46)

        self.cbox_projects = QComboBox()

        # -- menu items from project area --
        self.menu_area = QWidget()
        self.menu_layout = QStackedLayout(self.menu_area)
        
        self.menu_layout.setCurrentIndex

        self.default_widgets = {
            "btn_menu": self.btn_menu,
            "btn_home": self.btn_home,
            "cb_box_projects": self.cbox_projects,
            "default_area": self.default_content
        }

        self.layout_bar.addWidget(self.default_content)
        self.layout_bar.addWidget(self.menu_area)
        self.menu_layout_top.addWidget(self.btn_menu)
        self.toggle_layout.addWidget(self.toggle_mode)
        self.menu_layout_top.addWidget(self.toggle_container)
        self.default_layout.addWidget(self.menu_widget)
        self.default_layout.addWidget(self.home_bar)
        self.home_layout.addWidget(self.btn_home)
        self.home_layout.addWidget(self.cbox_projects)

    def add_menu_item(self,item,project_name):
        self.project_items[project_name]["layout"].addWidget(item)
        self.project_items[project_name]["items"].append(item)

    def create_project_menu(self,project_name):
        project_menu = QWidget()
        project_layout = QVBoxLayout(project_menu)
        project_layout.setContentsMargins(0,0,0,0)
        project_layout.setSpacing(0)
        project_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.project_items[project_name] = {
            "widget" : project_menu,
            "layout": project_layout,
            "stack_index" : self.menu_layout.addWidget(project_menu),
            "items" : []
        }
        project_menu.setProperty("project_menu", project_name)

        self.cbox_projects.addItem(project_name)

    def get_menu_button(self):
        return self.btn_menu

    def get_home_button(self):
        return self.btn_home
    
    def get_widgets_to_animate(self):
        return self.toggle_container,self.cbox_projects
    
    def set_default_area_style(self,style):
        self.default_content.setStyleSheet(style)

    def set_style_project_area(self,project,style):
        self.project_items[project]['widget'].setStyleSheet(style)
