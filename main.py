import json
import logging
import os
import sys
from pathlib import Path

import sdl2
import sdl2.ext
import serial
from PySide6 import QtCore, QtWidgets, QtGui

appPath = os.fspath(Path(__file__).resolve().parent)
os.add_dll_directory(appPath)

from app import *
from serial_worker import SerialWorker
from mainwindow_ui import Ui_MainWindow
from settingswindow_ui import Ui_SettingsWindow
from coefficient_editor import CoefficientEditor
from simconnect_force_calculator import SimconnectForceCalculator
from simconnect_worker import SimConnectWorker


class SettingsWindow(QtWidgets.QMainWindow, Ui_SettingsWindow):
    updatedJoystickSettings = QtCore.Signal()
    updatedSerialPortSettings = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.splitter.setSizes([self.minimumSizeHint().width(), self.minimumSizeHint().width() * 3])
        self.joystickPage.updated.connect(self.on_updated_joystick_setting)
        self.serialPage.updated.connect(self.on_updated_serial_port_setting)

    @QtCore.Slot(dict)
    def on_updated_joystick_setting(self):
        self.updatedJoystickSettings.emit()

    @QtCore.Slot(dict)
    def on_updated_serial_port_setting(self):
        self.updatedSerialPortSettings.emit()


class ConsoleLoggingHandler(logging.Handler):
    def __init__(self, console=None):
        super().__init__()
        self.console = console

    def emit(self, record):
        if self.console:
            log_entry = self.format(record)
            self.console.log(log_entry)


