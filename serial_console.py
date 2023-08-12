from PySide6.QtWidgets import QPlainTextEdit, QScrollBar, QMenu, QApplication, QFontDialog
from PySide6.QtGui import QPalette, QKeyEvent, QMouseEvent, QFont, QAction, QKeySequence
from PySide6.QtCore import Qt, Signal


class SerialConsole(QPlainTextEdit):
    getData = Signal(bytes)
    fontChanged = Signal(QFont)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document().setMaximumBlockCount(100)

        p = self.palette()
        p.setColor(QPalette.Base, Qt.black)
        p.setColor(QPalette.Text, Qt.green)
        self.setPalette(p)

        self.setFont(QFont('Console', 10))
        self.localEchoEnabled = False

    def putData(self, data):
        self.insertPlainText(data)
        bar = self.verticalScrollBar()
        bar.setValue(bar.maximum())

    def setLocalEchoEnabled(self, set):
        self.localEchoEnabled = set

    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Backspace, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            return
        if self.localEchoEnabled:
            super(SerialConsole, self).keyPressEvent(e)
        self.getData.emit(e.text().encode('utf-8'))

    def contextMenuEvent(self, event):
        context_menu = self.createStandardContextMenu()

        for i, action in enumerate(context_menu.actions()):
            if action.objectName() == "edit-paste":
                context_menu.removeAction(action)
                custom_copy_action = QAction("Paste", self)
                custom_copy_action.setShortcut(QKeySequence.Paste)
                custom_copy_action.triggered.connect(self.customPaste)
                context_menu.insertAction(context_menu.actions()[
                                              i], custom_copy_action)
                break

        clear_action = QAction("Clear Console", self)
        clear_action.triggered.connect(self.clear)
        context_menu.addAction(clear_action)

        font_selector_action = QAction("Select Font", self)
        font_selector_action.triggered.connect(self.selectFont)
        context_menu.addAction(font_selector_action)

        context_menu.exec(event.globalPos())

    def customPaste(self):
        clipboard_data = QApplication.clipboard().text()
        if clipboard_data:
            self.getData.emit(clipboard_data.encode('utf-8'))

    def selectFont(self):
        ok, font = QFontDialog.getFont(self.font(), self)
        if ok:
            self.setFont(font)
            self.fontChanged.emit(font)
