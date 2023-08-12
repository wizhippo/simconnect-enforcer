import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QMenu


class LoggingConsole(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #444444; color: white;')

        self.setReadOnly(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.follow_output = True

    def show_context_menu(self, position):
        context_menu = QMenu(self)

        # Follow Output Action
        follow_output_action = QAction("Follow Output", self)
        follow_output_action.setCheckable(True)
        follow_output_action.setChecked(self.follow_output)
        follow_output_action.triggered.connect(self.toggle_follow_output)

        # Clear Action
        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear)

        # Select All Action
        select_all_action = QAction("Select All", self)
        select_all_action.triggered.connect(self.selectAll)

        # Copy Action
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy)

        context_menu.addAction(follow_output_action)
        context_menu.addSeparator()
        context_menu.addAction(copy_action)
        context_menu.addAction(select_all_action)
        context_menu.addSeparator()
        context_menu.addAction(clear_action)

        context_menu.exec(self.mapToGlobal(position))

    @Slot()
    def toggle_follow_output(self, checked):
        self.follow_output = checked
        bar = self.verticalScrollBar()
        bar.setValue(bar.maximum())
        self.update()

    @Slot()
    def log(self, message):
        self.append(message)
        if self.follow_output:
            bar = self.verticalScrollBar()
            bar.setValue(bar.maximum())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    logger = LoggingConsole()
    logger.log("Test message 1")
    logger.log("Test message 2")
    logger.show()
    sys.exit(app.exec())
