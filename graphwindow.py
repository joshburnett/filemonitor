# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graphwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QToolBar,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget
import icons_rc

class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        if not GraphWindow.objectName():
            GraphWindow.setObjectName(u"GraphWindow")
        GraphWindow.resize(676, 484)
        icon = QIcon()
        icon.addFile(u":/icons/icons/graph_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        GraphWindow.setWindowIcon(icon)
        GraphWindow.setStyleSheet(u"")
        self.actionEditConfiguration = QAction(GraphWindow)
        self.actionEditConfiguration.setObjectName(u"actionEditConfiguration")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/advanced.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionEditConfiguration.setIcon(icon1)
        self.actionTest1 = QAction(GraphWindow)
        self.actionTest1.setObjectName(u"actionTest1")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/agt_update_critical.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionTest1.setIcon(icon2)
        self.actionTest2 = QAction(GraphWindow)
        self.actionTest2.setObjectName(u"actionTest2")
        self.actionTest2.setIcon(icon2)
        self.actionMonitorFileToggle = QAction(GraphWindow)
        self.actionMonitorFileToggle.setObjectName(u"actionMonitorFileToggle")
        self.actionMonitorFileToggle.setCheckable(True)
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/player_play.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/icons/player_pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.actionMonitorFileToggle.setIcon(icon3)
        self.actionLoadPresetConfig = QAction(GraphWindow)
        self.actionLoadPresetConfig.setObjectName(u"actionLoadPresetConfig")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/openConfig.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionLoadPresetConfig.setIcon(icon4)
        self.actionReloadFile = QAction(GraphWindow)
        self.actionReloadFile.setObjectName(u"actionReloadFile")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/quick_restart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionReloadFile.setIcon(icon5)
        self.actionClearData = QAction(GraphWindow)
        self.actionClearData.setObjectName(u"actionClearData")
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/editdelete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionClearData.setIcon(icon6)
        self.centralwidget = QWidget(GraphWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchText = QComboBox(self.centralwidget)
        self.searchText.setObjectName(u"searchText")
        self.searchText.setEditable(True)
        self.searchText.setInsertPolicy(QComboBox.NoInsert)

        self.horizontalLayout.addWidget(self.searchText)

        self.autoFormatButton = QPushButton(self.centralwidget)
        self.autoFormatButton.setObjectName(u"autoFormatButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoFormatButton.sizePolicy().hasHeightForWidth())
        self.autoFormatButton.setSizePolicy(sizePolicy)
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/cache.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.autoFormatButton.setIcon(icon7)

        self.horizontalLayout.addWidget(self.autoFormatButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.verticalLayout.addWidget(self.plotWidget)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        GraphWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(GraphWindow)
        self.statusBar.setObjectName(u"statusBar")
        GraphWindow.setStatusBar(self.statusBar)
        self.toolBar = QToolBar(GraphWindow)
        self.toolBar.setObjectName(u"toolBar")
        GraphWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.debugToolBar = QToolBar(GraphWindow)
        self.debugToolBar.setObjectName(u"debugToolBar")
        GraphWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.debugToolBar)

        self.toolBar.addAction(self.actionMonitorFileToggle)
        self.toolBar.addAction(self.actionReloadFile)
        self.toolBar.addAction(self.actionClearData)
        self.toolBar.addAction(self.actionEditConfiguration)
        self.debugToolBar.addAction(self.actionTest1)
        self.debugToolBar.addAction(self.actionTest2)
        self.debugToolBar.addAction(self.actionLoadPresetConfig)

        self.retranslateUi(GraphWindow)

        QMetaObject.connectSlotsByName(GraphWindow)
    # setupUi

    def retranslateUi(self, GraphWindow):
        GraphWindow.setWindowTitle(QCoreApplication.translate("GraphWindow", u"File Monitor", None))
        self.actionEditConfiguration.setText(QCoreApplication.translate("GraphWindow", u"Edit Configuration", None))
#if QT_CONFIG(tooltip)
        self.actionEditConfiguration.setToolTip(QCoreApplication.translate("GraphWindow", u"Edit the graph's configuration", None))
#endif // QT_CONFIG(tooltip)
        self.actionTest1.setText(QCoreApplication.translate("GraphWindow", u"Test 1", None))
#if QT_CONFIG(tooltip)
        self.actionTest1.setToolTip(QCoreApplication.translate("GraphWindow", u"Test 1", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionTest1.setShortcut(QCoreApplication.translate("GraphWindow", u"Ctrl+1", None))
#endif // QT_CONFIG(shortcut)
        self.actionTest2.setText(QCoreApplication.translate("GraphWindow", u"Test 2", None))
#if QT_CONFIG(tooltip)
        self.actionTest2.setToolTip(QCoreApplication.translate("GraphWindow", u"Test 2", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionTest2.setShortcut(QCoreApplication.translate("GraphWindow", u"Ctrl+2", None))
#endif // QT_CONFIG(shortcut)
        self.actionMonitorFileToggle.setText(QCoreApplication.translate("GraphWindow", u"Monitor File", None))
#if QT_CONFIG(tooltip)
        self.actionMonitorFileToggle.setToolTip(QCoreApplication.translate("GraphWindow", u"Toggle file monitoring", None))
#endif // QT_CONFIG(tooltip)
        self.actionLoadPresetConfig.setText(QCoreApplication.translate("GraphWindow", u"Load Preset Config", None))
#if QT_CONFIG(tooltip)
        self.actionLoadPresetConfig.setToolTip(QCoreApplication.translate("GraphWindow", u"Load Preset Config", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionLoadPresetConfig.setShortcut(QCoreApplication.translate("GraphWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionReloadFile.setText(QCoreApplication.translate("GraphWindow", u"Reload File", None))
#if QT_CONFIG(tooltip)
        self.actionReloadFile.setToolTip(QCoreApplication.translate("GraphWindow", u"Reparse Entire File", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionReloadFile.setShortcut(QCoreApplication.translate("GraphWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionClearData.setText(QCoreApplication.translate("GraphWindow", u"Clear Data", None))
#if QT_CONFIG(tooltip)
        self.actionClearData.setToolTip(QCoreApplication.translate("GraphWindow", u"Clear Data Buffer", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.autoFormatButton.setToolTip(QCoreApplication.translate("GraphWindow", u"Auto-Generate Format From Current String", None))
#endif // QT_CONFIG(tooltip)
        self.autoFormatButton.setText("")
        self.toolBar.setWindowTitle(QCoreApplication.translate("GraphWindow", u"toolBar", None))
        self.debugToolBar.setWindowTitle(QCoreApplication.translate("GraphWindow", u"toolBar_2", None))
#if QT_CONFIG(tooltip)
        self.debugToolBar.setToolTip("")
#endif // QT_CONFIG(tooltip)
    # retranslateUi

