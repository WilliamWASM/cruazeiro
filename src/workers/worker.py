from qt_core import *
from concurrent.futures import Future

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(object)  
    ask_input = Signal(object)

class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit() 

    def ask_for_input(self, fields, title="User Input"):
        future = Future()
        self.signals.ask_input.emit((fields, title, future))
        return future.result()