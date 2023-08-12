# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'coefficient_edditor.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QListView,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QVBoxLayout,
    QWidget)

from envelope_editor import EnvelopeEditor

class Ui_CoefficientEditor(object):
    def setupUi(self, CoefficientEditor):
        if not CoefficientEditor.objectName():
            CoefficientEditor.setObjectName(u"CoefficientEditor")
        CoefficientEditor.resize(800, 600)
        self.centralwidget = QWidget(CoefficientEditor)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listView = QListView(self.splitter)
        self.listView.setObjectName(u"listView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.listView)
        self.envelopEditor = EnvelopeEditor(self.splitter)
        self.envelopEditor.setObjectName(u"envelopEditor")
        self.envelopEditor.setFrameShape(QFrame.StyledPanel)
        self.envelopEditor.setFrameShadow(QFrame.Sunken)
        self.splitter.addWidget(self.envelopEditor)

        self.verticalLayout.addWidget(self.splitter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.setMinButton = QPushButton(self.centralwidget)
        self.setMinButton.setObjectName(u"setMinButton")

        self.horizontalLayout.addWidget(self.setMinButton)

        self.setMidButton = QPushButton(self.centralwidget)
        self.setMidButton.setObjectName(u"setMidButton")

        self.horizontalLayout.addWidget(self.setMidButton)

        self.setMaxButton = QPushButton(self.centralwidget)
        self.setMaxButton.setObjectName(u"setMaxButton")

        self.horizontalLayout.addWidget(self.setMaxButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        CoefficientEditor.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CoefficientEditor)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        CoefficientEditor.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CoefficientEditor)
        self.statusbar.setObjectName(u"statusbar")
        CoefficientEditor.setStatusBar(self.statusbar)

        self.retranslateUi(CoefficientEditor)

        QMetaObject.connectSlotsByName(CoefficientEditor)
    # setupUi

    def retranslateUi(self, CoefficientEditor):
        CoefficientEditor.setWindowTitle(QCoreApplication.translate("CoefficientEditor", u"MainWindow", None))
        self.setMinButton.setText(QCoreApplication.translate("CoefficientEditor", u"Set min", None))
        self.setMidButton.setText(QCoreApplication.translate("CoefficientEditor", u"Set mid", None))
        self.setMaxButton.setText(QCoreApplication.translate("CoefficientEditor", u"Set max", None))
    # retranslateUi

