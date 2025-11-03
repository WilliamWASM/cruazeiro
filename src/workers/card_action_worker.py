from PySide6.QtCore import QThreadPool, QTimer, Qt
from ..gui.views.notifications import Notification
from .worker import Worker

class CardActionWorker:
    def __init__(self, func, data, parent=None, minimal_duration=3000):
        self.parent = parent
        self.dialog = Notification.processing_action_card(parent=parent, minimal_duration=minimal_duration)
        self.worker = Worker(func, data)

        self.worker.signals.finished.connect(self.on_finished, Qt.QueuedConnection)
        self.worker.signals.error.connect(self.on_error, Qt.QueuedConnection)
        self.worker.signals.result.connect(self.on_result, Qt.QueuedConnection)
        self.worker.signals.ask_input.connect(self.on_ask_input, Qt.BlockingQueuedConnection)

        self._result = None
        self._error = None

    def run(self):
        QThreadPool.globalInstance().start(self.worker)

        self.dialog.exec()  

    def on_result(self, result):
        self._result = result

    def on_error(self, error_msg):
        self._error = error_msg

    def on_finished(self):
        self.dialog.safe_close()

    def on_ask_input(self, payload):
        fields, title, future = payload
        result = Notification.get_inputs(fields, title, self.parent)
        future.set_result(result)

    def show_result_notification(self):
        if self._error:
            Notification.error("Erro", self._error)
        else:
            Notification.info("Sucesso", self._result or "Operação concluída")
