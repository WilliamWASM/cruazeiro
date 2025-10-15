from qt_core import *
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