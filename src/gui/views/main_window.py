from qt_core import *
from .menu_bar import *
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SiteOps - Echo")
        screens = QApplication.screens()

        if len(screens) > 1:
            screen = screens[0]
        else:
            screen = QApplication.primaryScreen()

        avaiable_geometry = screen.availableGeometry()

        width = int(avaiable_geometry.width() * 0.7)
        height = int(avaiable_geometry.height() * 0.85)

        self.resize(width,height)

        screen_geometry = screen.geometry()

        x = screen_geometry.left() + (screen_geometry.width() - width) // 2
        y = screen_geometry.top() + (screen_geometry.height() - height) // 2
        self.move(x, y)

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0) 

        #Area de conteudo central
        self.content_area = QWidget()
        self.content_layout = QStackedLayout(self.content_area) 

        self.menu_bar = MenuBar()

        self.central_layout.addWidget(self.menu_bar)
        self.central_layout.addWidget(self.content_area)  

        # -- content to home button -- 
        self.home_area = QWidget()
        self.home_layout = QVBoxLayout(self.home_area)

        self.version_app = QLabel()
        self.title_feature = QLabel("Oque há de Novo:")
        self.features_text = QLabel()
        self.title_help = QLabel("Ficou com dúvidas?")
        self.help_section = QLabel()

        self.home_layout.addWidget(self.version_app)
        self.home_layout.addWidget(self.title_feature)
        self.home_layout.addWidget(self.features_text)
        self.home_layout.addWidget(self.title_help)
        self.home_layout.addWidget(self.help_section)

        self.home_index = self.set_central_content(self.home_area)

    def set_central_content(self, widget):
        index = self.content_layout.addWidget(widget)
        return index
    
    def get_home_index(self):
        return self.home_index