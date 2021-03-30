# -*- coding: utf-8 -*-
"""
Monitor a text file, extracting and plotting data on-the-fly

Parses the data file using scanf-style formatting strings


Author: Josh Burnett
Version: 1.0

Releases:
0.1
    2021-03-30, J. Burnett
    * Initial release
"""

__version__ = '0.1'
##__debugging__ = True

import re
import datetime
import sys, os
from pathlib import Path

from guidata.dataset.datatypes import DataSet, GetAttrProp, FuncProp
from guidata.dataset.dataitems import (FloatItem, IntItem, BoolItem, ChoiceItem,
                                       MultipleChoiceItem, ImageChoiceItem, FilesOpenItem,
                                       StringItem, TextItem, ColorItem, FileSaveItem,
                                       FileOpenItem, DirectoryItem, FloatArrayItem,
                                       DateItem, DateTimeItem)

# use numpy and pyqtgraph for graphing
from pyqtgraph.Qt import QtCore, QtWidgets
import pyqtgraph as pg
# fix pg.graphicsItems.ViewBox.enableAutoRange method
import monkeypatch_pyqtgraph

# GUI stuff.
import graphWindow

from scanf import scanf

pyqtSignal = QtCore.pyqtSignal


# copied from seaborn.palettes.py
SEABORN_PALETTES = dict(
    deep=["#4C72B0", "#55A868", "#C44E52",
          "#8172B2", "#CCB974", "#64B5CD"],
    muted=["#4878CF", "#6ACC65", "#D65F5F",
           "#B47CC7", "#C4AD66", "#77BEDB"],
    pastel=["#92C6FF", "#97F0AA", "#FF9F9A",
            "#D0BBFF", "#FFFEA3", "#B0E0E6"],
    bright=["#003FFF", "#03ED3A", "#E8000B",
            "#8A2BE2", "#FFC400", "#00D7FF"],
    dark=["#001C7F", "#017517", "#8C0900",
          "#7600A1", "#B8860B", "#006374"],
    colorblind=["#0072B2", "#009E73", "#D55E00",
                "#CC79A7", "#F0E442", "#56B4E9"]
    )


# Lets us know if we're running from the python code or the compiled executable.
# I assume that if we're running the python code, we should effectively be in DEBUG mode,
# so some extra GUI items are made visible.  If we're running from the executable, those
# GUI items get hidden.
def main_is_frozen():
    return hasattr(sys, "frozen")  # new py2exe


