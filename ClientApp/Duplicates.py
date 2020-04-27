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

class Window2(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setMinimumSize(QSize(500, 200))
        self.setWindowIcon(QtGui.QIcon(self.scriptDir + os.path.sep + 'Resources/redo.ico'))
        self.setWindowTitle('Redo TRG Location')

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/Logo2.ico'))
        self.setMinimumSize(QSize(700, 200))
        self.setWindowTitle('TRG-Duplicate Tracker')

        bar = self.menuBar()
        Functions_menu = bar.addMenu('Functions')

        scan_action = QAction('Scan', self)
        scan_action.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/Scan.ico'))
        scan_action.triggered.connect(self.scanScreen)

        search_action = QAction('Search', self)
        search_action.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/Search.ico'))
        search_action.triggered.connect(self.searchScreen)

        CheckLoc_action = QAction('Check Locations', self)
        CheckLoc_action.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/Racks.ico'))
        CheckLoc_action.triggered.connect(self.rackScreen)

        Functions_menu.addAction(scan_action)
        Functions_menu.addAction(search_action)
        Functions_menu.addAction(CheckLoc_action)

        blankWidget = QWidget()
        self.dupWidget = DuplicateTracker()
        self.searchWidget = Searcher()
        self.rackwidget = Racker()

        self.layout = QStackedLayout()
        self.layout.addWidget(self.dupWidget)
        self.layout.addWidget(self.searchWidget)
        self.layout.addWidget(self.rackwidget)

        blankWidget.setLayout(self.layout)
        self.setCentralWidget(blankWidget)

    def searchScreen(self):
        self.layout.setCurrentIndex(1)

    def scanScreen(self):
        self.layout.setCurrentIndex(0)

    def rackScreen(self):
        self.layout.setCurrentIndex(2)


class RedoWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.excelNumbers = os.path.join(scriptDir, r'Data/TRGs.csv')
        self.currentTRG = ''
        self.initUI()

    def initUI(self):
        self.scanlabel = QLabel('Enter TRG:')

        self.histdispTable = QTableWidget()
        self.histdispTable.setColumnCount(3)
        self.histdispTable.setRowCount(3)
        self.histdispTable.setHorizontalHeaderLabels(['TRGID', 'timeStamp', 'Location'])

        self.scanline = QLineEdit()
        self.scanline.setPlaceholderText('TRG-#########')

        self.enterbutton = QPushButton('Enter')
        self.enterbutton.clicked.connect(self.clickMethod)
        self.scanline.returnPressed.connect(self.clickMethod)

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.scanlabel, 3, 1)
        grid.addWidget(self.scanline, 3, 0)
        grid.addWidget(self.enterbutton, 4, 0)
        grid.addWidget(self.histdispTable, 0, 0, 3, 2)

        self.setLayout(grid)

    def clickMethod(self):
        #print(self.scanline.text())
        line = self.scanline.text()
        data = pd.read_csv(self.excelNumbers, index_col='TRGID')
        if re.search('TRG.*', line):
            if self.currentTRG == '':
                newtext = re.sub(' ', '', line)
                if newtext in data.index:
                    self.currentTRG = newtext
                    self.scanlabel.setText(newtext)
                    self.scanlabel.clear()
                else:
                    QMessageBox.about(self, 'Warning', newtext + ' not Scanned exit window to continue')
                    self.scanlabel.clear()
            else:
                QMessageBox.about(self, 'Warning', 'Scan a new Location you Are Trying to '
                                                   '\nChange the location of')
                self.scanlabel.clear()
        elif re.search('L.*', line):
            if self.currentTRG == '':
                QMessageBox.about(self, 'Warning', 'Scan The TRG you Are Trying to '
                                                   '\nChange the location of')
                self.scanlabel.clear()


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

        #self.histdisp = QTextEdit()
        #self.histdisp.setFrameStyle(QTextEdit.NoFrame)
        #self.histdisp.viewport().setAutoFillBackground(False)
        #self.histdisp.setLineWrapMode(QTextEdit.NoWrap)
        #self.histdisp.setReadOnly(True)

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
        #print(self.scanline.text())
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
                #print(v)
                self.histdispTable.setItem(i, 0, QTableWidgetItem(str(v[0])))
                self.histdispTable.setItem(i, 1, QTableWidgetItem(str(v[1])))
                self.histdispTable.setItem(i, 2, QTableWidgetItem(str(v[2])))
                i += 1

            self.scanline.clear()
        elif re.search('L.*', line):
            #print('Location updated' + line)
            self.scanlabel.setText('Location: ' + line)
            self.currentLocation = line
            self.scanline.clear()
        else:
            self.player.play()
            QMessageBox.about(self, 'Warning', 'TRG not Found')
            self.scanline.clear()
            return 0


