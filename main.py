from src.gui.views.main_window import *
from src.gui.controllers.main_window_controller import *
import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = MainWindowController(window)
    window.show()
    sys.exit(app.exec())