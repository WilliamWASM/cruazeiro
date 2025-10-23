from PySide6.QtCore import QThreadPool
from ..gui.views.notifications import Notification
from .worker import Worker

class CardActionWorker:
    def __init__(self, func, *args, parent=None, minimal_duration=3000, **kwargs):
        self.parent = parent
        self.minimal_duration = minimal_duration
        
        self.dialog = Notification.processing_action_card(
            parent=parent, 
            minimal_duration=minimal_duration
        )
        
        self.worker = Worker(func, *args, **kwargs)
        self.worker.signals.finished.connect(self.on_finished)
        self.worker.signals.error.connect(self.on_error)
        self.worker.signals.result.connect(self.on_result)

    def run(self):
        self.dialog.show()
        QThreadPool.globalInstance().start(self.worker)

    def on_result(self, result):
        self._result = result 

    def on_error(self, error_msg):
        self._error = error_msg

    def on_finished(self):
        self.dialog.safe_close()  

        self.signals.finished.emit()

        if hasattr(self, "_error"):
            Notification.error("Erro", self._error)
        else:
            Notification.info("Sucesso", getattr(self, "_result", "Operação concluída"))