def get_main_dir():
    if main_is_frozen():
        return Path(sys.executable).parent
    return Path(sys.argv[0]).parent


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = graphWindow.Ui_GraphWindow()

        # bg_color = pg.mkColor("#EAEAF2") # from seaborn.rcmos.py ('darkgrid' style)
        pg.setConfigOptions(background='w', foreground='k')
        pg.setConfigOptions(antialias=True)

        self.ui.setupUi(self)

        buildRecord = open('build_record.txt', 'r')
        self.buildNum = int(buildRecord.readlines()[-1].split(',')[0])
        buildRecord.close()
        self.ui.centralwidget.window().setProperty('windowTitle','File Monitor (v%s-r%i)' % (__version__, self.buildNum))

        self.ui.plotWidget.showGrid(x=True, y=True, alpha=0.25)

        self.y = []
        self.fname = ''
        self.curves = []
        self.colors = SEABORN_PALETTES['muted']
        self.datalabelstring = ''  # stores the plain data label string, used to check and see if it has changed
        self.datalabels = []       # stores the actual parsed data labels, split at any commas
        self.legend = None
        self.showlegend = False
        self.config = GraphConfig()

        if main_is_frozen():
            self.ui.debugToolBar.setVisible(False)

        self.config.filepath = ''
        self.filepath = self.config.filepath
        self.filelocation = 0
        self.mod_time = None
        self.file_size = None

        self.npoints = 0
        self.plotallpoints = True
        self.xlabel = ''

        self.replot = True

        self.load_format_presets()

        # set up status bar
        self.file_sb = QtWidgets.QLabel(self.statusBar())
        self.statusBar().addWidget(self.file_sb, 1)

        self.timestamp_sb = QtWidgets.QLabel('  Updated at: 0000-00-00, 00:00:00 AM  ', self.statusBar())
        self.timestamp_sb.setAlignment(QtCore.Qt.AlignCenter)
        self.timestamp_sb.setMinimumSize(self.timestamp_sb.sizeHint())
        self.timestamp_sb.setText('No file loaded')
        self.statusBar().addWidget(self.timestamp_sb)

        self.lastline = ''

        self.ui.actionMonitorFileToggle.setEnabled(False)
        self.ui.actionReloadFile.setEnabled(False)
        self.ui.actionClearData.setEnabled(False)

        self.fileUpdateRate = 1000 # millisecond interval for checking the data file
        self.fileupdatetimer = QtCore.QTimer()
        self.fileupdatetimer.timeout.connect(self.checkFileUpdate)

        # set up toolbar actions
        self.ui.actionTest1.triggered.connect(self.test)
        self.ui.actionTest2.triggered.connect(self.test2)

        # set up searchText signals
        self.ui.searchText.editTextChanged.connect(self.on_actionClearData_triggered)
        self.ui.searchText.currentIndexChanged.connect(self.on_actionReloadFile_triggered)

    def test(self):
        self.load_format_presets()

    def test2(self):
        import pdb
        pdb.set_trace()
        print('test function 2')

    @QtCore.pyqtSlot(bool)
    def on_autoFormatButton_clicked(self, checked=None):
        print('auto formatting')
        s = str(self.ui.searchText.currentText())
        if s:
            s = re.sub('([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)', r'%f', s)  # replace float with %f
            s = re.sub('\s+', ' ', s)  # collapse white space
            self.ui.searchText.setEditText(s)

    @QtCore.pyqtSlot(bool)
    def on_actionMonitorFileToggle_triggered(self, checked=None):
        if checked:
            print('Starting live updates')
            self.fileupdatetimer.start(self.fileUpdateRate)
        else:
            print('Stopping live updates')
            self.fileupdatetimer.stop()

    @QtCore.pyqtSlot(int)
    def on_actionReloadFile_triggered(self):
        print('on_actionReloadFile_triggered')
        self.clearData()
        self.filelocation = 0
        if self.filepath:
            self.updateData()
        self.replot = True
        self.updatePlot()

    @QtCore.pyqtSlot(str)
    def on_actionClearData_triggered(self):
        print('on_actionClearData_triggered')
        self.clearData()
        self.updatePlot()

    def clearData(self):
        self.y = []

    @QtCore.pyqtSlot()
    def on_actionLoadPresetConfig_triggered(self):
        print('Loading default file')
        self.config.filepath = os.path.join(get_main_dir(),'sample_data.log')
        self.config.windowcomment = 'Sample data file'
        self.ui.searchText.setEditText('TC-CHC1-HC1: st A  s %f  m %f')
        self.ui.actionMonitorFileToggle.setEnabled(True)
        self.ui.actionReloadFile.setEnabled(True)
        self.ui.actionClearData.setEnabled(True)
        self.updateConfig()

    def checkFileUpdate(self):
        mod_time_check = self.modification_date(self.filepath)
        file_size_check = os.path.getsize(self.filepath)

        if mod_time_check != self.mod_time or file_size_check != self.file_size:
            self.mod_time = mod_time_check
            self.file_size = file_size_check
            self.updateData()
            self.updatePlot()
            self.updateStatusBar()

    @QtCore.pyqtSlot()
    def on_actionEditConfiguration_triggered(self):
        if self.config.edit(size=(400, 170)):
            self.ui.actionMonitorFileToggle.setEnabled(True)
            self.ui.actionReloadFile.setEnabled(True)
            self.ui.actionClearData.setEnabled(True)
            self.updateConfig()

    def updateConfig(self):
        if self.config.windowcomment == '':
            self.ui.centralwidget.window().setProperty('windowTitle', 'File Monitor (v%s-r%i)' % (__version__, self.buildNum))
        else:
            self.ui.centralwidget.window().setProperty('windowTitle',
                                                       '%s -- File Monitor (v%s-r%i)' %
                                                          (self.config.windowcomment, __version__, self.buildNum))

        if self.filepath != self.config.filepath:
            # stop monitoring current file
            if self.ui.actionMonitorFileToggle.isChecked():
                self.ui.actionMonitorFileToggle.trigger()

            self.filepath = self.config.filepath
            self.filelocation = 0
            self.clearData()
            self.updateData()
            self.replot = True

            # start monitoring the new file
            if not self.ui.actionMonitorFileToggle.isChecked():
                self.ui.actionMonitorFileToggle.trigger()

        if self.xlabel != self.config.xlabel:
            self.xlabel = self.config.xlabel
            self.replot = True

        if self.datalabelstring != self.config.datalabels:
            self.datalabelstring = self.config.datalabels
            self.replot = True

        if self.showlegend != self.config.legend:
            self.showlegend = self.config.legend
            self.replot = True

        self.updateStatusBar()
        self.updatePlot()

    def updateStatusBar(self):
        self.file_sb.setText(self.filepath)
        if self.mod_time:
            self.timestamp_sb.setText(datetime.datetime.strftime(self.mod_time, 'Updated at: %Y-%m-%d, %I:%M:%S %p'))

    def updateData(self):
        f = open(self.filepath, 'r')
        f.seek(self.filelocation)
        pattern = str(self.ui.searchText.currentText())

        line = self.lastline + f.readline()
        while len(line) > 0 and line[-1] == '\n':
            match = scanf(pattern, line)
            if match:
                if len(self.y) == 0:
                    self.y = [[float(s)] for s in match]
                else:
                    for i, ydata in enumerate(self.y):
                        ydata.append(float(match[i]))
                self.replot = True
            line = f.readline()

        self.lastline = line

        self.filelocation = f.tell()

        f.close()

    def updatePlot(self):
        # update the data labels
        labels = self.config.datalabels.split(',')
        self.datalabels = []
        for i in range(len(self.y)):
            if i < len(labels) and len(labels[i].strip()) > 0:
                self.datalabels.append(labels[i].strip())
            else:
                self.datalabels.append('Field %i' % (i+1))

        if len(self.y) == 0:
            for item in self.curves:
                self.ui.plotWidget.removeItem(item)
            self.curves = []

        # ---Update curve(s)
        if len(self.y):
            # plot index on X axis
            self.x = range(1, len(self.y[0])+1)

        if self.replot or len(self.y) != len(self.curves):  # first time through this function with data of a different length
            for item in self.curves:
                self.ui.plotWidget.removeItem(item)
            if self.legend is not None:
                for item in self.legend.items[:]:
                        self.legend.removeItem(item[1].text)
            self.curves = []
            for i, ydata in enumerate(self.y):
                self.curves.append(self.ui.plotWidget.plot(pen=self.colors[i % len(self.colors)], name=self.datalabels[i]))
            self.replot = False

            if not self.showlegend:
                if self.legend:
                    self.ui.plotWidget.removeItem(self.legend)
                    self.legend.setVisible(False)
                    self.legend = None
            else:
                if self.legend is None:
                    self.legend = self.ui.plotWidget.addLegend()
    
                    for item in self.curves:
                        self.legend.addItem(item, item.name())

            self.ui.plotWidget.setLabel('bottom', self.xlabel)
            
        for curve, ydata in zip(self.curves, self.y):
            curve.setData(self.x, ydata)

    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def on_clearButton_released(self):
        self.resetGraph()

    def on_searchText_textChanged(self):
        self.resetGraph()

    def resetGraph(self):
        self.x = []
        self.y = []
        self.updatePlot()

    def load_format_presets(self):
        formatStringFile = open(os.path.join(get_main_dir(), 'format_strings.txt'))
        for line in formatStringFile:
            self.ui.searchText.addItem(line.rstrip())
        formatStringFile.close()
        self.ui.searchText.setCurrentIndex(-1)


class GraphConfig(DataSet):
    """File Monitor Configuration"""

    filepath = FileOpenItem("Open file", ("log", "txt", "*"))

    windowcomment = StringItem('Window Comment', '',
                               help='Identifying string to add to the window title')

    _prop = GetAttrProp("legend")
    legend = BoolItem("Display legend", default=False).set_prop("display", store=_prop)

    datalabels = StringItem("Data Labels", '',
                        help='Comma-separated list of labels for the parsed data').set_prop("display",
                            active=FuncProp(_prop, lambda x: x))

    xlabel = StringItem("X Axis Label","Data Point Index",
                        help='Label for the Horizontal Axis')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainwindow = MainWindow()

    mainwindow.show()
    sys.exit(app.exec_())