class Searcher(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.excelNumbers = os.path.join(scriptDir, r'TRGs.csv')
        self.initUI()

    def initUI(self):
        self.searchLable = QLabel('TRGs:')

        self.searchline = QTextEdit()
        self.searchline.setLineWrapMode(QTextEdit.NoWrap)

        self.ouput = QTextEdit()
        self.ouput.setReadOnly(True)
        self.ouput.setLineWrapMode(QTextEdit.NoWrap)
        
        self.outputTable = QTableWidget()
        self.outputTable.setColumnCount(3)
        self.outputTable.setHorizontalHeaderLabels(['TRGID', 'timeStamp', 'Location'])

        self.searchButton = QPushButton('Search')
        self.searchButton.clicked.connect(self.clickMethod)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.searchLable, 0, 0, 1, 1)
        grid.addWidget(self.searchline, 0, 1, 1, 1)
        grid.addWidget(self.outputTable, 1, 1, 4, 2)
        grid.addWidget(self.searchButton, 4, 0, 2, 1)
        self.setLayout(grid)

    def clickMethod(self):
        if self.searchline.toPlainText() == '':
            self.outputTable.setRowCount(0)
            return 0

        wordList = re.sub("[^\w]", " ", self.searchline.toPlainText()).split()
        #print(wordList)
        searchFrame = pd.DataFrame({'TRGID': wordList})
        searchFrame = searchFrame[searchFrame['TRGID'] != 'TRG']
        searchFrame = searchFrame.values

        df = pd.read_csv(self.excelNumbers)
        df['checkList'] = df['TRGID'].apply(self.stripList)
        df['checkList'] = df['checkList'].astype(str)
        df.set_index(keys='checkList', inplace=True)
        #print(df)
        i = 0
        self.outputTable.setRowCount(0)
        for w in searchFrame:
            #print(str(w[0]))
            if str(w[0]) in df.index:
                row = df.loc[str(w[0])].values
                self.outputTable.setRowCount(i+1)
                self.outputTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.outputTable.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.outputTable.setItem(i, 2, QTableWidgetItem(str(row[2])))
                i += 1


    def stripList(self, data):
        newList = re.sub('TRG-', '', data)
        return newList


class Racker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.FMSICSV = ''
        self.emptyLocations = pd.DataFrame({'TRGID': [],
                                            'LocationID': [],
                                            'ProductStatus': [],
                                            'LocationShortName': []})

        self.initUI()

    def initUI(self):
        self.searchLable = QLabel('Locations:')

        self.searchline = QTextEdit()
        self.searchline.setLineWrapMode(QTextEdit.NoWrap)

        self.outputTable = QTableWidget()
        self.outputTable.setColumnCount(7)
        self.outputTable.setHorizontalHeaderLabels(['LocationID', 'LocationName', 'TRGID Count', ' : ',
                                                    'ScannedLocations', 'ScannedTRGcount', 'Difference'])
        self.searchButton = QPushButton('Search')
        self.searchButton.clicked.connect(self.clickMethod)
        self.SelectedDisp1 = QLabel('SelectFIle')

        self.fileButton = QPushButton('Select File')
        self.fileButton.clicked.connect(self.fileSelect)

        #vbox = QVBoxLayout()
        #self.outputTable.setLayout(vbox)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.searchLable, 0, 0, 1, 1)
        grid.addWidget(self.searchline, 0, 1, 1, 1)
        grid.addWidget(self.outputTable, 1, 1, 4, 2)
        grid.addWidget(self.SelectedDisp1, 2, 0)
        grid.addWidget(self.fileButton, 3, 0)
        grid.addWidget(self.searchButton, 4, 0, 2, 1)
        self.setLayout(grid)

    def fileSelect(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;CSV Files (*.CSV)", options=options)
        if fileName:
            # print(fileName)
            self.FMSICSV = fileName
            path, name = os.path.split(fileName)
            head, tail = os.path.splitext(fileName)
            self.SelectedDisp1.setText(name)
            #print(name)

    def clickMethod(self):
        if self.FMSICSV == '':
            self.outputTable.setRowCount(0)
            return 0
        else:
            self.outputTable.setRowCount(0)
            self.filexrevolver(self.FMSICSV)
            copy = pd.DataFrame({'TRGID': self.emptyLocations['TRGID'].values,
                                 'LocationID': self.emptyLocations['LocationID'].values,
                                 'ProductStatus': self.emptyLocations['ProductStatus'].values,
                                 'LocationShortName': self.emptyLocations['LocationShortName'].values})
            locations = copy.groupby(['LocationShortName', 'LocationID']).count()[['TRGID']]
            locations.reset_index(inplace=True)
            locations = locations.values
            i = 0
            for row in locations:
                self.outputTable.setRowCount(i+1)
                self.outputTable.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.outputTable.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.outputTable.setItem(i, 2, QTableWidgetItem(str(row[2])))
                i += 1

            #print(locations)

    def filexrevolver(self, locs):
        path, name = os.path.split(locs)
        head, tail = os.path.splitext(locs)
        if tail == '.csv':
            self.emptyLocations = pd.read_csv(locs, usecols=self.emptyLocations.columns)
        elif tail == '.xlsx':
            self.emptyLocations = pd.read_excel(locs, usecols=self.emptyLocations.columns)

    def CleanLocations(self, locid):
        print(locid)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

