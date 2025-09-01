from GUI.main_window import *
from GUI.widgets.cards import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setup_config(1200,700,700,400,"Teste Application")
    sys.exit(app.exec())