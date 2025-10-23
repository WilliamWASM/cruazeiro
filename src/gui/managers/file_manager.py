from qt_core import QFileDialog

class FileManager:
    @staticmethod
    def select_file(parent=None, caption="Selecionar arquivo", filter="Arquivos Excel (*.xlsx *.csv *.xlsb)"):
        path, _ = QFileDialog.getOpenFileName(parent, caption, "", filter)
        return path or None

    @staticmethod
    def save_file(parent=None, caption="Salvar arquivo", filter="Arquivos Excel (*.xlsx *.csv)"):
        path, _ = QFileDialog.getSaveFileName(parent, caption, "", filter)
        return path or None

    @staticmethod
    def select_directory(parent=None, caption="Selecionar diretório"):
        path = QFileDialog.getExistingDirectory(parent, caption, "", QFileDialog.ShowDirsOnly)
        return path or None