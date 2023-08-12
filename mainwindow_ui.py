# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QSplitter, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)

from logging_console import LoggingConsole
from serial_console import SerialConsole
from uivector import UIVector
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(627, 460)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/feather/info.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout.setIcon(icon)
        self.actionAboutQt = QAction(MainWindow)
        self.actionAboutQt.setObjectName(u"actionAboutQt")
        self.actionAboutQt.setIcon(icon)
        self.actionConnectSerialPort = QAction(MainWindow)
        self.actionConnectSerialPort.setObjectName(u"actionConnectSerialPort")
        self.actionConnectSerialPort.setCheckable(True)
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/feather/terminal.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionConnectSerialPort.setIcon(icon1)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/feather/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon2)
        self.actionClear = QAction(MainWindow)
        self.actionClear.setObjectName(u"actionClear")
        icon3 = QIcon()
        icon3.addFile(u":/icons/resources/icons/feather/refresh-ccw.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClear.setIcon(icon3)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        icon4 = QIcon()
        icon4.addFile(u":/icons/resources/icons/feather/log-out.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionQuit.setIcon(icon4)
        self.actionSimConnect = QAction(MainWindow)
        self.actionSimConnect.setObjectName(u"actionSimConnect")
        self.actionSimConnect.setCheckable(True)
        icon5 = QIcon()
        icon5.addFile(u":/icons/resources/icons/feather/toggle-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon5.addFile(u":/icons/resources/icons/feather/toggle-right.svg", QSize(), QIcon.Normal, QIcon.On)
        self.actionSimConnect.setIcon(icon5)
        self.actionSimConnect.setMenuRole(QAction.NoRole)
        self.actionCoefficientEditor = QAction(MainWindow)
        self.actionCoefficientEditor.setObjectName(u"actionCoefficientEditor")
        icon6 = QIcon()
        icon6.addFile(u":/icons/resources/icons/feather/activity.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionCoefficientEditor.setIcon(icon6)
        self.actionCoefficientEditor.setMenuRole(QAction.NoRole)
        self.actionSaveCoefficients = QAction(MainWindow)
        self.actionSaveCoefficients.setObjectName(u"actionSaveCoefficients")
        icon7 = QIcon()
        icon7.addFile(u":/icons/resources/icons/feather/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSaveCoefficients.setIcon(icon7)
        self.actionSaveCoefficients.setMenuRole(QAction.NoRole)
        self.actionLoadCoefficients = QAction(MainWindow)
        self.actionLoadCoefficients.setObjectName(u"actionLoadCoefficients")
        icon8 = QIcon()
        icon8.addFile(u":/icons/resources/icons/feather/book-open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionLoadCoefficients.setIcon(icon8)
        self.actionLoadCoefficients.setMenuRole(QAction.NoRole)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.loggingConsole = LoggingConsole(self.layoutWidget)
        self.loggingConsole.setObjectName(u"loggingConsole")
        self.loggingConsole.setReadOnly(True)

        self.horizontalLayout.addWidget(self.loggingConsole)

        self.vectorDisplay = UIVector(self.layoutWidget)
        self.vectorDisplay.setObjectName(u"vectorDisplay")

        self.horizontalLayout.addWidget(self.vectorDisplay)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.splitter.addWidget(self.layoutWidget)
        self.serialConsole = SerialConsole(self.splitter)
        self.serialConsole.setObjectName(u"serialConsole")
        self.splitter.addWidget(self.serialConsole)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 627, 22))
        self.menuCalls = QMenu(self.menubar)
        self.menuCalls.setObjectName(u"menuCalls")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuCalls.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuCalls.addAction(self.actionSimConnect)
        self.menuCalls.addAction(self.actionConnectSerialPort)
        self.menuCalls.addAction(self.actionSaveCoefficients)
        self.menuCalls.addAction(self.actionLoadCoefficients)
        self.menuCalls.addSeparator()
        self.menuCalls.addAction(self.actionQuit)
        self.menuTools.addAction(self.actionSettings)
        self.menuTools.addAction(self.actionClear)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAboutQt)
        self.mainToolBar.addAction(self.actionSimConnect)
        self.mainToolBar.addAction(self.actionCoefficientEditor)
        self.mainToolBar.addAction(self.actionConnectSerialPort)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SimConnect Enforcer", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"&About", None))
#if QT_CONFIG(tooltip)
        self.actionAbout.setToolTip(QCoreApplication.translate("MainWindow", u"About program", None))
#endif // QT_CONFIG(tooltip)
        self.actionAboutQt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.actionConnectSerialPort.setText(QCoreApplication.translate("MainWindow", u"C&onnect", None))
#if QT_CONFIG(tooltip)
        self.actionConnectSerialPort.setToolTip(QCoreApplication.translate("MainWindow", u"Connect to serial port", None))
#endif // QT_CONFIG(tooltip)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.actionClear.setText(QCoreApplication.translate("MainWindow", u"C&lear", None))
#if QT_CONFIG(tooltip)
        self.actionClear.setToolTip(QCoreApplication.translate("MainWindow", u"Clear data", None))
#endif // QT_CONFIG(tooltip)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionSimConnect.setText(QCoreApplication.translate("MainWindow", u"SimConnect", None))
#if QT_CONFIG(tooltip)
        self.actionSimConnect.setToolTip(QCoreApplication.translate("MainWindow", u"SimConnect", None))
#endif // QT_CONFIG(tooltip)
        self.actionCoefficientEditor.setText(QCoreApplication.translate("MainWindow", u"CoefficientEditor", None))
        self.actionSaveCoefficients.setText(QCoreApplication.translate("MainWindow", u"SaveCoefficients", None))
        self.actionLoadCoefficients.setText(QCoreApplication.translate("MainWindow", u"LoadCoefficients", None))
        self.menuCalls.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

