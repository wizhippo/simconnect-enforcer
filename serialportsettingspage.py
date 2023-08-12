import serial.tools.list_ports
from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QMessageBox, QVBoxLayout, QLineEdit


class SerialPortSettingsPage(QWidget):
    updated = Signal(dict)

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Serial Port Options")
        self.setMinimumWidth(400)

        self.port_label = QLabel("Select Serial Port:")
        self.port_combo = QComboBox()

        self.baud_label = QLabel("Baud Rate:")
        self.baud_combo = QComboBox()  # Drop-down for baud rates
        self.baud_combo.addItems(["300", "1200", "2400", "4800", "9600", "14400", "19200", "38400",
                                  "57600", "115200", "230400", "460800", "921600", "Custom"])
        self.baud_combo.setCurrentText("115200")
        self.custom_baud_edit = QLineEdit()
        self.custom_baud_edit.setPlaceholderText("Enter custom baud rate")
        self.custom_baud_edit.setEnabled(False)
        self.custom_baud_edit.setValidator(QIntValidator())  # Allow only integer input

        self.data_bits_label = QLabel("Data Bits:")
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.addItems(["5", "6", "7", "8"])
        self.data_bits_combo.setCurrentText("8")

        self.parity_label = QLabel("Parity:")
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(["None", "Even", "Odd", "Mark", "Space"])

        self.stop_bits_label = QLabel("Stop Bits:")
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.addItems(["1", "1.5", "2"])
        self.stop_bits_combo.setCurrentText("1")

        self.flow_control_label = QLabel("Flow Control:")
        self.flow_control_combo = QComboBox()
        self.flow_control_combo.addItems(["None", "Hardware", "Software"])

        self.options_button = QPushButton("Apply")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.port_label)
        self.layout.addWidget(self.port_combo)
        self.layout.addWidget(self.baud_label)
        self.layout.addWidget(self.baud_combo)
        self.layout.addWidget(self.custom_baud_edit)
        self.layout.addWidget(self.data_bits_label)
        self.layout.addWidget(self.data_bits_combo)
        self.layout.addWidget(self.parity_label)
        self.layout.addWidget(self.parity_combo)
        self.layout.addWidget(self.stop_bits_label)
        self.layout.addWidget(self.stop_bits_combo)
        self.layout.addWidget(self.flow_control_label)
        self.layout.addWidget(self.flow_control_combo)
        self.layout.addWidget(self.options_button)

        self.setLayout(self.layout)

        if settings:
            self.port_combo.setCurrentText(settings.get('port'))
            if str(settings['baud']) in [str(self.baud_combo.itemText(index)) for index in
                                         range(self.baud_combo.count())]:
                self.baud_combo.setCurrentText(str(settings.get('baud')))
            else:
                self.baud_combo.setCurrentText("Custom")
                self.custom_baud_edit.setText(str(settings.get('baud')))
            self.data_bits_combo.setCurrentText(
                str(settings.get('data_bits')))
            self.parity_combo.setCurrentText(settings.get('parity'))
            self.stop_bits_combo.setCurrentText(
                str(settings.get('stop_bits')))
            self.flow_control_combo.setCurrentText(settings.get('flow_control'))

        self.populate_serial_ports()
        self.baud_combo.currentTextChanged.connect(
            self.handle_baud_rate_selection)
        self.options_button.clicked.connect(self.set_serial_options)

    def populate_serial_ports(self):
        available_ports = list(serial.tools.list_ports.comports())
        for port in available_ports:
            self.port_combo.addItem(port.device)

    def handle_baud_rate_selection(self, text):
        if text == "Custom":
            self.custom_baud_edit.setEnabled(True)
        else:
            self.custom_baud_edit.setEnabled(False)

    def set_serial_options(self):
        selected_port = self.port_combo.currentText()
        if not selected_port:
            QMessageBox.warning(self, "No Port Selected",
                                "Please select a serial port.")
            return

        if self.baud_combo.currentText() == "Custom":
            baud_rate = int(self.custom_baud_edit.text())
        else:
            baud_rate = int(self.baud_combo.currentText())
        data_bits = int(self.data_bits_combo.currentText())
        parity = self.parity_combo.currentText()

        # Convert stop bits to float (e.g., "1" to 1.0)
        stop_bits = float(self.stop_bits_combo.currentText())

        flow_control = self.flow_control_combo.currentText()

        settings = {
            'port': selected_port,
            'baud': baud_rate,
            'data_bits': data_bits,
            'parity': parity,
            'stop_bits': stop_bits,
            'flow_control': flow_control
        }

        if selected_port:
            self.updated.emit(settings)

    def getSerialSettings(self):
        selected_port = self.port_combo.currentText()
        if self.baud_combo.currentText() == "Custom":
            baud_rate = int(self.custom_baud_edit.text())
        else:
            baud_rate = int(self.baud_combo.currentText())
        parity_str = self.parity_combo.currentText()
        data_bits_str = self.data_bits_combo.currentText()
        stop_bits_str = self.data_bits_combo.currentText()

        parity = serial.PARITY_NONE
        if parity_str == "Even":
            parity = serial.PARITY_EVEN
        elif parity_str == "Odd":
            parity = serial.PARITY_ODD
        elif parity_str == "Mark":
            parity = serial.PARITY_MARK
        elif parity_str == "Space":
            parity = serial.PARITY_SPACE

        data_bits = serial.EIGHTBITS
        if data_bits_str == "5":
            data_bits = serial.FIVEBITS
        elif data_bits_str == "6":
            data_bits = serial.SIXBITS
        elif data_bits_str == "7":
            data_bits = serial.EIGHTBITS

        stop_bits = serial.STOPBITS_ONE
        if stop_bits_str == "1":
            stop_bits = serial.STOPBITS_ONE
        elif stop_bits_str == "1.5":
            stop_bits = serial.STOPBITS_ONE_POINT_FIVE
        elif stop_bits_str == "2":
            stop_bits = serial.STOPBITS_TWO

        flow_control_str = self.flow_control_combo.currentText()

        return {
            'port': selected_port,
            'baud': baud_rate,
            'data_bits': data_bits,
            'parity': parity,
            'stop_bits': stop_bits,
            'xonxoff': True if flow_control_str == "Software" else False,
            'rtscts': True if flow_control_str == "Hardware" else False,
        }
