
from PySide6 import QtCore


class SerialWorkerSignals(QtCore.QObject):
    received = QtCore.Signal(str)
    stopped = QtCore.Signal()
    started = QtCore.Signal()


class SerialWorker(QtCore.QRunnable):
    def __init__(self, serial):
        super(SerialWorker, self).__init__()
        self.serial = serial
        self.signals = SerialWorkerSignals()
        self.running = False

    @QtCore.Slot()
    def run(self):
        self.running = True
        self.signals.started.emit()
        while self.running and self.serial.is_open:
            data = self.serial.read_all().decode('ascii')
            if data:
                self.signals.received.emit(data)
            QtCore.QThread.yieldCurrentThread()

    def stop(self):
        self.running = False
        self.signals.stopped.emit()
