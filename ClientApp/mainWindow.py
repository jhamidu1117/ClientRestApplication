import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QSlider, QTextEdit
from PyQt5.QtWidgets import QPushButton, QMessageBox, QAction, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QSize, QUrl


import re
import os
import pandas as pd


class Window2(QMainWindow):
    def __init__(self, data):
        QMainWindow.__init__(self)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setMinimumSize(QSize(600, 400))
        self.setWindowTitle("TRG-Search")
        self.setWindowIcon(QtGui.QIcon(self.scriptDir + os.path.sep + 'Search.png'))
        self.Data = data

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('TRG:')
        self.textEdit = QTextEdit(self)
        self.textEdit.move(80, 25)
        self.textEdit.resize(400, 32)
        self.nameLabel.move(20, 25)

        self.pybutton = QPushButton('OK', self)
        self.pybutton.clicked.connect(self.clickMethod)
        self.pybutton.resize(400, 32)
        self.pybutton.move(80, 60)
        self.pybutton.setToolTip('This is a tooltip message.')

        self.outputLable = QLabel(self)
        self.outputLable.setText('Search:')
        self.textouput = QTextEdit(self)
        self.textouput.resize(400, 250)
        self.textouput.move(80, 95)
        self.outputLable.move(20, 95)
        self.textouput.setReadOnly(True)
        self.textouput.setLineWrapMode(QTextEdit.NoWrap)

        """"
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        for i in range(1, 50):
            object = QLabel("TextLabel")
            self.vbox.addWidget(object)
        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.setGeometry(600, 100, 1000, 900)
        """

    def clickMethod(self):
        wordList= re.sub("[^\w]", " ",  self.textEdit.toPlainText()).split()
        searchList = pd.DataFrame({'TRGID': wordList})
        searchList = searchList[searchList['TRGID'] != 'TRG']
        searchList = searchList.values
        self.Data = self.Data.astype({'TRGID': str})
        checkList = self.Data
        checkList['checkList'] = checkList['TRGID'].apply(self.stripList)
        checkList = checkList.values
        result1 = []
        result2 = []
        for row in checkList:
            for item in searchList:
                if row[2] == item[0]:
                    result1.append(item[0])
                    result2.append(row[1])
                    #print(item[0], row[1])
        result = pd.DataFrame({'TRGID': result1,
                               'TimeStamp': result2})
        result = result.to_string(index=False)
        self.textouput.setText(result)
        print(result)

    def stripList(self,Data):
        newList = re.sub('TRG-','',Data)
        return newList

class MainWindow(QMainWindow):
    def __init__(self, data):
        QMainWindow.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        url = QUrl.fromLocalFile(scriptDir + os.path.sep + 'Alarm.mp3')
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)

        self.setMinimumSize(QSize(600, 100))
        self.setWindowTitle("TRG-Duplicate Tracker")
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Logo2.png'))
        self.Data = data

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('TRG:')
        self.line = QLineEdit(self)
        self.line.move(80, 25)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        # Add button widget
        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        self.line.returnPressed.connect(self.clickMethod)
        pybutton.resize(200, 32)
        pybutton.move(80, 60)
        pybutton.setToolTip('This is a tooltip message.')

        # Create new action
        newAction = QAction(QtGui.QIcon(scriptDir + os.path.sep + 'Search.png'), '&Search', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        self.tailoutput = QTextEdit(self)
        self.tailoutput.move(350, 15)
        self.tailoutput.resize(200, 64)
        self.tailoutput.setFrameStyle(QTextEdit.NoFrame)
        self.tailoutput.viewport().setAutoFillBackground(False)
        self.tailoutput.setLineWrapMode(QTextEdit.NoWrap)
        self.tailoutput.setReadOnly(True)

        '''
        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openCall)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)
        '''

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Functions')
        fileMenu.addAction(newAction)

        '''
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        '''
    ''''
    def openCall(self):
        print('Open')
    '''


    def newCall(self):
        print('New')
        self.w = Window2(self.Data)
        self.w.show()

    '''
    def exitCall(self):
        print('Exit app')
    '''

    def clickMethod(self):
        if re.search('TRG.*', self.line.text()):
            newtext = re.sub(' ', '', self.line.text())
            newTRG = pd.DataFrame({'TRGID': [newtext],
                                   'timeStamp': [pd.Timestamp.now()]})

            newTRG['timeStamp'] = newTRG['timeStamp'].apply(lambda x: x.strftime('%x %X'))

            self.Data = self.Data.astype({'TRGID': str})

            i = 0
            for T in self.Data['TRGID']:
                if T == newtext:
                    self.player.play()
                    QMessageBox.about(self, 'Warning', 'Duplicate Found: '+T)
                    self.line.clear()
                    return 0
                i += 1

            self.Data = self.Data.append(newTRG, ignore_index=True, sort=False)
            self.Data.to_csv(r'TRGs.csv', index=False, header=True)
            result = self.Data.tail(3)
            result = result.to_string(index=False)
            self.tailoutput.setText(result)
            self.line.clear()
        elif re.search('L.*', self.line.text()):
            print('Current Location now ')
        else:
            self.player.play()
            QMessageBox.about(self, 'Warning', 'TRG not found')
            self.line.clear()
            return 0

if __name__ == "__main__":
    wk_dir = os.path.dirname('__file__')
    excelFile = 'TRGs.csv'
    excelPath = os.path.join(wk_dir, excelFile)
    TRGs = pd.read_csv(excelPath)

    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(TRGs)
    mainWin.show()
    sys.exit(app.exec_())