import sdl2
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QSpacerItem, QSizePolicy


class JoystickSettingsPage(QWidget):
    updated = Signal()

    def __init__(self):
        super().__init__()
        self.settings = None

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Select Joystick:", self)
        self.joystickComboBox = QComboBox(self)

        self.populate_joysticks()

        self.apply_button = QPushButton("Apply")

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.joystickComboBox)
        self.layout.addWidget(self.apply_button)
        self.layout.addItem(self.spacer)
        self.setLayout(self.layout)

        self.setWindowTitle('Joystick Selector')
        self.setGeometry(200, 200, 300, 150)

        self.apply_button.clicked.connect(self.on_apply_button_clicked)

    def populate_joysticks(self):
        num_joysticks = sdl2.SDL_NumJoysticks()
        for i in range(num_joysticks):
            joystick_name = sdl2.SDL_JoystickNameForIndex(i).decode('utf-8')
            self.joystickComboBox.addItem(joystick_name, i)

    @Slot()
    def on_apply_button_clicked(self):
        index = self.joystickComboBox.currentIndex()
        name = self.joystickComboBox.currentText()
        self.settings = (index, name)
        self.updated.emit()

    def getJoystickSettings(self):
        return self.settings
