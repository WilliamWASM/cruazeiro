from qt_core import *
import time
class Notification():

    @staticmethod
    def info(title,text,parent = None):
        return QMessageBox.information(parent,title,text)

    @staticmethod
    def error(title,text,parent = None):
        return QMessageBox.critical(parent,title,text)

    @staticmethod
    def get_inputs(fields:list, title="Entradas do Usuário", parent=None):
        class InputDialog(QDialog):
            def __init__(self, labels):
                super().__init__(parent)
                self.setWindowTitle(title)
                self.setModal(True)

                layout = QVBoxLayout()
                self.inputs = []

                for field in fields:
                    layout.addWidget(QLabel(field))
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

        dialog = InputDialog(fields)
        if dialog.exec():
            return dialog.get_values()
        return None
    
    
    @staticmethod
    def processing_action_card(parent=None, minimal_duration=3000):
        class LoadingDialog(QDialog):
            def __init__(self, parent, minimal_duration):
                super().__init__(parent)
                self.setModal(True)
                self.setWindowTitle("Processando Tarefa")
                self.setFixedSize(300, 100)
                self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
                
                layout = QVBoxLayout(self)
                self.processing_lbl = QLabel("Aguarde, executando tarefas...")
                self.progress = QProgressBar()
                self.progress.setRange(0, 0)
                
                layout.addWidget(self.processing_lbl)
                layout.addWidget(self.progress)
                
                self.minimal_duration = minimal_duration
                self.start_time = None

            def showEvent(self, event):
                super().showEvent(event)
                self.start_time = time.time()

            def safe_close(self):
                elapsed = (time.time() - self.start_time) * 1000
                remaining = max(0, self.minimal_duration - elapsed)
                
                if remaining > 0:
                    QTimer.singleShot(int(remaining), self.accept)
                else:
                    self.accept()

        return LoadingDialog(parent, minimal_duration)
