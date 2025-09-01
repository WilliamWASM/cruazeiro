from GUI.qt_core import *

class Notification():

    @staticmethod
    def info(title,text,parent = None):
        return QMessageBox.information(parent,title,text)

    @staticmethod
    def error(title,text,parent = None):
        return QMessageBox.critical(parent,title,text)

    
    @staticmethod
    def get_user_input(parent=None):
        class InputDialog(QDialog):
            def __init__(self):
                super().__init__(parent)
                self.setWindowTitle("Entradas do Usuário")
                self.setModal(True)

                layout = QVBoxLayout()
                self.inputs = []

                for label_text in ["Data End", "OSC", "Semestre de Ingresso"]:
                    layout.addWidget(QLabel(label_text))
                    line_edit = QLineEdit()
                    line_edit.textChanged.connect(self.check_inputs)
                    layout.addWidget(line_edit)
                    self.inputs.append(line_edit)

                self.ok_button = QPushButton("OK")
                self.ok_button.setEnabled(False)
                self.ok_button.clicked.connect(self.accept)
                layout.addWidget(self.ok_button)

                self.setLayout(layout)

            def check_inputs(self):
                filled = all(field.text().strip() for field in self.inputs)
                self.ok_button.setEnabled(filled)

            def get_values(self):
                return [field.text().strip() for field in self.inputs]

        dialog = InputDialog()
        if dialog.exec():
            return dialog.get_values()
        return None