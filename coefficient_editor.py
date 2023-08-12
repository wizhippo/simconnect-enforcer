from PySide6 import QtCore, QtWidgets, QtGui

from coefficient_edditor_ui import Ui_CoefficientEditor


class CoefficientEditor(QtWidgets.QMainWindow, Ui_CoefficientEditor):
    def __init__(self, coefficients, parent=None):
        super(CoefficientEditor, self).__init__(parent)
        self.setupUi(self)
        self.coefficients = coefficients
        self.selected_coefficient = None

        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)

        for k in self.coefficients:
            item = QtGui.QStandardItem(k)
            self.model.appendRow(item)

        index = self.model.index(0, 0)
        self.listView.setCurrentIndex(index)
        self.on_item_selected()

        self.splitter.setSizes([self.minimumSizeHint().width(), self.minimumSizeHint().width() * 3])

        self.listView.clicked.connect(self.on_item_selected)
        self.envelopEditor.updated.connect(self.on_new_envelope)
        self.setMinButton.clicked.connect(self.on_set_min_button)
        self.setMidButton.clicked.connect(self.on_set_mid_button)
        self.setMaxButton.clicked.connect(self.on_set_max_button)

    @QtCore.Slot()
    def on_set_min_button(self, points):
        if self.selected_coefficient:
            self.coefficients[self.selected_coefficient] = [(0, 0), (1, 0)]
            self.envelopEditor.setPoints(self.coefficients[self.selected_coefficient])
            self.update()

    @QtCore.Slot()
    def on_set_mid_button(self, points):
        if self.selected_coefficient:
            self.coefficients[self.selected_coefficient] = [(0, 0.5), (1, 0.5)]
            self.envelopEditor.setPoints(self.coefficients[self.selected_coefficient])
            self.update()

    @QtCore.Slot()
    def on_set_max_button(self, points):
        if self.selected_coefficient:
            self.coefficients[self.selected_coefficient] = [(0, 1), (1, 1)]
            self.envelopEditor.setPoints(self.coefficients[self.selected_coefficient])
            self.update()

    @QtCore.Slot()
    def on_item_selected(self):
        self.selected_coefficient = self.listView.currentIndex().data()
        if self.selected_coefficient:
            self.envelopEditor.setPoints(self.coefficients[self.selected_coefficient])

    @QtCore.Slot()
    def on_new_envelope(self, points):
        self.coefficients[self.selected_coefficient] = points