class VLine(QtWidgets.QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.Shape.VLine)
        self.setFrameShadow(self.Shadow.Sunken)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        QtCore.QCoreApplication.setOrganizationName(APP_ORGANIZATON)
        QtCore.QCoreApplication.setApplicationName(APP_NAME)

        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_HAPTIC)

        self.serial_port_settings = {
            'port': '/dev/ttyUSB0',
            'baud': '115200',
            'data_bits': '8',
            'parity': 'None',
            'stop_bits': '2',
            'flow_control': 'None',
        }
        self.console_settings = {
            'font': 'None',
        }
        self.joystick_settings = None

        self.setStyleSheet('QSplitter::handle{background: red;')

        self.simconnectForceCalculator = SimconnectForceCalculator()
        self.threadpool = QtCore.QThreadPool()
        self.serial = None
        self.serial_worker = None
        self.hid_device = None
        self.simconnect_worker = None

        self.restoreSettings()

        self.settingsWindow = SettingsWindow()

        self.port_label = QtWidgets.QLabel("Port: Not Set")
        self.baud_rate_label = QtWidgets.QLabel("Baud Rate: Not Set")
        self.connection_status_label = QtWidgets.QLabel("Connection Status: Not Connected")

        self.statusbar.addPermanentWidget(VLine())
        self.statusbar.addPermanentWidget(self.port_label)
        self.statusbar.addPermanentWidget(VLine())
        self.statusbar.addPermanentWidget(self.baud_rate_label)
        self.statusbar.addPermanentWidget(VLine())
        self.statusbar.addPermanentWidget(self.connection_status_label)

        port = self.serial_port_settings["port"]
        self.port_label.setText(f"Port: {port}")
        baud_rate = self.serial_port_settings["baud"]
        self.baud_rate_label.setText(f"Baud Rate: {baud_rate}")

        self.actionConnectSerialPort.setEnabled(len(self.serial_port_settings["port"]))
        self.actionQuit.setEnabled(True)

        self.actionSettings.triggered.connect(self.on_show_settings)
        self.actionConnectSerialPort.toggled.connect(self.on_toggle_serial_port)
        self.actionClear.triggered.connect(self.serialConsole.clear)
        self.actionSimConnect.toggled.connect(self.on_toggle_simconnect)
        self.actionQuit.triggered.connect(self.close)
        self.actionAboutQt.triggered.connect(QtWidgets.QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.on_about)
        self.actionSaveCoefficients.triggered.connect(self.on_save_coefficients)
        self.actionLoadCoefficients.triggered.connect(self.on_load_coefficients)

        self.serialConsole.getData.connect(self.writeData)
        self.serialConsole.fontChanged.connect(self.saveConsoleFontSettings)

        self.actionCoefficientEditor.triggered.connect(self.on_show_coefficient_editor)

        self.settingsWindow.joystickPage.updated.connect(self.on_joystick_settings_updated)
        self.settingsWindow.serialPage.updated.connect(self.on_serial_port_settings_updated)

        self.statusbar.showMessage("Ready", 5000)

    @QtCore.Slot()
    def on_show_settings(self):
        self.settingsWindow.show()

    @QtCore.Slot()
    def on_joystick_settings_updated(self):
        self.joystick_settings = self.settingsWindow.joystickPage.getJoystickSettings()

    @QtCore.Slot()
    def on_serial_port_settings_updated(self):
        self.serial_port_settings = self.settingsWindow.serialPage.getSerialSettings()

    @QtCore.Slot()
    def on_save_coefficients(self):
        documents_path = QtCore.QDir.toNativeSeparators(
            QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DocumentsLocation))
        settings = QtCore.QSettings()
        documents_path = settings.value("last_opened_file", documents_path)
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", str(documents_path),
                                                            "Json Files (*.json);;All Files (*)")
        if filePath:
            with open(filePath, 'w') as json_file:
                json.dump(self.simconnectForceCalculator.coefficients, json_file, indent=2)
            settings = QtCore.QSettings()
            settings.setValue("last_opened_file", filePath)

    @QtCore.Slot()
    def on_load_coefficients(self):
        documents_path = QtCore.QDir.toNativeSeparators(
            QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DocumentsLocation))
        settings = QtCore.QSettings()
        documents_path = settings.value("last_opened_file", documents_path)
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", str(documents_path),
                                                            "Json Files (*.json);;All Files (*)")
        if filePath:
            with open(filePath, 'r') as json_file:
                self.simconnectForceCalculator.coefficients = json.load(json_file)

    @QtCore.Slot()
    def on_show_coefficient_editor(self):
        editor = CoefficientEditor(self.simconnectForceCalculator.coefficients, self)
        editor.show()

    @QtCore.Slot()
    def on_about(self):
        f = open("LICENSE-3RD-PARTY.txt", "r")
        third_party = f.read()
        f.close()

        QtWidgets.QMessageBox.about(self, "About SimConnect Enforcer",
                                    "This software create force feedback effects based on data from SimConnect<br/>"
                                    "This software makes use of the following 3rd party libraries<br/>"
                                    "<pre>" + third_party + "</pre>")

    @QtCore.Slot()
    def on_toggle_simconnect(self, checked):
        if checked:
            self.startSimConnect()
        else:
            self.stopSimConnect()

    @QtCore.Slot()
    def on_toggle_serial_port(self, checked):
        if checked:
            self.startSerialCommunication()
        else:
            self.stopSerialCommunication()

    def closeEvent(self, event):
        self.stopSerialCommunication()
        self.stopSimConnect()
        self.saveSettings()
        sdl2.SDL_Quit()

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue("window_state", self.saveState())
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("joystick_settings", self.joystick_settings)
        settings.setValue("serial_port_settings", self.serial_port_settings)
        settings.setValue("console_preferences", self.console_settings)
        settings.setValue("splitter/window_state", self.splitter.saveState())
        settings.setValue("simconnectForceCalculator/coefficients", self.simconnectForceCalculator.coefficients)

    def restoreSettings(self):
        settings = QtCore.QSettings()
        self.restoreState(settings.value("window_state", QtCore.QByteArray()))
        self.restoreGeometry(settings.value("window_geometry", QtCore.QByteArray()))
        self.joystick_settings = settings.value("joystick_settings", self.joystick_settings)
        self.serial_port_settings = settings.value("serial_port_settings", self.serial_port_settings)
        self.console_settings = settings.value("console_preferences", self.console_settings)
        if self.console_settings.get('font') != 'None':
            font = QtGui.QFont()
            font.fromString(self.console_settings.get('font'))
            self.serialConsole.setFont(font)
        self.splitter.restoreState(settings.value("splitter/window_state", QtCore.QByteArray()))
        loaded_coefficients = settings.value("simconnectForceCalculator/coefficients",
                                             self.simconnectForceCalculator.coefficients)
        if len(loaded_coefficients) == len(self.simconnectForceCalculator.coefficients):
            self.simconnectForceCalculator.coefficients = loaded_coefficients

    def startSimConnect(self):
        try:
            self.simconnectForceCalculator = SimconnectForceCalculator()
            self.simconnect_worker = SimConnectWorker(self.simconnectForceCalculator, self.joystick_settings[0])
            self.threadpool.start(self.simconnect_worker)
            self.simconnect_worker.signals.force_updated.connect(self.vectorDisplay.update_vector)
        except Exception as e:
            self.actionSimConnect.setChecked(False)
            logging.error(str(e))

    def stopSimConnect(self):
        if self.simconnect_worker:
            self.simconnect_worker.stop()

    def startSerialCommunication(self):
        try:
            self.serial = serial.Serial(
                port=self.serial_port_settings.get("port"),
                baudrate=self.serial_port_settings.get("baud"),
                bytesize=self.serial_port_settings.get("data_bits"),
                parity=self.serial_port_settings.get("parity"),
                stopbits=self.serial_port_settings.get("stop_bits"),
                xonxoff=True if self.serial_port_settings.get("flow_control") == 'Software' else False,
                rtscts=True if self.serial_port_settings.get("flow_control") == 'Hardware' else False
            )

            self.serial_worker = SerialWorker(self.serial)
            self.serial_worker.signals.received.connect(self.readData)
            self.threadpool.start(self.serial_worker)
        except Exception as e:
            self.actionConnectSerialPort.setChecked(False)
            logging.error(str(e))

    def stopSerialCommunication(self):
        if self.serial_worker:
            self.serial_worker.stop()

        if self.serial and self.serial.is_open:
            self.serial.close()
            self.serial = None

    def saveConsoleFontSettings(self, font):
        self.console_settings['font'] = font.toString()

    @QtCore.Slot(str)
    def writeData(self, data):
        if self.serial and self.serial.is_open:
            self.serial.write(data.decode('utf-8').encode('utf-8'))

    @QtCore.Slot(str)
    def readData(self, received_text):
        self.serialConsole.putData(f"{received_text}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root_logger = logging.getLogger()

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()

    console_logging_handler = ConsoleLoggingHandler(mainWindow.loggingConsole)
    console_logging_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_logger.addHandler(console_logging_handler)

    mainWindow.show()
    sys.exit(app.exec())
