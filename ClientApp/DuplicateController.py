import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QSlider, QTextEdit, QGridLayout
from PyQt5.QtWidgets import QPushButton, QMessageBox, QAction, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QStackedLayout, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QSize, QUrl, Qt


import re
import os
import pandas as pd


class DuplicateTracker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        url = QUrl.fromLocalFile(scriptDir + os.path.sep + 'Resources/Alarm.mp3')
        self.excelNumbers = os.path.join(scriptDir, r'Data/TRGs.csv')
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.currentLocation = ''
        self.initUI()

    def initUI(self):
        self.scanlabel = QLabel('TRGs:')

        self.scanline = QLineEdit()
        self.scanline.setPlaceholderText('TRG-#########')

        # self.histdisp = QTextEdit()
        # self.histdisp.setFrameStyle(QTextEdit.NoFrame)
        # self.histdisp.viewport().setAutoFillBackground(False)
        # self.histdisp.setLineWrapMode(QTextEdit.NoWrap)
        # self.histdisp.setReadOnly(True)

        self.histdispTable = QTableWidget()
        self.histdispTable.setColumnCount(3)
        self.histdispTable.setRowCount(3)
        self.histdispTable.setHorizontalHeaderLabels(['TRGID', 'timeStamp', 'Location'])

        self.enterbutton = QPushButton('Enter')
        self.enterbutton.clicked.connect(self.clickMethod)
        self.scanline.returnPressed.connect(self.clickMethod)

        self.redoButton = QPushButton('Redo')
        self.enterbutton.clicked.connect(self.redoMethod)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.scanlabel, 3, 1)
        grid.addWidget(self.scanline, 3, 0)
        grid.addWidget(self.enterbutton, 4, 0)
        grid.addWidget(self.redoButton, 4, 1)
        grid.addWidget(self.histdispTable, 0, 0, 3, 2)

        self.setLayout(grid)

    def redoMethod(self):
        self.w = Window2()
        self.w.show()


    def clickMethod(self):
        # print(self.scanline.text())
        line = self.scanline.text()
        data = pd.read_csv(self.excelNumbers, index_col='TRGID')
        if re.search('TRG.*', line):
            if self.currentLocation == '':
                self.player.play()
                QMessageBox.about(self, 'Warning', 'Scan Location To Continue')
                self.scanline.clear()
                return 0

            newtext = re.sub(' ', '', line)
            newTRG = pd.DataFrame({'TRGID': [newtext],
                                   'timeStamp': [pd.Timestamp.now()],
                                   'Location': [self.currentLocation]})
            newTRG['timeStamp'] = newTRG['timeStamp'].apply(lambda x: x.strftime('%x %X'))

            if newtext in data.index:
                self.player.play()
                QMessageBox.about(self, 'Warning', 'Duplicate Found:\nPlease Notify your line lead\n' + newtext)
                self.scanline.clear()
                return 0

            data.reset_index(inplace=True)
            data = data.append(newTRG, ignore_index=True, sort=False)
            data.to_csv(r'TRGs.csv', index=False, header=True)
            result = data.tail(3)
            result = result.values
            i = 0
            for v in result:
                # print(v)
                self.histdispTable.setItem(i, 0, QTableWidgetItem(str(v[0])))
                self.histdispTable.setItem(i, 1, QTableWidgetItem(str(v[1])))
                self.histdispTable.setItem(i, 2, QTableWidgetItem(str(v[2])))
                i += 1

            self.scanline.clear()
        elif re.search('L.*', line):
            # print('Location updated' + line)
            self.scanlabel.setText('Location: ' + line)
            self.currentLocation = line
            self.scanline.clear()
        else:
            self.player.play()
            QMessageBox.about(self, 'Warning', 'TRG not Found')
            self.scanline.clear()
            return 0
